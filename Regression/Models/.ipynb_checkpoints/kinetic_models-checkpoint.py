import numpy

def pseudo_first(t, parms):
    qe, k1 = parms
    return qe*(1 - numpy.exp(-k1*t))

def two_phase_pfo(t, parms):
    qe_1, qe_2, k1_1, k1_2 = parms
    return qe_1*(1 - numpy.exp(-k1_1*t)) + qe_2*(1 - numpy.exp(-k1_2*t))

def pseudo_second(t, parms):
    qe, k2 = parms
    return (qe**2)*k2*t/(1 + qe*k2*t)

def elovich(t, parms):
    a, b = parms
    return 1/b*numpy.log(1 + a*b*t)

def abt(t, parms):
    qe, ka, kd = parms
    return qe*ka/(ka + kd)*(1 - numpy.exp(-(ka+kd)*t))

def short_crank(t, De_R2):
    return 6*numpy.sqrt(De_R2*t)*(numpy.pi**(-0.5) - 0.5*numpy.sqrt(De_R2*t))

def long_crank(t, De_R2):
    return 1 - 6/numpy.pi**2*numpy.exp(-De_R2*numpy.pi**2*t)

def pw_crank(t, De_R2):
    return numpy.piecewise(t, 
                           [t < 0.8, t >= 0.8], 
                           [lambda t:short_crank(t, De_R2),
                            lambda t:long_crank(t, De_R2)])