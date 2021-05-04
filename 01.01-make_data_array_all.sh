#!/bin/bash

conda activate faith-benchmark

for i in {1..70}; do
  ./scripts/make_data_array.sh "$i"
done
