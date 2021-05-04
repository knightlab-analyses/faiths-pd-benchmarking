import process_results
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input-dir', '-i', dest='input_dir')
parser.add_argument('--output-file', '-o',
                    dest='output_file',
                    default=None)

args = parser.parse_args()

process_results.process_dir(args.input_dir, args.output_file)
