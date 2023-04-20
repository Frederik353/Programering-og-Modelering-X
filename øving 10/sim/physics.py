
import sim
import sim.utils as utils

import numpy as np
from scipy.spatial.transform import Rotation


def finn_rel_velocity(svw, R):
    _, v, w, _ = svw
    return v + R * np.cross(np.array([0,0,1]), w)

def løs_kule_kule_kolisjon(svw1, svw2):

    r1, r2 = svw1[0], svw2[0]
    v1, v2 = svw1[1], svw2[1]

    v_rel = v1 - v2
    v_mag = np.linalg.norm(v_rel)

    n = utils.unit_vector(r2 - r1)
    t = utils.coordinate_rotation(n, np.pi/2)

    beta = utils.angle(v_rel, n)

    svw1[1] = t * v_mag*np.sin(beta) + v2
    svw2[1] = n * v_mag*np.cos(beta) + v2

    # finner minste rotasjonsvektor for å unngå problemer senere
    svw1[3] = utils.normalize_rotation_vector(svw1[3])
    svw2[3] = utils.normalize_rotation_vector(svw2[3])

    return svw1, svw2


def løs_kule_vegg_kolisjon(svw, normal, R, m, h):

    # normal fra vegg og ut fra spilleflaten
    normal = normal if np.dot(normal, svw[1]) > 0 else -normal

    # endrer referansesystemet
    psi = utils.angle(normal)
    svw_R = utils.coordinate_rotation(svw.T, -psi).T

    phi = utils.angle(svw_R[1]) % (2*np.pi)

    e = finn_ball_vegg_restitution(svw_R)
    mu = finn_ball_vegg_friction(svw_R)

    # avhengig av høyde på veggen relativt til kulen
    theta_a = np.arcsin(h/R - 1)

    sx = svw_R[1,0]*np.sin(theta_a) - svw_R[1,2]*np.cos(theta_a) + R*svw_R[2,1]
    sy = -svw_R[1,1] - R*svw_R[2,2]*np.cos(theta_a) + R*svw_R[2,0]*np.sin(theta_a)
    c = svw_R[1,0]*np.cos(theta_a)

    I = 2/5*m*R**2
    A = 7/2/m
    B = 1/m

    PzE = (1 + e)*c/B
    PzS = np.sqrt(sx**2 + sy**2)/A

    if PzS <= PzE:
        PX = -sx/A*np.sin(theta_a) - (1+e)*c/B*np.cos(theta_a)
        PY = sy/A
        PZ = sx/A*np.cos(theta_a) - (1+e)*c/B*np.sin(theta_a)
    else:
        PX = -mu*(1+e)*c/B*np.cos(phi)*np.sin(theta_a) - (1+e)*c/B*np.cos(theta_a)
        PY = mu*(1+e)*c/B*np.sin(phi)
        PZ = mu*(1+e)*c/B*np.cos(phi)*np.cos(theta_a) - (1+e)*c/B*np.sin(theta_a)

    # oppdater fart
    svw_R[1,0] += PX/m
    svw_R[1,1] += PY/m

    # opdater vinkelmoment
    svw_R[2,0] += -R/I*PY*np.sin(theta_a)
    svw_R[2,1] += R/I*(PX*np.sin(theta_a) - PZ*np.cos(theta_a))
    svw_R[2,2] += R/I*PY*np.cos(theta_a)

    # endre tilbake til bord referansesystemet
    svw = utils.coordinate_rotation(svw_R.T, psi).T

    # igjen finner vi minste rotasjonsvektor for å unngå problemer senere
    svw[3] = utils.normalize_rotation_vector(svw[3])

    return svw


def finn_ball_vegg_restitution(svw):
    # finn restituisjons koefisienten avhengig av ball tilstand
    return max([
        0.40,
        0.50 + 0.257*svw[1,0] - 0.044*svw[1,0]**2
    ])


def finn_ball_vegg_friction(svw):
    # finn friksjons koefisienten avhengig av ball tilstand

    ang = utils.angle(svw[1])

    if ang > np.pi:
        ang = np.abs(2*np.pi - ang)

    return 0.471 - 0.241*ang
    return 0.38 - 0.241*ang
    return 0


def finn_kule_kule_kolisjon_tid(svw1, svw2, s1, s2, mu1, mu2, m1, m2, g, R):
    # tid til kolisjon mellom de to kulene

    c1x, c1y = svw1[0, 0], svw1[0, 1]
    c2x, c2y = svw2[0, 0], svw2[0, 1]

    if s1 == sim.stille or s1 == sim.spinnenende:
        a1x, a1y, b1x, b1y = 0, 0, 0, 0
    else:
        phi1 = utils.angle(svw1[1])
        v1 = np.linalg.norm(svw1[1])

        u1 = (np.array([1,0,0])
              if s1 == sim.rullende
              else utils.coordinate_rotation(utils.unit_vector(finn_rel_velocity(svw1, R)), -phi1))

        a1x = -1/2*mu1*g*(u1[0]*np.cos(phi1) - u1[1]*np.sin(phi1))
        a1y = -1/2*mu1*g*(u1[0]*np.sin(phi1) + u1[1]*np.cos(phi1))
        b1x = v1*np.cos(phi1)
        b1y = v1*np.sin(phi1)

    if s2 == sim.stille or s2 == sim.spinnenende:
        a2x, a2y, b2x, b2y = 0, 0, 0, 0
    else:
        phi2 = utils.angle(svw2[1])
        v2 = np.linalg.norm(svw2[1])

        u2 = (np.array([1,0,0])
              if s2 == sim.rullende
              else utils.coordinate_rotation(utils.unit_vector(finn_rel_velocity(svw2, R)), -phi2))

        a2x = -1/2*mu2*g*(u2[0]*np.cos(phi2) - u2[1]*np.sin(phi2))
        a2y = -1/2*mu2*g*(u2[0]*np.sin(phi2) + u2[1]*np.cos(phi2))
        b2x = v2*np.cos(phi2)
        b2y = v2*np.sin(phi2)

    Ax, Ay = a2x-a1x, a2y-a1y
    Bx, By = b2x-b1x, b2y-b1y
    Cx, Cy = c2x-c1x, c2y-c1y

    a = Ax**2 + Ay**2
    b = 2*Ax*Bx + 2*Ay*By
    c = Bx**2 + 2*Ax*Cx + 2*Ay*Cy + By**2
    d = 2*Bx*Cx + 2*By*Cy
    e = Cx**2 + Cy**2 - 4*R**2

    roots = np.roots([a,b,c,d,e])

    roots = roots[
        (abs(roots.imag) <= sim.toleranse) & \
        (roots.real > sim.toleranse)
    ].real

    return roots.min() if len(roots) else np.inf


def finn_kule_vegg_kolisjon_tid(svw, s, lx, ly, l0, mu, m, g, R):
    # tid til kolisjon mellom kule og vegg
    if s == sim.stille or s == sim.spinnenende:
        return np.inf

    phi = utils.angle(svw[1])
    v = np.linalg.norm(svw[1])

    u = (np.array([1,0,0]
         if s == sim.rullende
         else utils.coordinate_rotation(utils.unit_vector(finn_rel_velocity(svw, R)), -phi)))

    ax = -1/2*mu*g*(u[0]*np.cos(phi) - u[1]*np.sin(phi))
    ay = -1/2*mu*g*(u[0]*np.sin(phi) + u[1]*np.cos(phi))
    bx, by = v*np.cos(phi), v*np.sin(phi)
    cx, cy = svw[0, 0], svw[0, 1]

    A = lx*ax + ly*ay
    B = lx*bx + ly*by
    C1 = l0 + lx*cx + ly*cy + R*np.sqrt(lx**2 + ly**2)
    C2 = l0 + lx*cx + ly*cy - R*np.sqrt(lx**2 + ly**2)

    roots = np.append(np.roots([A,B,C1]), np.roots([A,B,C2]))

    roots = roots[
        (abs(roots.imag) <= sim.toleranse) & \
        (roots.real > sim.toleranse)
    ].real

    return roots.min() if len(roots) else np.inf


def finn_glide_tid(svw, R, u_g, g):
    return 2*np.linalg.norm(finn_rel_velocity(svw, R)) / (7*u_g*g)

def finn_rulle_tid(svw, u_r, g):
    _, v, _, _ = svw
    return np.linalg.norm(v) / (u_r*g)

def finn_spinne_tid(svw, R, u_sp, g):
    _, _, w, _ = svw
    return np.abs(w[2]) * 2/5*R/u_sp/g


def avanser_kule_bevegelse(tilstand, svw, R, m, u_g, u_sp, u_r, g, t):
    if tilstand == sim.stille:
        return svw, tilstand

    if tilstand == sim.glidende:
        tau_glide = finn_glide_tid(svw, R, u_g, g)

        if t >= tau_glide:
            svw = avanser_glide_tilstand(svw, R, m, u_g, u_sp, g, tau_glide)
            tilstand = sim.rullende
            t -= tau_glide
        else:
            return avanser_glide_tilstand(svw, R, m, u_g, u_sp, g, t), sim.glidende

    if tilstand == sim.rullende:
        tau_rulle = finn_rulle_tid(svw, u_r, g)

        if t >= tau_rulle:
            svw = avanser_rulle_tilstand(svw, R, u_r, u_sp, g, tau_rulle)
            tilstand = sim.spinnenende
            t -= tau_rulle
        else:
            return avanser_rulle_tilstand(svw, R, u_r, u_sp, g, t), sim.rullende

    if tilstand == sim.spinnenende:
        tau_spinne = finn_spinne_tid(svw, R, u_sp, g)

        if t >= tau_spinne:
            return avanser_perpendicular_spinne_tilstand(svw, R, u_sp, g, tau_spinne), sim.stille
        else:
            return avanser_perpendicular_spinne_tilstand(svw, R, u_sp, g, t), sim.spinnenende


def avanser_glide_tilstand(svw, R, m, u_g, u_sp, g, t):
    if t == 0:
        return svw

    # vinkel til fartsvektor i bord referansesystem
    phi = utils.angle(svw[1])

    svw_B0 = utils.coordinate_rotation(svw.T, -phi).T

    # relativ fart mellom kule og bord i kule referansesystem
    u_0 = utils.coordinate_rotation(utils.unit_vector(finn_rel_velocity(svw, R)), -phi)


    # regn ut ny fart, posisjon og vinkelmoment i x og y retningene
    svw_B = np.array([
        np.array([svw_B0[1,0]*t - 1/2*u_g*g*t**2 * u_0[0], -1/2*u_g*g*t**2 * u_0[1], 0]),
        svw_B0[1] - u_g*g*t*u_0,
        svw_B0[2] - 5/2/R*u_g*g*t * np.cross(u_0, np.array([0,0,1])),
        svw_B0[3] + svw_B0[2]*t - 1/2 * 5/2/R*u_g*g*t**2 * np.cross(u_0, np.array([0,0,1])),
    ])

    # avanser vinkelmoment i z aksen
    svw_B[2, 2] = svw_B0[2, 2]
    svw_B[3, 2] = svw_B0[3, 2]
    svw_B = avanser_perpendicular_spinne_tilstand(svw_B, R, u_sp, g, t)

    # roter tilbake til bord referansesystemet
    svw_T = utils.coordinate_rotation(svw_B.T, phi).T
    svw_T[0] += svw[0] # Add initial kule position

    return svw_T


def avanser_rulle_tilstand(svw, R, u_r, u_sp, g, t):
    if t == 0:
        return svw

    r_0, v_0, w_0, e_0 = svw

    v_0_hat = utils.unit_vector(v_0)

    r = r_0 + v_0 * t - 1/2*u_r*g*t**2 * v_0_hat
    v = v_0 - u_r*g*t * v_0_hat
    w = utils.coordinate_rotation(v/R, np.pi/2)
    e = e_0 + utils.coordinate_rotation((v_0*t - 1/2*u_r*g*t**2 * v_0_hat)/R, np.pi/2)

    # Independently avanser the z spinne
    temp = avanser_perpendicular_spinne_tilstand(svw, R, u_sp, g, t)

    w[2] = temp[2, 2]
    e[2] = temp[3, 2]

    return np.array([r, v, w, e])


def avanser_perpendicular_spinne_component(wz, ez, R, u_sp, g, t):
    if t == 0:
        return wz, ez

    if abs(wz) < sim.toleranse:
        return wz, ez

    alpha = 5*u_sp*g/(2*R)

    if t > abs(wz)/alpha:
        # kan ikke gå fra positiv til negativ vinkelmoment uten en påvirkende kraft
        t = abs(wz)/alpha

    # vinkelmomentet går mot 0 over tid
    sign = 1 if wz > 0 else -1

    wz_final = wz - sign*alpha*t
    ez_final = ez + wz*t - sign*1/2*alpha*t**2

    return wz_final, ez_final


def avanser_perpendicular_spinne_tilstand(svw, R, u_sp, g, t):
    svw = svw.copy()

    svw[2, 2], svw[3, 2] = avanser_perpendicular_spinne_component(svw[2, 2], svw[3, 2], R, u_sp, g, t)
    return svw


def stav_skudd(m, M, R, V0, phi, theta, a, b):
    """
    parametere:

    m : kule masse
    M : stav masse
    R : radius til kule
    V0 : opprinnelig fart til stav ved skudd
    phi : vinkel i grader i forhold til x-aksen (positiv retning)
    theta : vinkel i grader i forhold til xy planet
    a : hvor mye til siden på ballen treffer man df 1,-1
    b : hvor vertikalt på ballen treffer man df 1,-1
    """

    a *= R
    b *= R

    phi *= np.pi/180
    theta *= np.pi/180

    I = 2/5 * m * R**2

    c = np.sqrt(R**2 - a**2 - b**2)

    # finn kraft ved støt
    numerator = 2 * M * V0
    temp = a**2 + (b*np.cos(theta))**2 + (c*np.cos(theta))**2 - 2*b*c*np.cos(theta)*np.sin(theta)
    denominator = 1 + m/M + 5/2/R**2 * temp
    F = numerator/denominator

    v_B = -F/m * np.array([0, np.cos(theta), 0])
    w_B = F/I * np.array([-c*np.sin(theta) + b*np.cos(theta), a*np.sin(theta), -a*np.cos(theta)])

    # roter til bord referansesystemet
    rot_angle = phi + np.pi/2
    v_T = utils.coordinate_rotation(v_B, rot_angle)
    w_T = utils.coordinate_rotation(w_B, rot_angle)

    return v_T, w_T

