from skbio.diversity import alpha_diversity
from skbio.tree import TreeNode
import numpy as np
import time
from biom import load_table
import itertools
import pandas as pd
from numpy import random
import json
import os
import multiprocessing
from functools import partial
from util import to_dense, safe_dir
from table import get_random_subtable


def run_faith(counts, otu_ids, tree):
    return list(alpha_diversity('faith_pd', counts, tree=tree, otu_ids=otu_ids).values)

def run_fast_faith(counts, otu_ids, tree):
    return list(alpha_diversity('fast_faith_pd', counts, tree=tree, otu_ids=otu_ids, shear=False).values)

def run_fast_faith_shear(counts, otu_ids, tree):
    return list(alpha_diversity('fast_faith_pd', counts, tree=tree, otu_ids=otu_ids, shear=True).values)

functions = {'faith_pd': run_faith,
             'fast_faith': run_fast_faith,
             'fast_faith_shear': run_fast_faith_shear
            }

def timeit(func, *args, **kwargs):
    t0 = time.time()
    output = func(*args, **kwargs)
    t1 = time.time()
    tot_time = t1-t0
    data = {'time': tot_time, 'results': output}
    return data

def faith_core(table, tree, func_name, otu_size, sample_size, seed=None, results_file=None):
    table_subset = get_random_subtable(table, otu_size, sample_size, seed=seed)
    counts = np.asarray([table_subset.data(i) for i in table_subset.ids()])
    otu_ids = table_subset.ids('observation')
    sample_ids = table_subset.ids('sample')
    func = functions[func_name]
    results = timeit(func, counts, otu_ids, tree)
    results['function'] = func_name
    results['seed'] = seed
    results['otu_ids'] = list(otu_ids)
    results['sample_ids'] = list(sample_ids)
    results['num_otus'] = len(otu_ids)
    results['num_samples'] = len(otu_ids)

    if results_file is not None:
        # write results to file, then pop otu_ids and sample_ids from results to save on space
        with open(results_file, 'w') as fp:
            json.dump(results, fp)

    results.pop('otu_ids')
    results.pop('sample_ids')

    return results

def prep_faith(table, tree, func_name, otu_size, sample_size, seed=None, results_file=None):
    table_subset = get_random_subtable(table, otu_size, sample_size, seed=seed)
    counts = [table_subset.data(i, dense=False) for i in table_subset.ids()]
    otu_ids = table_subset.ids('observation')
    sample_ids = table_subset.ids('sample')
    return counts, otu_ids, sample_ids, tree, func_name, seed, results_file

def pool_faith(counts, otu_ids, sample_ids, tree, func_name, seed, results_file=None):
    func = functions[func_name]
    counts = np.asarray([to_dense(vec) for vec in counts]) 
    results = timeit(func, counts, otu_ids, tree)
    results['function'] = func_name
    results['seed'] = seed
    results['otu_ids'] = list(otu_ids)
    results['sample_ids'] = list(sample_ids)
    results['num_otus'] = len(otu_ids)
    results['num_samples'] = len(otu_ids)

    if results_file is not None:
        # write results to file, then pop otu_ids and sample_ids from results to save on space
        with open(results_file, 'w') as fp:
            json.dump(results, fp)

    results.pop('otu_ids')
    results.pop('sample_ids')

    return results

def apply_faith_func(args):
    return pool_faith(*args)

def apply_args(table, tree, args_list, n_cpus=False):

    if n_cpus==-1:
        apply_faith = lambda other_args: prep_faith(table, tree, *other_args)
        args = map(apply_faith, args_list)
        processes = multiprocessing.Pool()
        results = processes.map(apply_faith_func, args)
    elif n_cpus > 1:
        apply_faith = lambda other_args: prep_faith(table, tree, *other_args)
        args = map(apply_faith, args_list)
        processes = multiprocessing.Pool(n_cpus)
        results = processes.map(apply_faith_func, args)
    elif n_cpus==1:
        def apply_faith(args): return faith_core(table, tree, *args)
        results = map(apply_faith, args_list)
    else:
        raise ValueError("Invalid number of CPUs")

    return results

def prepare_args(func_names, reps, otu_sizes=None, sample_sizes=None, directory=None):
    if otu_sizes is None:
        otu_sizes = [None]
    if sample_sizes is None:
        sample_sizes = [None]

    total_subsets = len(otu_sizes)*len(sample_sizes)*reps
    sizes = total_subsets * reps
    size_combs = list(itertools.product(otu_sizes, sample_sizes))
    size_reps = [size_comb for _ in range(reps) for size_comb in size_combs]
    seeds = range(total_subsets)

    sizes_with_seeds = [(*size_reps[seed], seed) for seed in seeds]

    all_args_but_file = [(func_name, *other_args) for func_name in func_names for other_args in sizes_with_seeds]

    
    file_names = ['_'.join(str(arg) for arg in other_args) + '.json' for other_args in all_args_but_file]

    dir_ = safe_dir(directory) 
    file_names = [os.path.join(dir_, name) for name in file_names]

    all_arguments = [(*other_args, file_names[i]) for i, other_args in enumerate(all_args_but_file)]
    
    return all_arguments


def experiment(table, tree, func_names, reps, otu_sizes=None, sample_sizes=None, directory=None, n_cpus=-1):
    """

    Parameters
    ----------

    sizes: iterable
    
    reps: int

    tree: skbio.TreeNode

    table: biom.Table

    funcs: runs Faith's PD, standardized form (ex. above)
    
    Returns
    -------

    pd.DataFrame of results

    Examples
    --------

    >>> table = biom.load_table('...')
    >>> tree = ...
    >>> experiment(table, tree, ['faith_pd'], 12, otu_sizes=[10, 100])

    """
    args = prepare_args(func_names, reps, otu_sizes, sample_sizes, directory=directory)
    results = apply_args(table, tree, args, n_cpus=n_cpus)
    return pd.DataFrame(results)
    
# TODO: method that reads args from file and applies them (apply_args)

if __name__ == '__main__':

    tree = TreeNode.read('data/gg_13_8_otus/trees/97_otus.tree')

    bt = load_table('data/moving-pictures/67_otu_table.biom')

    print("Adding zero branch lengths")
    for node in tree.traverse():
        if node.length is None:
            node.length = 0

    print("Running experiment...")
    results = experiment(bt,
                         tree,
                         functions.keys(),
                         5,
                         otu_sizes=[10, 100, 1000, 10000, 15000],
                         sample_sizes=[1000],
                         directory='data/output/demo_exp2',
                         n_cpus=-1)
    print("Done.")

    results.to_csv('data/output/demo2_results.txt', sep='\t')

