import os
import json
from util import safe_dir

def process_dir(input_dir, output_file=None):
    # TODO: sanity check on directory
    file_names = [os.path.join(input_dir, file_) for file_ in os.listdir(input_dir)]

    all_results = [process_results_file(file_) for file_ in file_names]

    if output_file is None:
        output_path = 'results.json'
    else:
        #safe_dir(output_file)
        output_path = os.path.join(output_file)
    
    with open(output_path, 'w') as fp:
        json.dump(all_results, fp)
    

def process_results_file(results_file):
    with open(results_file, 'r') as fp:
        lines = fp.readlines()

    file_name = os.path.basename(results_file)
    # remove .txt
    file_name = file_name[:-4]
    splits = file_name.split('--')
    split_splits = [val.split('-') for val in splits]
    results = {val[0]: val[1] for val in split_splits[:-1]}

    lines = [line.strip() for line in lines]

#    results = {}

    for i in range(6):
        try:
            this_line = lines[0]
            assert 'Command being timed:' not in this_line
            k, v = this_line.split('-', 1)
            results[k] = v
            lines.pop(0)
        except:
            pass

    #try:
    #    results['method'] = lines[0].split('-')[1]
    #except:
    #    results['method'] = 'NA'

    #try:
    #    results['python_time'] = lines[1].split('-')[1]
    #except:
    #    results['python_time'] = 'NA'

#    times = filter(lambda x: len(x) > 0, lines[1].split('  '))
#    for time in times:
#        t, k = time.split(' ')
#        results[k] = t

    for line in lines:
        try:
            k, t = line.split(': ')
            results[k] = t
        except:
            k = line[:5]
            results[k] = line

    return results

