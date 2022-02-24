## Break the Loop: Gender Imbalance in Music Recommenders

This repository contains the code to reproduce the results of the paper entitled "Break the Loop: Gender Imbalance in Music Recommenders", by Andres Ferraro, Xavier Serra, and Christine Bauer.

## Instructions

**Step 1**

For the purpose of the course, I've already added the data needed to the `data/`-folder (otherwise you'd need to download a 42GB file).
The file `data/raw/LFM-1b/LFM-1b_LEs.txt` now only contains 50.000 lines as opposed to the original 1.088.161.692 lines (hence the '1b' in the filename).

### OPTIONAL: start virtual environment for python3.10

    # Make sure you have a working version of python3.10 installed
    # Create virtual env with venv
    pip install virtualenv
    python3.10 -m venv python3.10-env

    # Activate
    source python3.10-env/bin/activate

### Install requirements

Install dependencies specified in requirements.txt

    # With pip
    pip install -r requirements.txt

Troubleshooting for MacOS 11 and up
* Make sure your Xcode installation is up to date
* https://github.com/scipy/scipy/issues/13409
* https://stackoverflow.com/questions/65825346/pip-install-pandas-results-in-error-python3-8-pycharm-apple-silicon

**Step 2**

Before starting to generate recommendations the data has to be processed and formatted.
Run the following commands from the base directory of the repository: 

 - `python src/generate_mtrx.py` : Generate matrix for artists using the LFM-1b dataset

**Warning: Stop here if you're reproducing the process for the course**

Everything below is not yet modified to be reproducible without needing the full data set.

 - `python src/generate_mtrx_360k.py`: Generate matrix for artists using LFM-360k dataset
 - `python src/generate_mtrx_tracks.py`: Generate matrix with tracks using LFM-1b dataset

**Step 3**

To run the first experiment (generate artist recommendations) the following scripts must be executed:

 - `python src/model_predict.py` : Generate recommendations for artists using the LFM-1b dataset
 - `python src/model_predict_360k.py`: Generate artist recommendations using the LFM-360k dataset

To run the second experiment (generate track recommendations) the following script must be executed:

 - `python src/model_predict_tracks.py`: Genrate track recommendations using the LFM-1b dataset

**Step 4**

Finally, to run the last experiment (simulations) the following script must be executed:

 - `python model_simulate_artist.py -l 0`: Generate simulation with artist recommendations using LFM-1b dataset indicating the value of lambda

## Cite

Andrés Ferraro, Xavier Serra, and Christine Bauer (2021). Break the Loop: Gender Imbalance in Music Recommenders. In Proceedings of the 2021 ACM SIGIR Conference on Human Information Interaction and Retrieval (CHIIR ’21), March 14–19, 2021, Canberra, ACT, Australia. ACM, New York, NY, USA. https://doi.org/10.1145/3406522.3446033


## Project organization
- PG = project-generated
- HW = human-writable
- RO = read only
```
.
├── .gitignore
├── CITATION.md
├── LICENSE.md
├── README.md
├── requirements.txt
├── bin                <- Compiled and external code, ignored by git (PG)
│   └── external       <- Any external source code, ignored by git (RO)
├── config             <- Configuration files (HW)
├── data               <- All project data, ignored by git
│   ├── processed      <- The final, canonical data sets for modeling. (PG)
│   ├── raw            <- The original, immutable data dump. (RO)
│   └── temp           <- Intermediate data that has been transformed. (PG)
├── docs               <- Documentation notebook for users (HW)
│   ├── manuscript     <- Manuscript source, e.g., LaTeX, Markdown, etc. (HW)
│   └── reports        <- Other project reports and notebooks (e.g. Jupyter, .Rmd) (HW)
├── results
│   ├── figures        <- Figures for the manuscript or reports (PG)
│   └── output         <- Other output for the manuscript or reports (PG)
└── src                <- Source code for this project (HW)

```


## License

This project is licensed under the terms of the [MIT License](/LICENSE.md)
