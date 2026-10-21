# Nuclear Cross-Section Modelling

## Setup and Running:
1. Clone the github repo
2. Install `uv` (a modern python package and project manager) on your system.
3. Run `uv sync` - this will install all the relevant packages on your system.
4. Running the code: `uv run main.py` - for now this only sets up the logger.
5. Running tests: `uv run pytest` - for now this only tests the fortran to csv conversion.
6. Processing data: `uv run main.py --proc-data` - for now only does GDR data processing.
7. Miscellaneous function: `uv run main.py --misc`

## Files/Folders and their intents:
- **src/nn_nuclear_xs/**: is the primary folder containing the code
- **data/**: will hold any data for the project - not required to be uploaded to github (depending on the dataset size)
- **logs/**: We are using the `loguru` library for logging. All logs are saved in this folder, appended to the same file.
- **tests/**: Will hold any integration, unit, or functional tests, if written.
- **src/nn_nuclear_xs/config/**: Holds the configuration paramters for the whole project. Putting them all in this folder helps put all the config in one place.
    - The `app_config.py` simply collects all the various config files together.
    - The intention is to have one config file per module - but that is not a strict requirement.
    - The `logs.py` file sets up places where stuff is logged using loguru.
    - `data_handler.py`: Various configurations for processing the GDR data (for now, in general it is generic for all the data) - like the default fortran format, the url, etc.
- **src/nn_nuclear_xs/data_handler/**: Contains files for downloading and converting the data into a usable format (often csv).
    - `fetch_data.py`: for now it only extracts the GDR data since automated download of GDR data is not allowed. 
    - `fortran_to_csv.py`: it converts from the provided fortran format (for GDR data) into csv format.
    - `process_data.py`: It is intended to contain all the processing code. For now it only converts all the various GDR .dat files into .csv.
- **src/nn_nuclear_xs/exploration/**: Often during coding, we need to figure out various things and see how things work or try them out on a scratchpad. This is that scratchpad. The `misc.py` file in this folder is intended to be the main runner for any exploration code. `uv run main.py --misc` runs the `miscellaneous_function` in the file for ease of use.
- **src/nn_nuclear_xs/utils/**: Often, we need helper functions that do not form part of the core logic of the code. All that stuff can go here.
    - The `logger_setup.py` file sets up beautiful logs using rich, and writes logs into the `logs/` folder. Don't need to touch it except to change logging behaviour (like adding/removing third-party logs).

## Attributes:
- These attributes are from Faraaz's datasets
- TODO: This section is for reference only, should be removed before finalisation
Enhanced Generalized Superfluid Model (EGSM): Energy_MeV,Z1,N1,beta2,Z2,N2,Er1,Wr1,S1,CSp1,Qn,Shell,a_exp,Cross_Section_mb,A1
Constant-Temperature Model: Z1,N1,A1,Z2,N2,A2,Energy_MeV,Cross_Section_mb,I0,Bn,D0,Nlow,Ulow,Ntop,Utop,dW,gamma,ainf,pairing,Ematch,E0,T,Er1,Wr1,S1,S,CSp1
Back Shifted Fermi Gas (BSFG): Z1,N1,A1,Z2,N2,A2,Energy_MeV,Cross_Section_mb,Er1,Wr1,S1,S,CSp1,I0,Bn,D0,Nlow,Ulow,Ntop,Utop,dW,gamma,ainf,pairing

BSFG from RIPL level-densities-bfmeff.csv:
Z      :  atomic number of the compound nucleus
A      :  mass number of the compound nucleus
El     :  element symbol of the compound nucleus
Io     :  spin of the ground state of the target nucleus
Bn     :  neutron binding energy of the compound nucleus in MeV
Do     :  evaluated average resonance spacing in eV
Derr   :  uncertainty of the resonance spacing in eV
Nlow   :  lowest level used for the fit
Ulow   :  Excitation energy of the level Nlow in MeV
Ntop   :  highest level used for the fit
Utop   :  Excitation energy of the level Ntop in MeV
dW     :  Shell correction energy used in the Ignatyuk formula in MeV
gamma  :  Damping parameter of the Ignatyuk formula
ainf   :  asymptotic level density parameter in 1/MeV
aerr   :  uncertainty of the asymptotic level density parameter in 1/MeV
pairing:  effective energy shift in MeV

## Dataset sources
- TODO: This section is for reference only, should be removed before finalisation
- This is the data originally present in Faraaz's repo
1. Back-Shifted Fermi Gas Model (BSFG) [level-densities-bfmeff.csv](javascript:openpopbig('densities/level-densities-bfmeff.dat')) on [this](https://www-nds.iaea.org/RIPL-3/) page.
2. Gilbert-Cameron Model [level-densities-ctmeff.dat](javascript:openpopbig('densities/level-densities-ctmeff.dat')) on [this](https://www-nds.iaea.org/RIPL-3/) page.
3. Enhanced Generalized Superfluid Model (EGSM) [level-densities-egsm.dat](https://www-nds.iaea.org/RIPL-3/densities/level-densities-egsm.dat) on [this](https://www-nds.iaea.org/RIPL-3/) page.
4. GDR Parameters: [gdr-parameters...](https://www-nds.iaea.org/PSFdatabase/atlas/gdr) - the 8980 isotopes one - manual download only

## Contributors
This work is a collaboration between:
1. Faraaz Shaikh
2. Sharanya Ranka
3. Danish Shakeel Mohammad
