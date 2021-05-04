import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def read_results_table(file_path):
    return pd.read_csv(file_path, sep='\t', index_col=0)

def speed_lineplot(results_table, *args, **kwargs):
    plot = sns.lineplot(x='num_otus',
    #plot = sns.pointplot(x='num_otus',
                 y='time',
                 hue='function',
                 data=results_table,
                 markers=True,
                 *args, **kwargs)
    plot.set(xlabel="Number of OTUs", ylabel="Time (s)") 
     
def timeplot_from_file(file_path, *args, **kwargs):
    results = read_results_table(file_path)
    return speed_lineplot(results, *args, **kwargs)

if __name__ == "__main__":

    fig, ax = plt.subplots()
    timeplot_from_file('data/output/demo2_results.txt', ax=ax)
    plt.xscale('log')
    plt.show()

