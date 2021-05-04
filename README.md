# fast-faith-pd-benchmarking
Benchmarking speed and memory for fast calculation of Faith's PD

## Installation
TODO put instructions for how to install everything here


```bash
conda create --yes -n faith-benchmark python=3.6 pip "numpy>=1.15" -c conda-forge
conda activate faith-benchmark
conda install -c conda-forge -c bioconda unifrac=0.10.0 scikit-bio=0.5.4 biom-format scipy seaborn
pip install --upgrade-strategy only-if-needed iow


# try again...
conda create --yes -n faith-benchmark python=3.6 pip "numpy>=1.15" -c conda-forge
conda activate faith-benchmark
conda env update --file requirements.yml 
```

## Get the data
TODO

## Benchmarking
```bash

# Make the subsets of the data
./01.01-make_data_array_all.sh

# Generate a file with commands used for benchmarking
./01.02-generate-commands-file.sh

# Benchmark Skbio Faith's PD
./01.03-par_timeout_skbio.sh

# Benchmark SFPhD
./01.04-par_timeout_sfphd.sh

# Aggregate the results
./01.05-process_results.sh

# Make the benchmarking plot
jupyter notebook
# run through 01.06-create-faiths-pd-benchmarking-figure.ipynb

```

### Generate data of desired size

### Run Benchmarking

### Create benchmarking plot

### Benchmarking large table


## Power Analysis for FINRISK


## Phylogenetic Analysis

### Age distributions

### Empress Visualization

