import sim
import sim.physics as physics
import sim.configurations as configurations

from sim.objects import (
    Kule,
    Bord,
    Billiardkølle,
)
import numpy as np


class Hendelse(object):
    def __init__(self, event_type, agents, tau):
        self.agents = agents
        self.tau = tau
        self.event_type = event_type


class SkuddLog(object):
    # lagrer endringen til kulene over tid

    def __init__(self):
        self.kuler = {}
        self.reset_log()

    def reset_log(self):
        self.vectorized = False

        self.log = {
            'kuler': {},
            'index': [],
            'tid': [],
            'event': [],
        }

        self.n = -1
        self.tid = 0

        self.touch_log()

    def touch_log(self):
        #initialiserer kulebanene hvis ikke allerede initialisert

        for kule_id in self.kuler:
            if kule_id not in self.log['kuler']:
                self.init_kule_log(kule_id)

    def init_kule_log(self, kule_id):

        self.log['kuler'][kule_id] = {
            's': [np.nan] * self.n,
            'svw': [np.nan * np.ones((4, 3))] * self.n,
            'euler': [np.nan * np.ones((4, 3))] * self.n,
            'quat': [np.nan * np.ones((4, 4))] * self.n,
        }

    def tidstamp(self, dt, event=None):
        #opp
        self.n += 1
        self.tid += dt

        # lagrer tiden i loggen
        self.log['tid'].append(self.tid)
        self.log['index'].append(self.n)

        # lagrer eventen i loggen
        self.log['event'].append(event)

        # lagrer kulenes tilstander
        for kule_id, kule in self.kuler.items():
            self.log['kuler'][kule_id]['s'].append(kule.s)
            self.log['kuler'][kule_id]['svw'].append(kule.svw)

    def continuize(self, dt=0.05):
        # fyller inn tiden mellom hendelsene ved å løse funksjonene for hver delta tid dt fram til hendelsen
        old_log = self.log
        self.reset_log()

        self.set_bord_tilstand_fra_log(index=0, log=old_log)
        self.tidstamp(0)

        dt_prime = dt
        for index, event in zip(old_log['index'], old_log['event']):

            if not isinstance(event, Hendelse):
                continue

            if event.tau == np.inf:
                break

            # løser funksjonene for hver delta tid dt fram til hendelsen
            event_tid = 0
            while event_tid < (event.tau - dt_prime):
                self.avanser(dt_prime, log=False)
                self.tidstamp(dt, event=None)
                event_tid += dt_prime

                dt_prime = dt

            dt_prime = dt - (event.tau - event_tid)
            # lagre kule tilstandene som skjer før hendelsen i loggen
            self.set_bord_tilstand_fra_log(index=index, log=old_log)

        self.vektoriser_log()

    def set_bord_tilstand_fra_log(self, index, log=None):
        if log is None:
            log = self.log

        for kule_id, kule in self.kuler.items():
            kule.set(
                log['kuler'][kule_id]['svw'][index],
                log['kuler'][kule_id]['s'][index],
            )

    def vektoriser_log(self):

        self.log['index'] = np.array(self.log['index'])
        self.log['tid'] = np.array(self.log['tid'])
        for kule in self.log['kuler']:
            self.log['kuler'][kule]['s'] = np.array(
                self.log['kuler'][kule]['s'])
            self.log['kuler'][kule]['svw'] = np.array(
                self.log['kuler'][kule]['svw'])
            self.log['kuler'][kule]['euler'] = np.array(
                self.log['kuler'][kule]['euler'])
            self.log['kuler'][kule]['quat'] = np.array(
                self.log['kuler'][kule]['quat'])

        self.vectorized = True


class SkuddSimulasjon(SkuddLog):
    # simulerer et skudd

    def __init__(self):
        self.g = sim.g

        self.stav = None
        self.bord = None

        SkuddLog.__init__(self)

    def simuler(self, tid=None, name='NA'):
        self.touch_log()

        event = Hendelse(event_type=None, agents=tuple(), tau=0)

        self.tidstamp(0, event)
        while event.tau < np.inf:
            event = self.finn_next_event()
            self.avanser(dt=event.tau, event=event)

            if tid is not None and self.tid >= tid:
                break

        self.vektoriser_log()

    def set_stav(self, stav):
        self.stav = stav

    def set_bord(self, bord):
        self.bord = bord

    def set_kuler(self, kuler):
        self.kuler = kuler

    def avanser(self, dt, log=True, event=None):
        for kule_id, kule in self.kuler.items():
            svw, s = physics.avanser_kule_bevegelse(
                tilstand=kule.s,
                svw=kule.svw,
                R=kule.R,
                m=kule.m,
                u_g=self.bord.u_g,
                u_sp=self.bord.u_sp,
                u_r=self.bord.u_r,
                g=self.g,
                t=dt,
            )
            kule.set(svw, s)

        if event is not None:
            self.løs(event)

        if log:
            self.tidstamp(dt, event=event)

    def løs(self, event):
        if not event.event_type:
            return

        if event.event_type == 'kule-kule':
            kule_id1, kule_id2 = event.agents

            svw1 = self.kuler[kule_id1].svw
            svw2 = self.kuler[kule_id2].svw

            svw1, svw2 = physics.løs_kule_kule_kolisjon(svw1, svw2)
            s1, s2 = sim.glidende, sim.glidende

            self.kuler[kule_id1].set(svw1, s1)
            self.kuler[kule_id2].set(svw2, s2)

        elif event.event_type == 'kule-vegg':
            kule_id, vegg_id = event.agents

            kule = self.kuler[kule_id]
            vegg = self.bord.veggs[vegg_id]

            svw = self.kuler[kule_id].svw
            normal = self.bord.veggs[vegg_id].normal

            svw = physics.løs_kule_vegg_kolisjon(
                svw=kule.svw,
                normal=vegg.normal,
                R=kule.R,
                m=kule.m,
                h=vegg.height,
            )
            s = sim.glidende

            self.kuler[kule_id].set(svw, s)

    def finn_next_event(self):
        # finn ut hva neste hendelse er
        tau_min = np.inf
        agents = tuple()
        event_type = None

        tau, ids, e = self.finn_min_bevegelse_event_tid()
        if tau < tau_min:
            tau_min = tau
            event_type = e
            agents = ids

        tau, ids = self.finn_min_kule_kule_event_tid()
        if tau < tau_min:
            tau_min = tau
            event_type = 'kule-kule'
            agents = ids

        tau, ids = self.finn_min_kule_vegg_event_tid()
        if tau < tau_min:
            tau_min = tau
            event_type = 'kule-vegg'
            agents = ids

        return Hendelse(event_type, agents, tau_min)

    def finn_min_bevegelse_event_tid(self):
        # finn tid til neste overgang mellom to tilstander for en av kulene er 

        tau_min = np.inf
        kule_id = None
        event_type_min = None

        for kule in self.kuler.values():
            if kule.s == sim.stille:
                continue
            elif kule.s == sim.rullende:
                tau = physics.finn_rulle_tid(kule.svw, self.bord.u_r, self.g)
                event_type = 'end-rulle'
            elif kule.s == sim.glidende:
                tau = physics.finn_glide_tid(
                    kule.svw, kule.R, self.bord.u_g, self.g)
                event_type = 'end-glide'
            elif kule.s == sim.spinnenende:
                tau = physics.finn_spinne_tid(
                    kule.svw, kule.R, self.bord.u_sp, self.g)
                event_type = 'end-spinne'

            if tau < tau_min:
                tau_min = tau
                kule_id = kule.id
                event_type_min = event_type

        return tau_min, (kule_id, ), event_type_min

    def finn_min_kule_kule_event_tid(self):
        # finn tid til neste kule - kule kollisjon

        tau_min = np.inf
        kule_ids = tuple()

        for i, kule1 in enumerate(self.kuler.values()):
            for j, kule2 in enumerate(self.kuler.values()):
                if i >= j:
                    continue

                if kule1.s == sim.stille and kule2.s == sim.stille:
                    continue

                tau = physics.finn_kule_kule_kolisjon_tid(
                    svw1=kule1.svw,
                    svw2=kule2.svw,
                    s1=kule1.s,
                    s2=kule2.s,
                    mu1=(self.bord.u_g if kule1.s ==
                         sim.glidende else self.bord.u_r),
                    mu2=(self.bord.u_g if kule2.s ==
                         sim.glidende else self.bord.u_r),
                    m1=kule1.m,
                    m2=kule2.m,
                    g=self.g,
                    R=kule1.R
                )

                if tau < tau_min:
                    kule_ids = (kule1.id, kule2.id)
                    tau_min = tau

        return tau_min, kule_ids

    def finn_min_kule_vegg_event_tid(self):
        # finn tid til neste kule - vegg kollisjon

        tau_min = np.inf
        agent_ids = (None, None)

        for kule in self.kuler.values():
            if kule.s == sim.stille:
                continue

            for vegg in self.bord.veggs.values():
                tau = physics.finn_kule_vegg_kolisjon_tid(
                    svw=kule.svw,
                    s=kule.s,
                    lx=vegg.lx,
                    ly=vegg.ly,
                    l0=vegg.l0,
                    mu=(self.bord.u_g if kule.s ==
                        sim.glidende else self.bord.u_r),
                    m=kule.m,
                    g=self.g,
                    R=kule.R
                )

                if tau < tau_min:
                    agent_ids = (kule.id, vegg.id)
                    tau_min = tau

        return tau_min, agent_ids

    def setup_test(self, setup='masseskudd'):
        self.stav = Billiardkølle()
        self.kuler = {}

        if setup == 'masseskudd':
            self.bord = Bord()
            self.kuler['stav'] = Kule('stav')
            self.kuler['stav'].svw[0] = [
                self.bord.senter[0], self.bord.B+0.33, 0]

            self.kuler['8'] = Kule('8')
            self.kuler['8'].svw[0] = [self.bord.senter[0], 1.6, 0]

            self.kuler['3'] = Kule('3')
            self.kuler['3'].svw[0] = [self.bord.senter[0]*0.70, 1.6, 0]

            self.stav.skudd(
                kule=self.kuler['stav'],
                V0=2.9,
                phi=80.746,
                theta=80,
                a=0.15,
                b=0.0,
            )
        elif setup == 'veggskudd':
            self.bord = Bord()
            self.kuler['stav'] = Kule('stav')
            self.kuler['stav'].svw[0] = [
                self.bord.senter[0], self.bord.T-0.6, 0]

            self.stav.skudd(
                kule=self.kuler['stav'],
                V0=0.6,
                phi=90,
                a=0.7,
                b=0.7,
                theta=0,
            )
        elif setup == 'åpningsskudd':
            self.bord = Bord()

            self.kuler['1'] = Kule('1')
            self.kuler['2'] = Kule('2')
            self.kuler['3'] = Kule('3')
            self.kuler['4'] = Kule('4')
            self.kuler['5'] = Kule('5')
            self.kuler['6'] = Kule('6')
            self.kuler['7'] = Kule('7')
            self.kuler['8'] = Kule('8')
            self.kuler['9'] = Kule('9')
            self.kuler['10'] = Kule('10')
            self.kuler['11'] = Kule('11')
            self.kuler['12'] = Kule('12')
            self.kuler['13'] = Kule('13')
            self.kuler['14'] = Kule('14')
            self.kuler['15'] = Kule('15')

            c = configurations.FemtenKuleTrekant(list(self.kuler.values()),
                                               spacing_factor=1e-6,
                                               )

            c.arrange()
            c.sentrer_på_bord(self.bord)

            self.kuler['stav'] = Kule('stav')
            self.kuler['stav'].svw[0] = [self.bord.senter[0], self.bord.T*2/8, 0]

            self.stav.skudd_treff_kule(
                kule=self.kuler['stav'],
                obj=self.kuler['1'],
                offset=0,
                V0=8.50001,
                a=0.05,
                b=0.05,
                theta=0,
            )
