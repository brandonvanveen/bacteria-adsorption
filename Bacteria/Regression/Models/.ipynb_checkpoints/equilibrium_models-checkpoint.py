import numpy

def langmuir(Ce, parms):
    qmax, Kl = parms
    return qmax*Kl*Ce/(1 + Kl*Ce)

def mod_lang(pH, parms): #solves for qmax(pH)
    q0, qinf, ke = parms
    return q0*numpy.exp(ke*pH)/(1 - q0/qinf*(1 - numpy.exp(ke*pH)))

def two_surf_lang(Ce, parms):
    qmax_1, Kl_1, qmax_2, Kl_2 = parms
    return qmax_1*Kl_1*Ce/(1 + Kl_1*Ce) + qmax_2*Kl_2*Ce/(1 + Kl_2*Ce)

def freundlich(Ce, parms):
    Kf, alpha = parms
    return Kf*Ce**alpha

def sips(Ce, parms):
    qmax, Ks, s = parms
    return qmax*Ks*(Ce**s)/(1 + Ks*(Ce**s))

def mod_sips(pH, parms): #solves for Ks(pH)
    M1, M2 = parms
    return numpy.exp(M1*pH + M2)

def temkin(indeps, parms):
    Ce, T = indeps
    bT, AT = parms
    R = 8.314 # J/mol/K
    return R*T/bT*numpy.log(AT*Ce)
    
def dubrad(indeps, parms):
    Ce, T = indeps
    qmax, Kdr = parms
    R = 8.314 #J/mol/K
    eps = R*T*numpy.log(1 + 1/Ce)
    return qmax*numpy.exp(-Kdr*eps**2)

def thermodynamics(indeps, parms):
    Ce, T, qe = indeps
    delG, delH, delS = parms
    Kc = qe/Ce
    R = 8.314 #J/mol/K
    return -delH/R/T + delS/R
