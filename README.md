# faiths-pd-benchmarking
Benchmarking speed and memory for fast calculation of Faith's PD

## Installation
The installation of all packages needed for benchmarking requires 
[`conda`](https://conda.io).

```bash
conda create --yes -n faith-benchmark python=3.6 pip "numpy>=1.15" -c conda-forge
conda activate faith-benchmark
conda env update --file requirements.yml 
```

## Benchmarking

### Generate data of desired size
```bash

# Make the subsets of the data
./01.01-make_data_array_all.sh

# Generate a file with commands used for benchmarking
./01.02-generate-commands-file.sh


```

### Run Benchmarking
```bash

# Benchmark Skbio Faith's PD
./01.03-par_timeout_skbio.sh

# Benchmark SFPhD
./01.04-par_timeout_sfphd.sh

# Aggregate the results
./01.05-process_results.sh

```

### Create benchmarking plot
After the above steps have been completed, the benchmarking plot can be 
recreated by running the `01.06-create-faiths-pd-benchmarking-figure.ipynb` 
notebook.

### Benchmarking large table
The `benchmark/time_stacked_faith.py` script can be used with the large 
table with the following command, if the path to table and tree are known.
```bash
python benchmark/time_stacked_faith.py <path to table> <path to tree>
```

## Power Analysis for FINRISK
The results of the power analysis can be recreated with the notebook: 
`02.01-power-analysis-figure.ipynb`

## Phylogenetic Analysis

### Faith's PD  distributions on metagenomics by Age
The distributions of Faith's PD by Age group can recreated with the notebook:
`03.01-plot-alpha-distributions.ipynb`

### Empress Visualization
The Empress visualization can be created with the notebook `03.
02-metagenomic-age-phylog-analysis.ipynb`. Note that a working installation
of [Qiime2](https://qiime2.org/) with
[Empress](https://github.com/biocore/empress) is need to reproduce the 
visualization.
