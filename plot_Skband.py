import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
from scipy.interpolate import CloughTocher2DInterpolator

colors = ['blue', 'red', 'green', 'orange', 'gray']

def Sk_interp(sk_file):
    """ 
    Should return a 2D interpolator for log S(k) as a function of log k and y 
    Note definition of S(k) = 

    """
    df = pd.read_csv(sk_file, comment='#', sep=' ')
    y = df['y'].values
    log_k = df['log10_k'].values
    log_Sk2 = df['log10_S(k)'].values

    interpolator = CloughTocher2DInterpolator(list(zip(y, log_k)), log_Sk2)
    return interpolator


def main(sk_files_dir, y_vals):

    """
    Returns and plots S(k) * sigma_0/2 with 2 sigma error bands

    """

    interpolators = []
    for i in range(100):
        sk_file = os.path.join(sk_files_dir, f"2Dft_{i}.csv")
        print(f"Reading file: {sk_file}")
        interpolators.append(Sk_interp(sk_file))

    parameter_file = "LO_MVe/posteriorsamples.dat"
    sigma02 = np.loadtxt(parameter_file, usecols=3) # check which column corresponds to the proton transverse area
    k_values = 100
    log_k_grid = np.linspace(-2, 2, k_values)
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    
    j = 0
    for y_val in y_vals:

        mean = np.zeros(k_values)
        up_sd = np.zeros(k_values)
        down_sd = np.zeros(k_values)

        i = 0
        for log_k in log_k_grid:
            log_SK = np.array([10**(interpolators[a](y_val, log_k))*sigma02[a] for a in range(100)])
            mean[i] = np.mean(log_SK)
            lower_region = log_SK < np.mean(log_SK)
            upper_region = log_SK > np.mean(log_SK)
            up_sd[i] = np.std(log_SK[upper_region])
            down_sd[i] = np.std(log_SK[lower_region])
            i += 1

        ax.plot(log_k_grid, mean, label=f'y = {y_val}', color=colors[j])
        ax.fill_between(log_k_grid, mean - 2*down_sd, mean + 2*up_sd, color=colors[j], alpha=0.4)

        j += 1

    ax.legend()
    ax.set_xlabel('log10(k)')
    ax.set_yscale('log')
    ax.set_ylabel('(S(k))*sigma0/2')
    fig.savefig("logsk_fory_proton_sigma02.pdf", dpi=300)

if __name__ == "__main__":

    " Run code as: python3 plot_Skband.py y1 y2 y3, i.e. pass as many rapidities as you want"
    
    y = np.zeros(len(sys.argv)-1)
    for n in range(1, len(sys.argv)):
        y[n-1] = float(sys.argv[n])
    
    sk_files_dir = "LO_MVe/momspace_dipoles/proton"
    main(sk_files_dir, y_vals = y)

