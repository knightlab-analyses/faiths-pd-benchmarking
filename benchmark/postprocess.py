import pandas as pd
import os
import json
import numpy as np

def validate_results(output_dir):
    full_data = read_results_directory(output_dir)
    if not metadata_matches(full_data):
        raise AssertionError('Metadata of otu\'s sampled does not match')
    if not metric_matches(full_data):
        raise AssertionError('Metric measurements does not match in all'
                'comparable trials')
    return True

def metadata_matches(data_table):
    gpby = data_table.groupby('seed')
    if set(gpby['sample_ids'].nunique()) != {1}:
        return False
    if set(gpby['otu_ids'].nunique()) != {1}:
        return False
    if set(gpby['num_samples'].nunique()) != {1}:
        return False
    if set(gpby['num_otus'].nunique()) != {1}:
        return False
    return True

def metric_matches(data_table):
    results = data_table.loc[:,['seed', 'results']].sort_values('seed')
    it_rows = results.itertuples()
    first_entry = next(it_rows)
    current_seed = first_entry.seed
    current_results = first_entry.results
    for entry in it_rows:
        next_seed = entry.seed
        next_results = entry.results
        if next_seed==current_seed:
            if not np.allclose(current_results, next_results):
                return False
        current_seed = next_seed
        current_results = next_results
    return True

def read_results_directory(output_dir=os.path.curdir):
    directory_file_names = os.listdir(output_dir)
    data_file_names = filter(lambda name: name[-4:] == 'json', directory_file_names)
    data_dicts = []
    for file_name in data_file_names:
        with open(os.path.join(output_dir, file_name), 'r') as fp:
            content = json.load(fp)
            data_dicts.append(content)
    return pd.DataFrame(data_dicts)

def read_results_table(file_path):
    return pd.read_csv(file_path, sep='\t', index_col=0)

