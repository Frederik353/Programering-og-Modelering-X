import numpy as np



g = 9.8 # gravitasjons akselerasjon m/s^2
M = 0.567 # vekt billiard kølle
m = 0.170097 # kule masseskudd
R = 0.028575 # kule radius
u_g = 0.2 # glide friksjonskoeffisient
u_r = 0.01 # rulle friksjonskoeffisient
u_sp = 10 * 2/5*R/9 # spinnene friksjonskoeffisient
bord_lengde = 2.54
bord_bredde = 1.27

vegg_bredde = 0.0635
vegg_høyde = 0.64*2*R
bord_kant_bredde = 0.10
bord_merke_størrelse = 0.01

# kule tilstands
stille=0
spinnenende=1
glidende=2
rullende=3

tilstand_dict = {
    0: 'stille',
    1: 'spinnenende',
    2: 'glidende',
    3: 'rullende',
}

toleranse = 1e-12
