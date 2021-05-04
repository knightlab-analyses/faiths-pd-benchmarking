import itertools
import os
from numpy import random
from util import temporary_seed, safe_dir
import biom
from biom.util import biom_open
import skbio
import bp
from typing import Optional
from scipy import sparse


def random_subset(table, otu_size=None, sample_size=None, seed=None):

    otu_ids = table.ids(axis='observation')
    sample_ids = table.ids(axis='sample')

    # temporary_seed helps make sampling thread-safe
    with temporary_seed(seed):
        if otu_size is not None:
            otu_subset = random.choice(otu_ids, size=otu_size, replace=False)
        else:
            otu_subset = otu_ids

        if sample_size is not None:
            sample_subset = random.choice(sample_ids, size=sample_size,
                                          replace=False)
        else:
            sample_subset = sample_ids

    return otu_subset, sample_subset


def filter_table(table, otu_subset=None, sample_subset=None):
    new_table = table.copy()
    if otu_subset is not None:
        # filter_otus = lambda values, id_, md: \
        #         id_ in otu_subset
        # new_table.filter(filter_otus, axis='observation', inplace=True)
        new_table.filter(ids_to_keep=otu_subset, axis='observation',
                         inplace=True)
    if sample_subset is not None:
        # filter_samples = lambda values, id_, md: \
        #         id_ in sample_subset
        # new_table.filter(filter_samples, axis='sample', inplace=True)
        new_table.filter(ids_to_keep=sample_subset, axis='sample',
                         inplace=True)
    return new_table


def get_random_subtable(table,
                        otu_size,
                        sample_size,
                        seed,
                        density=None):
    """Returns a random sub-table with specified otu and sample sizes


    Parameters
    ----------

    table : biom.Table
        table to subset

    otu_size : int, optional
        number of otus in final table (must be equal or 
        smaller than `table`). All otus are used if None.

    sample_size : int, optional
        number of samples in final table (must be equal or 
        smaller than `table`). All otus are used if None.

    seed : int, optional
        seed for the random generator

    density : float, optional
        if specified, random counts will be added to the
        table to achieve a density of `density`.


    Returns
    -------

    biom.Table
        subset of original table with `otu_size` otus and 
        `sample_size` samples.

    """
    otu_subset, sample_subset = random_subset(table,
                                              otu_size=otu_size,
                                              sample_size=sample_size,
                                              seed=seed)
    filtered_table = filter_table(table,
                                  otu_subset=otu_subset,
                                  sample_subset=sample_subset)

    if density is not None and len(density) > 0:
        filtered_table = add_density(filtered_table, density, seed=seed)

    return filtered_table

def add_density(table, density, format='csr', seed=None):
    """Adds non-zero entries randomly to `table` to 
    achieve a desired density. If the table is alread more dense
    than `density`, do nothing.

    Parameters
    ----------

    table : biom.Table
        A table to add random entries to. Operates in-place 
        on this table.

    density : float
        Desired density of output table

    Returns
    -------

    biom.Table
        A table with density approximately equal to `density`

    """

    density_of_table = table.get_table_density()

    residual_density = density - density_of_table

    if residual_density > 0:
        m, n = table.matrix_data.shape
        new_counts = sparse.random(m, 
                                   n,
                                   density=residual_density,
                                   format=format,
                                   random_state=seed
                                  )

        assert spares.isspmatrix_csr(table.matrix_data)
        new_table_data = table.matrix_data + new_counts

        new_table = Table(new_table_data,
                          table.ids("observation"),
                          table.ids("sample")
                         ) 

        return new_table

    return table


def prep_args(otu_sizes=None, sample_sizes=None, reps=1, densities=None):
    """
    Generates (otu_size, sample_size, density, rep_number, seed) pairs
    """
    if otu_sizes is None:
        otu_sizes = [None]
    if sample_sizes is None:
        sample_sizes = [None]
    if densities is None:
        densities = [None]

    total_subsets = len(densities)*len(otu_sizes)*len(sample_sizes)*reps
    sizes = total_subsets * reps
    size_combs = list(itertools.product(otu_sizes, sample_sizes, densities))
    size_reps = [(*size_comb, i) for i in range(reps) for
                 size_comb in size_combs]
    seeds = range(total_subsets)

    sizes_with_seeds = [(*size_reps[seed], seed) for seed in seeds]
    return sizes_with_seeds


arg_names = ['otu_size', 'sample_size', 'rep', 'seed']


def subset_and_write_table_tree(otu_size: int, 
                                sample_size: int,
                                density: float,
                                rep: int,
                                seed: int, 
                                table: biom.Table,
                                tree: bp.BP,
                                output_dir: str,
                                ) -> None:
    """Given parameters for a single subset, filter the table and tree and
    write to file

    """
    # prepare output info
    file_start = 'otu_size-{}--sample_size-{}--rep-{}--seed-{}--density-{}' \
        .format(otu_size, sample_size, rep, seed, density)
    full_file_start = os.path.join(output_dir, file_start)

    # get subset of table
    table_subset = get_random_subtable(table,
                                       otu_size=otu_size,
                                       sample_size=sample_size,
                                       seed=seed,
                                       density=density)

    table_subset.table_id = file_start

    # write out biom table
    with biom_open(full_file_start + '.biom', 'w') as fp:
        table_subset.to_hdf5(fp, "subset: " + file_start)

    # create a sheared tree based off the table
    otu_ids = table_subset.ids('observation')

    # TODO: change bp_tree to tree
    bp_tree = tree # bp.from_skbio_treenode(tree)

    sheared_bp = bp_tree.shear(set(otu_ids))

    tree_subset = bp.to_skbio_treenode(sheared_bp)

    # tree_subset = tree.shear(otu_ids)

    for node in tree_subset.traverse():
        if node.length is None:
            node.length = 0
    tree_subset.write(full_file_start + '.newick')


def generate_random_tables(table, tree, output_dir, otu_sizes=None,
                           sample_sizes=None, reps=1, densities=None,
                           job=None):

    # TODO use safe_dir to create output_dir if not created
    #safe_dir(output_dir)

    args = prep_args(otu_sizes=otu_sizes, sample_sizes=sample_sizes, reps=reps, densities=densities)

    if job is None:  
            for arg in args:
                subset_and_write_table_tree(*arg, table, tree, output_dir)

    else:
        arg = args[job-1]
        subset_and_write_table_tree(*arg, table, tree, output_dir)

    if (job == 1) or (job is None):
        # write out arguments to file
        args_file = os.path.join(output_dir, 'args.txt')
        with open(args_file, 'w') as fp:
            for arg in args:
                for item in arg:
                    fp.write(str(item) + '\n')
                fp.write('\n')

    return output_dir


if __name__ == '__main__':
    from biom import load_table
    from skbio import TreeNode
    table = load_table('../../trial-unifrac/moving-pictures-downloaded'
                       '/table-dir/feature-table.biom')
    tree = TreeNode.read('../../trial-unifrac/moving-pictures-downloaded'
                         '/tree-dir/tree.nwk')

    generate_random_tables(table, tree, '../data/demo2', otu_sizes=[1, 10],
                           sample_sizes=[1, 10], reps=3)
