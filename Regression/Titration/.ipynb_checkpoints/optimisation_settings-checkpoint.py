import pandas, numpy

def create_protofit_main_inp(dataset_name, initial_guess, electrostatic_model,SSA=1.0,DV=1.0):
    """
    Writes the protofit_main.inp file for Protofit optimisation settings 
    
    dataset_name: 
        
    initial_guess: xlsx file with initial values used for optimisation of logK_acidic, logK_basic, logC
    
    electrostatic_model: integer to determine which of the following models are employed:
        1 = Guoy-Chapman Double Layer Model (DLM)
        2 = Constant Capacitance Model (CCM)
        3 = Donnan Shell Model (DSM)
        4 = Non-electrostatic adsorption
        
    SSA: specific surface area, m^2/g
    
    DV: Donnan volume, m^3/g
    
    """
    
    inc = 1.0                       # (real) the increment in the starting guess for parameter i;
    imax = 1                        # (int) the number of starting guesses for parameter i;
    
    # BELOW: init(i) (real) the initial starting guess for parameter i.
    
    sites = pandas.read_excel(initial_guess,index_col=0)
    
    site_types = list(sites.index)
    site_str = "\n"
    site_count = 0
    parm_count = 0
    itypes = ""
    
    for site_n in list(sites):
        # Count the number of sites
        if sum(abs(sites[site_n])) != 0:
            site_count += 1
        
        # Determine whether to optimize a paramter based by specifying increments
        for site_type in site_types:
            if sites[site_n][site_type] == 0:
                set_inc = 0.0
            else:
                set_inc = inc
                parm_count += 1
            
            site_str += "%s\t%s\t%s\n" % (str(imax), str(set_inc), sites[site_n][site_type])
        
        # Classify the sites into acidic (0), basic (2), or amphoteric (1) (protofit_main.inp line 16)
        if abs(sites[site_n]['K_basic']) > 0 and abs(sites[site_n]['K_acidic']) > 0:
            itypes += "1 "
        elif abs(sites[site_n]['K_basic']) > 0:
            itypes += "2 "
        else:
            itypes += "0 "
    
    site_count = str(site_count)
        
    
    np = str(parm_count)                          # (int) Number of parameters to optimize
    
    if electrostatic_model == 1:
        line14_input = str(numpy.log10(SSA))
    elif electrostatic_model == 3:
        line14_input = str(numpy.log10(DV))
    else:   
        line14_input = str(1.0)
    
    line14 = " 1\t1.0\t" + line14_input 
    
    imod = str(electrostatic_model) #"4"                      # (int) Adsorption model to be used:
                                    # 1 = Guoy-Chapman Double Layer Model (DLM)
                                    # 2 = Constant Capacitance Model (CCM)
                                    # 3 = Donnan Shell Model (DSM)
                                    # 4 = Non-electrostatic adsorption
                    
    capacitance = "8"               # (real) capacitance value for CCM (Farad / m 2 )
    
    iact = "2"  # (int) Specifies model for calculating activity coefficients
                                    # 1 = Extended Debye-Huckel
                                    # 2 = Davies
                                    # 3 = Truesdell-Jones
                                    # 4 = activity coefficients
                    
    isurfparam = "2"                # Specifies whether a surface parameter (e.g. specific surface area, specific shell volume) should be optimized
                                    # 0 = do not optimize surface parameter
                                    # 1 = optimize surface parameter
                                    # 2 = specify a value (use value for init on line 10)
                    
    iIS = "1"                       # (int) Specifies whether or not to track ionic strength changes. 0 = do not; 1 = do
    
    ipHzpc = "0"                    # (int) specifies whether or not to use pHzpc as a constraint in model optimization
                                    # 0 = do not; 1 = do
        
    pHzpc_obs = "9.0"               # (real) specified pHzpc value used in the optimization
    
    nbest = "16"                    # (int) Number of best-fitting parameter sets to sort and print upon completion of program
    
    nwex = "0"                      # (int) Specifies amount of output displayed to screen by parameter optimization subroutine:
                                    # 0 = no output (recommended)
                                    # 1 = writes copious output indicating progress of optimizing routine (entertaining but not recommended)
    
    icompare = "0"                  # (int) specifies whether or not program will be run in "compare mode”: 
                                    # 0 = “optimization-mode”
                                    # 1 = “simulation-mode:” program will run a simulation of the dataset specified by isetcompare using the parameter values specified in the variable init above.
    
    isetcompare = "1"               # (int) specifies the number of the dataset (in list below line 27) to be used in the simulation
    
    wpar = "1.0"                    # (real) wpar is the error weighting parameter “w”
    
    step1 = "0.1"                     # (real) Specifies the “coarse adjust” step size for adjusting parameters. This value should be about an order of magnitude larger than step2
    
    step2 = "0.01"                   # (real) Specifies the “fine adjust” step size for adjusting parameters. This value determines the precision of your optimized parameters
    
    nsets = "1"                     # (int) Specifies the number of datasets to read. In optimization mode, the parameters will be optimized simultaneously to all datasets read by the program
    
    dat_filenm = "\"/mnt/0E786F10786EF63D/Users/brand/Documents/University/MEng/Project/Bacteria/Regression/Titration/ttrns/" + dataset_name + ".dat\"" # (char) The filenames of each dataset to be read
    
    
    agglomeration = ("\t" +  # 'Agglomerates' all the information specified above into a format that can be written to file protofit_main.inp for optimisation
          np + # line 1
          site_str + # lines 2 - 13
          line14 + "\n" + # line 14
          site_count + "\t! nsites\n" + # line 15
          itypes +   "\t! itype\n" + # line 16
          imod + "\t! imod\n" +  # line 17
          capacitance + "\t! capacitance\n" + # line 18
          iact + "\t! iact\n" + # line 19
          isurfparam + "\t! isurfparam\n" + # line 20
          iIS + "\t! iIS\n" + # line 21
          ipHzpc + " " + pHzpc_obs + "\t! ipHzpc, pHzpc_obs\n" + # line 22
          nbest + "\t! nbest\n" +  # line 23
          nwex + "\t! nwex\n" +  # line 24
          icompare + " " + isetcompare + " " + wpar + "\t! icompare, isetcompare, wpar\n" + # line 25
          step1 + "\t! setp1\n" + # line 26
          step2 + "\t! step2\n" + # line 27
          nsets + "\t! nsets\n" + # line 28
          dat_filenm) # line 29
    
    temp = open('/mnt/0E786F10786EF63D/Users/brand/Documents/University/MEng/Software/protofit_2.1/protofit_main.inp', 'w')
    temp.write(agglomeration) 
    temp.close()