## Data from Bayesian fits to HERA data
Posterior samples from [2311.10491](https://arxiv.org/abs/2311.10491), [2506.00487](https://arxiv.org/abs/2506.00487), and [2604.22332](https://arxiv.org/abs/2604.22332). Further contains:
- Coordinate space dipole amplitudes evolved with the leading order running coupling BK, kinematically constrained BK, or full next-to-leading order BK
- Momentum space dipole amplitudes are included in the LO_MVe fit for proton and nuclear (Au) targets
- F2 and FL calculated using code from [paper](https://arxiv.org/abs/2604.09071) and [code](https://zenodo.org/records/19367635)

See official Zenodo repositories for [KCBK fit](https://zenodo.org/records/15552940) and [NLOBK fit](https://zenodo.org/records/19695675).

### Reading coordinate space dipoles

Sample code to print and plot $\mathcal{N}(r)$ amplitdues for a given rapidity: `python3 read_bk.py LO_MVe/bks/1.dat 2` interpolates throught the numerical data of the dipole amplitudes at rapidity $y=2$ from the initial condition obtained in the leading MVe fit to HERA data. 

The code `read_bk_allparams.py` plots the dipole amplitude (mean over posterior samples) and $2\sigma$ band for a given rapidity. 

### Reading momentum space dipoles

Numerical data of the 2-dimensional Fourier transform of dipole amplitudes for different rapidites and $k$ are available for the leading order MVe fit (see LO_MVe/momspace_dipoles). To visualize one can use the `plot_Skband.py` code. Sample code: `python3 plot_Skband.py 2 4` reads from the *.csv datafiles and plots the $\tilde{S}(k)\times \sigma_0/2$ mean over posterior samples and $2\sigma$ band for rapidities $y=2$ and $y=4$. 