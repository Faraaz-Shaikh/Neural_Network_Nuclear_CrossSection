# Nuclear Cross-Section Modelling

## Setup and Running:
1. Clone the github repo
2. Install `uv` (a modern python package and project manager) on your system.
3. Run `uv sync` - this will install all the relevant packages on your system.
4. Running the code: `uv run main.py` - for now this only sets up the logger.

## Files/Folders and their intents:
- **src/nn_nuclear_xs/**: is the primary folder containing the code
- **data/**: will hold any data for the project - not required to be uploaded to github (depending on the dataset size)
- **logs/**: We are using the `loguru` library for logging. All logs are saved in this folder, appended to the same file.
- **tests/**: Will hold any integration, unit, or functional tests, if written.
- **src/nn_nuclear_xs/config/**: Holds the configuration paramters for the whole project. Putting them all in this folder helps put all the config in one place.
    - The `app_config.py` simply collects all the various config files together.
    - The intention is to have one config file per module - but that is not a strict requirement.
    - The `logs.py` file sets up places where stuff is logged using loguru.
- **src/nn_nuclear_xs/data_handler/**: Will store files for downloading and processing the data.
- **src/nn_nuclear_xs/exploration/**: Often during coding, we need to figure out various things and see how things work or try them out on a scratchpad. This is that scratchpad. The `misc.py` file in this folder is intended to be the main runner for any exploration code. `uv run main.py --misc` runs the `miscellaneous_function` in the file for ease of use.
- **src/nn_nuclear_xs/utils/**: Often, we need helper functions that do not form part of the core logic of the code. All that stuff can go here.
    - The `logger_setup.py` file sets up beautiful logs using rich, and writes logs into the `logs/` folder. Don't need to touch it except to change logging behaviour (like adding/removing third-party logs).

## Contributors
This work is a collaboration between:
1. Faraaz Shaikh
2. Sharanya Ranka
3. Danish Shakeel Mohammad
