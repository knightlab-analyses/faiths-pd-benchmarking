from table import generate_random_tables
from biom import load_table
from skbio import TreeNode
import argparse
import bp

parser = argparse.ArgumentParser()

parser.add_argument('--tree', '-t', dest='tree',
                    help='File name for tree')
parser.add_argument('--table' '-T', dest='table',
                    help='File name for table')
parser.add_argument('--otu-sizes', '-o', dest='otu_sizes',
                    nargs='*', type=int, default=None,
                    help='List of number of OTUS to '\
                                'sample.')
parser.add_argument('--densities', '-e', dest='densities',
                    nargs='*', type=float, default=None,
                    help="List of densities to use")
parser.add_argument('--sample-sizes', '-s', dest='sample_sizes',
                    nargs='*', type=int, default=None,
                    help='List of number of samples to '\
                                'sample.')
parser.add_argument('--reps', '-r', dest='reps', default=1,
                    type=int,
                    help='Number of times to sample each')
parser.add_argument('--output-dir', '-d', dest='output_dir',
                    help="directory to write results to")
parser.add_argument('--job-id', '-j', dest='job_id',
                    type=int, default=None,
                    help="job number for job array") 

args = parser.parse_args()

table = load_table(args.table)
tree = bp.parse_newick(open(args.tree).read())
#tree = TreeNode.read(args.tree)
generate_random_tables(table, tree, args.output_dir, 
                       otu_sizes=args.otu_sizes,
                       densities=args.densities,
                       sample_sizes=args.sample_sizes,
                       reps=args.reps,
                       job=args.job_id)

# '../../trial-unifrac/moving-pictures-downloaded/table-dir/feature-table.biom'
# '../../trial-unifrac/moving-pictures-downloaded/tree-dir/tree.nwk'
