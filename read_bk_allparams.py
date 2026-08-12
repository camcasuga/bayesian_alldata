import sys
import matplotlib.pyplot as plt
import numpy as np
import dipole

def main(bk_folder, Y):
    """
    Plots N(Y, r), mean and 2 sigma band, for the given rapidity Y 

    Args:
        bk_folder (str): Path to the folder containing all BK files.
        Y (float): Value of rapidity Y.
    """
    rs = np.logspace(-3,2,50)
    n_sigma = 2
    fig, ax = plt.subplots(figsize=(8, 6))
    interpolators = dipole.BKDipoleEnsemble(bk_folder)
    mean, up_sd, down_sd = interpolators.get_dipole_mean_upsd_downsd(rs, Y = Y)
    ax.plot(rs, mean, linestyle='--', color='b', label=f'Y={Y}')
    ax.fill_between(rs, mean + n_sigma*up_sd, mean - n_sigma*down_sd, color='b', alpha=0.3)
    ax.set_xscale('log')
    #ax.set_yscale('log')
    ax.set_xlabel(r'$r$ (GeV$^{-1}$)')
    ax.set_ylabel(r'$N(r)$')
    ax.set_xlim(0.5e-1, 1e2)
    ax.legend()
    fig.savefig(f'Nr_Y_{Y:.2f}_allparams.pdf')
    print(f"Created plot: Nr_Y_{Y:.2f}_allparams.pdf")

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Usage: python read_bk_allparams.py <bk_folder> <Y>")
        sys.exit(1)
    
    bk_folder = sys.argv[1]
    Y = float(sys.argv[2])

    main(bk_folder, Y)

