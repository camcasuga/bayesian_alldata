# Python code for reading and interpolating the dipole amplitude from BK solver output files.

import numpy as np
import scipy.interpolate as interpolate
import os

class BKDipole:

    def __init__(self, bk_file):
        self.bkfile = bk_file
        self.interpolator, self.Y_range, self.r_range = self.ReadBKDipole()

    def ReadBKDipole(self): # 
        '''
        Reads the dipole amplitude from the given datafile produced running BK solver from 
        
        Returns an interpolator for the dipole: N(Y, r), where r is in GeV^-1, 
        and Y is the evolution rapidity
        '''

        with open(self.bkfile) as f:
            content = f.read().split("###")
        
        content = content[1:]   # gets rid of the stuff at the beginning
        content = [i.split() for i in content] # cleans up lines
        NrY_data = []
        pars = []
        for i in content:

            x = list(map(float, i))
            if len(x) == 1:
                pars.append(x)
            else:
                NrY_data.append(x)

            
        rmYs = np.array(NrY_data).T[1:]     # removes Y values
        N_values = rmYs.T
        Y_values = np.array(NrY_data).T[0]

        pars = np.ndarray.flatten(np.array(pars))
        minr = pars[0]
        mult = pars[1]
        n = int(pars[2])
        r_values = np.array([minr*mult**i for i in range(n)])
        
        
        rgrid=[]
        ygrid=[]
        for y in Y_values:
            for r in r_values:
                rgrid.append(r)
                ygrid.append(y)
        
        self.interpolator = interpolate.CloughTocher2DInterpolator((ygrid, rgrid), N_values.flatten(), rescale=True)
        self.Y_range = (np.min(Y_values), np.max(Y_values))
        self.r_range = (np.min(r_values), np.max(r_values))
        return self.interpolator, self.Y_range, self.r_range

    def N(self, Y, r):
        '''
        Returns the interpolated value of N(Y, r).

        Returns NaN before the initial condition (Y < 0) or if the requested
        evolution rapidity is outside the range  

        Args:
            Y (float): Evolution rapidity
            r (float): Dipole size in GeV^-1
        '''
        r_min, r_max = self.r_range
        Y_min, Y_max = self.Y_range
        
        if r < 0 or Y < 0:
            return np.nan
        
        if Y > Y_max:
            return np.nan
        
        if r > r_max and 0 <= Y <= Y_max: # large r, Y within limits
            return 1.0 
        
        if 0 <= r < r_min and 0 <= Y <= Y_max: # small r, Y within limits
            return 0.0

        N = self.interpolator(Y, r)

        return N

    def Nr(self, Y, r_min = 1e-3, r_max = 1e2, r_points = 50):
        '''
        Returns the dipole amplitude N evaluated at 
        multiple points r [GeV^-1] logarithimically spaced between r_min and r_max.
        '''
        #bk_interpolator = ReadBKDipole(bk_file_dir)
        r_values = np.logspace(np.log10(r_min), np.log10(r_max), r_points)
        N_values = [self.N(Y, r) for r in r_values]
        return r_values, np.array(N_values)
    
class BKDipoleEnsemble:

    def __init__(self, bk_folder):
        '''
        Loads the BKDipoleEnsemble given bk_folder containing multiple BK files.
        '''
        self.bk_interpolators = []
        bk_folder_list = [f for f in os.listdir(bk_folder) if f.endswith('.dat')]
        for i, fname in enumerate(bk_folder_list):
            print(f"Reading file: {i+1}/{len(bk_folder_list)}")
            bk_file = os.path.join(bk_folder, fname)
            self.bk_interpolators.append(BKDipole(bk_file))

    def get_sd(self, values, mean):
        
        ''' Returns standard deviation of values above or below mean '''

        up_sd = np.std(values[values > mean])
        down_sd = np.std(values[values < mean])

        return up_sd, down_sd

    def get_dipole_mean_upsd_downsd(self, rs, Y = np.log(1/1)):
        '''
        Returns the mean and upper/lower standard deviation of func for a given an array of r and rapidity Y.
        '''
        mean = []
        up_sd = []
        down_sd = []

        if len(rs.shape) != 1:
            raise ValueError("r must be a 1D array")
        
        for r in rs:
            val_per_r = []
            for interpolator in self.bk_interpolators:
                val_per_r.append(interpolator.N(Y, r))
                
            val_per_r = np.array(val_per_r)
            val_per_r_mean = np.mean(val_per_r)
            mean.append(val_per_r_mean)
            up_sd_r, down_sd_r = self.get_sd(val_per_r, val_per_r_mean)
            up_sd.append(up_sd_r)
            down_sd.append(down_sd_r)
        
        return np.array(mean), np.array(up_sd), np.array(down_sd)