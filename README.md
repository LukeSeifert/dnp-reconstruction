# MoSDeN
Molten Salt Delayed Neutron (MoSDeN) is a tool used for reconstruction of 
delayed neutron precursor groups in molten salt reactors.

## History
This tool had a previous version in this repository accessible with 
git hash `b56528a4`.
That version has a publication associated with it, given here:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14888551.svg)](https://doi.org/10.5281/zenodo.14888551)

## Functionality
MoSDeN operates in three distinct stages: preprocessing, processing, and 
post-processing.
Preprocessing loads in data and builds necessary files for processing.
Processing runs the main bulk of the calculations for generating parameters.
Post-processing handles figure generation and data analysis.

### Preprocessing
Preprocessing should be run to generate any data needed (if it does not already 
exist as processed data).
This data is dependent on the energy of the irradiating neutrons as well as the 
fissile nuclide target.

The exact organization of raw, unprocessed data is flexible, with some notable 
exceptions:
- OpenMC chain files to be should all be in a subdirectory labeled with 
"omcchain" (see `preprocessing.py` for all keywords)
- ENDF NFY data should all be in a subdirectory labeled `nfy`
- ENDF NFY files should be named "nfy-<ZZZ>_<ID>_<AAA>.csv", so 235U would be 
`nfy-092_U_235.csv`.
- IAEA beta-delayed neutron emission data should be in a directory `iaea` and 
be called `eval.csv` (default when downloading data).

Data can be collected from different sources:
- [OpenMC depletion chains](https://openmc.org/depletion-chains/): these give 
half-lives and independent fission yields (linearly interpolated 
energy dependence)
- [ENDF data](https://www.nndc.bnl.gov/endf-releases/): these give (currently) 
cumulative fission yields (with energy dependence based on nearest energy)
- [IAEA data](https://www-nds.iaea.org/beta-delayed-neutron/database.html): 
these give emission probabilities and half-lives

### Processing
Processing consists of three steps:
1. Generate concentrations (or collect fission yield data).
2. Generate the delayed neutron count rate.
3. Fit a set of delayed neutron precursor group parameters that best fit the 
count rate.

The generation of concentrations varies based on the model used.
The simplest model is the 0D scaled model, and uses cumulative fission yields.
The concentration of each DNP is calculated as the cumulative fission yield over 
the decay constant of that DNP.
The 0D flow model (not implemented as of 2025-09-02) uses OpenMC to incorporate 
decay chains and parasitic absorption effects, offering a better model of 
the DNP concentrations at each point during the irradiation and subsequent 
decay.

The generation of the delayed neutron count rate and non-linear least squares
fitting methods do not change between different models.

### Postprocessing
Postprocessing handles plotting and data analysis from the processed results, 
including analysis of each step.

## Using the tool from source
Download the repository from GitHub.
The environment will also to be created by running 
`conda env create -f environment.yml`.
This should be followed with `conda activate mosdenv` to activate 
the environment.
Run `pip install -e .` to make the package available to use on the command line 
as `mosden` in the `mosdenv` environment.
Download the data used in tests by running `bash download_data.sh`.
Check that tests pass by running `pytest` or `pytest -m "not slow"` for the 
faster version.
Use `mosden -a <input.json>` to do a full run, `mosden -pre <input.json>` for 
preprocessing, or `mosden -post <input.json>` for post-processing.

### Input file
The input file contains the majority of parameters of interest.
The command line arguments describe what stage of MoSDeN to run (preprocessing, 
processing, or post-processing), while the input file describes what should 
happen during each of those stages.
The `default.py` and input files in `examples` can be used as a guide for 
formatting and what parameters can be included.

#### Log level
One of the parameters is the log level, which can be useful for collecting 
additional information about the simulation.
This can be configured in the input file, but the default level of 20 is also 
the suggested level for collecting useful information while not overcollecting 
various debug outputs.

- [<10] is the debug level
- [<20] is the info level (This is the suggested level)
- [<30] is the warning level
- [<40] is the error level
- [<50] is the critical level