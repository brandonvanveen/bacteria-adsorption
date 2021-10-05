"""
Passes input data on to ProtoFit for optimisation of parameters

optimise:    executes terminal command that uses Protofit to optimise parameters

"""

import os, pandas, numpy

def optimise():
    os.chdir('/mnt/0E786F10786EF63D/Users/brand/Documents/University/MEng/Software/protofit_2.1')
    os.system('./protofit.exe')
    
    results = open('/mnt/0E786F10786EF63D/Users/brand/Documents/University/MEng/Software/protofit_2.1/protofit_results.txt', 'r')
    best_fit = results.readlines()[2].split()
    best_fit = [float(best_fit[i]) for i in range(len(best_fit))]
    os.chdir('/mnt/0E786F10786EF63D/Users/brand/Documents/University/MEng/Project/Bacteria/Regression/Titration')
    return best_fit

class Results(object):
    def __init__(self, name, best_fit):
        
        self.name = name
        self.SSE = best_fit[13]
        self.pHzpc = best_fit[14]
        # Site 1
        self.lgK1_1 = best_fit[1]
        self.lgK2_1 = best_fit[2]
        self.lgC_1  = best_fit[3]
        # Site 2
        self.lgK1_2 = best_fit[4]
        self.lgK2_2 = best_fit[5]
        self.lgC_2  = best_fit[6]
        # Site 3
        self.lgK1_3 = best_fit[7]
        self.lgK2_3 = best_fit[8]
        self.lgC_3  = best_fit[9]
        # Site 4
        self.lgK1_4 = best_fit[10]
        self.lgK2_4 = best_fit[11]
        self.lgC_4  = best_fit[12]
        
        self.df = pandas.DataFrame(data={'sites':numpy.nan, 'run_name':self.name,
                                         'lgK1_1':[best_fit[1]], 'lgK2_1':[best_fit[2]], 'lgC_1':[best_fit[3]],
                                         'lgK1_2':[best_fit[4]], 'lgK2_2':[best_fit[5]], 'lgC_2':[best_fit[6]],
                                         'lgK1_3':[best_fit[7]], 'lgK2_3':[best_fit[8]], 'lgC_3':[best_fit[9]],
                                         'lgK1_4':[best_fit[10]],'lgK2_4':[best_fit[11]],'lgC_4':[best_fit[12]],
                                         'SSE':numpy.nan, 'AICc':numpy.nan})
        
        parameter_list = best_fit[1:13]
        number_of_parameters = 0
        for i in parameter_list:
            if abs(i) > 0.0:
                number_of_parameters += 1
        self.np = number_of_parameters
