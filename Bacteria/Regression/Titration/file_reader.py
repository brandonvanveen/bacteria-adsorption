import pandas, numpy

class TitrationData(object):
    
    def __init__(self,file, name, init_vol, Cs, adsorbent_mass, Nacid):
        """
        Defines titration experiment according to the following variables:
        
        init_vol: initial solution volume (L)
        Cs: background electrolyte concentration (mol/L)
        adsorbent_mass: mass of adsorbent (g)
        Nacid: normality of acid (eq/L) (note: use a negative value if using a base)
        
        """
        
        self.file = file
        self.name = name
        self.init_vol = init_vol
        self.Cs = Cs
        self.adsorbent_mass = adsorbent_mass
        self.Nacid = Nacid
        self.nob = numpy.nan

        # LIFT DATA FROM RAW INPUT FILE:

        # Read original file
        file = open(self.file, 'rt', encoding='unicode_escape')
        all_lines = file.readlines()
        initiator = 25
        j = initiator
        while all_lines[j][0] != '$':
            j += 1
        terminator = j
        vals = []
        for i in range(initiator, terminator):
            vals.append(all_lines[i].replace('\t', ','))
        file.close()

        # Create temporary file for pH-vol data
        temp = open('temp_files/temp.txt','w')
        temp.write('i,vol,pH,na1,na2,na3\n')
        temp.close()
        temp = open('temp_files/temp.txt','a')
        for i in range(len(vals)):
            temp.write(vals[i])
        temp.close()

        # Weed out unecessary data
        df = pandas.read_csv('temp_files/temp.txt')
        df = df.drop(columns=['i','na1','na2','na3'])
        df = df[['pH','vol']].round(3)
        
        self.df = df
        
    def protofit_formatter(self):

        df = self.df
        df.to_csv('temp_files/temp.txt',sep='\t',index=False,header=False)
        self.nob = len(df)

        # Final file creation
        final = open('ttrns/' + self.name + '.dat','w')
        final.write('# %s\n%s           ! nob\n%s      ! init_vol (L)\n%s          ! Cs (mol/L)\n1.0         ! Z\n298.15      ! T (K)\n%s      ! adsorbent_mass (g)\n140        ! SSA (m^2/g)\n%s      ! Nacid (eq/L)\n' % (self.name,self.nob,self.init_vol,self.Cs,self.adsorbent_mass,self.Nacid))
        final.close()
        final = open('ttrns/' + self.name + '.dat','a')
        table = open('temp_files/temp.txt','r')
        cont = table.read()
        final.write(cont)
        final.close()
                
        
        
        