from scipy import sparse
from scipy.sparse import coo_matrix
import pickle
from biom import load_table
from biom.table import Table
from biom.util import biom_open
import numpy as np

def accumulate_random_choice(n_possible, size, random_state=np.random):
    # indices = set(random_state.choice(n_possible, size=size*10))
    # while(len(indices) < size):
    #     new_indices = random_state.choice(n_possible, size*10)
    #     indices.update(new_indices)
    # indices = list(indices)
    # np.random.shuffle(indices)
    # return indices[:size]
    assert n_possible > size
    chunk_size = n_possible // size
    indices = random_state.choice(chunk_size, size=size)
    start_pos = (chunk_size * np.arange(size)).astype(int)
    random_indices = start_pos + indices
    return random_indices

table = load_table('/home/garmstro/faith_pd/large-data/update-merged/merged.biom')
sparse_mat = table.matrix_data
dims = sparse_mat.shape
m, n = dims
mn = m * n

base_density = sparse_mat.nnz / (sparse_mat.shape[0] * sparse_mat.shape[1])
densities = [0.001, 0.01, 0.01]
densities = [density - base_density for density in densities]


for density in densities:
    k = int(density * m * n)
    print("Starting density {}...".format(density))
    #new_matrix = sparse.random(*dims, format='csr')
    ind = accumulate_random_choice(mn, k)
    j = np.floor(ind * 1. / m).astype(np.int64, copy=False)
    i = (ind - j * m).astype(np.int64, copy=False)
    vals = np.random.rand(k) 
    new_matrix = coo_matrix((vals, (i, j)), shape=(m, n)).asformat('csr', copy=False)
    print("Finished.")
    print("Adding sparse tables...")
    new_matrix = new_matrix + sparse_mat
    print("Finished.")
    print("Making BIOM table...")
    new_table = Table(new_matrix, 
                      table.ids('observation'),
                      table.ids('sample'),
                      table_id="Density {} table".format(density))
    #matrix_file = '/home/garmstro/faith_pd/large-data/ind_density-{}.p'.format(density)
    matrix_file = '/home/garmstro/faith_pd/large-data/large_table_density-{}.biom'.format(density + base_density)
    print("Finished.")
    print("Writing...")
    with biom_open(matrix_file, 'w') as fp:
        new_table.to_hdf5(fp, "density {}".format(density + base_density))
    del new_table
    del new_matrix
    #with open(matrix_file, 'wb') as fp:
    #    pickle.dump(new_matrix, fp)
    print("Finished.")

