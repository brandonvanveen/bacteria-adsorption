import numpy, scipy.optimize, scipy.stats

class Model(object):
    """
    Parameters
    
    equation:    a function from equilibrium_models or kinetic_models
    """
        
    def __init__(self, equation):
        self.equation = equation
        self.parms = numpy.nan
        self.num_of_parms = numpy.nan
        self.r2 = numpy.nan
        self.adj_r2 =  numpy.nan
        self.q_sim = numpy.nan
        self.sse = numpy.nan
        self.aic = numpy.nan
        

    def fit_curve(self, xs, q_exp, parms, bounds, constraints=None):
        
        indeps = xs
        if len(xs) <= 2:
            xs = xs[0]
        else:
            xs = xs
        
        self.parms = parms
        self.num_of_parms = len(parms)
        
        def SSE(p):
            sum_of_squerrors = sum((q_exp - self.equation(indeps, p))**2)
            self.sse = sum_of_squerrors
            return sum_of_squerrors
    
        # Fit parameters
        p = scipy.optimize.minimize(SSE, self.parms, bounds=bounds, constraints=constraints)
        self.parms = p.x
        
        # Simulate
        self.q_sim = self.equation(indeps, self.parms)

        # AICc
        n = len(xs)
        np = self.num_of_parms
        self.aic = n*numpy.log(self.sse/n) + 2*(np + 1) + 2*(np + 1)*(np + 2)/(n - np - 2) 
        
        # Coefficient of determination
        ss_tot = numpy.sum((q_exp - numpy.mean(q_exp))**2)
        self.r2 = 1 - self.sse/ss_tot
        self.adj_r2 = 1 - (n - 1)*(1 - self.r2)/(n - np - 1)
        
        
        # Prediction band calcs
        alpha = 1 - 0.95
        self.Syx = numpy.sqrt(self.sse/(n - 2))
        self.quant = scipy.stats.t.ppf(1 - alpha/2, n - np)
        self.n = n
        
    def simulate(self, xs):
        return self.equation(xs, self.parms)
    
    def prediction_int(self, xs):
        sx = (xs - numpy.mean(xs))**2
        return self.quant*self.Syx*(1 + 1/self.n + sx/numpy.sum(sx))    
         
def P_AICc(AIC_2, AIC_1):
    delta = AIC_2 - AIC_1
    return numpy.exp(-0.5*delta)/(1 + numpy.exp(-0.5*delta))
