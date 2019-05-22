"""
Plot optimization paths from logs
@author: kkorovin@cs.cmu.edu
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
font = {#'family' : 'normal',
        # 'weight' : 'bold',
        'size'   : 12}
plt.rc('font', **font)


# VIS_DIR = 'experiments/results/visualizations'
VIS_DIR = 'experiments/visualizations'


def plot_paths(name, grouped_paths_list, labels):
    results = []
    for paths_list in grouped_paths_list:
        group = []
        for path in paths_list:
            res = get_list_from_file(path)
            group.append(res)
        results.append(group)

    # preprocessing
    fig = plt.figure(figsize=(15,10))
    ax = fig.add_subplot(1,1,1)

    max_len = max([max([len(res) for res in group])
                    for group in results])

    for i, (group, label) in enumerate(zip(results, labels)):
        for res in group:
            res.extend( [res[-1]] * (max_len - len(res)) )
        avg = np.array(group).mean(axis=0)
        stddev = np.array(group).std(axis=0) / np.sqrt(5)  # SE correction
        plt.plot(range(20, 20 + len(avg)), avg, label=label)
        plt.fill_between(range(20, 20 + len(avg)), avg-stddev, avg+stddev, alpha=0.1)

    # plot eps
    plt.title("QED optimization")
    # plt.ylim(0.8, 1)
    plt.legend()
    plot_path = os.path.join(VIS_DIR, f"{name}.pdf")
    # plt.show()
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    extent.x0 -= 0.5
    extent.y0 -= 0.3
    extent.y1 += 0.7
    plt.savefig(plot_path, bbox_inches=extent, pad_inches=0)
    # plt.savefig(plot_path, format='eps', dpi=1000)

    plt.clf()

def get_list_from_file(path):
    res = []
    with open(path, 'r') as f:
        if path.endswith('exp_log'):
            # Chemist
            for line in f:
                if line.startswith("#"):
                    curr_max = line.split()[3]
                    curr_max = float(curr_max.split("=")[1][:-1])
                    res.append(curr_max)
        elif path.endswith('opt_vals'):
            # Explorer
            line = f.readline()
            res = [float(v) for v in line.split()]
    return res

def format_chem(group):
    return [f"./experiments/final/chemist_exp_dir_{exp_num}/exp_log" for exp_num in group]

def format_rand(group):
    return [f"./experiments/final/rand_exp_dir_{exp_num}/opt_vals" for exp_num in group]


if __name__ == "__main__":
    qed_paths_list = [
    # format_rand(["20190520041204", "20190520041338", "20190520041540", "20190520114502", "20190520115328"]),
    format_rand(["20190521154417", "20190522072706", "20190522072835", "20190522073130", "20190522073258"]),
    format_chem(["20190518132128", "20190518184219", "20190519053538", "20190519172351"]),
    format_chem(["20190518095359", "20190518182118", "20190518182227", "20190520042603"])
            ]

    plogp_paths_list = [
                format_rand(["20190522072622", "20190522072737", "20190522072853", "20190522073012", "20190522073132"]),
                format_chem(["20190519053341", "20190520035241", "20190520051810"]),
                format_chem(["20190520034409", "20190520034422", "20190520041405"])
            ]

    name = "qed_result"
    labels = ["rand", "sim", "dist"]
    plot_paths(name, qed_paths_list, labels)

    # exp_nums = ["20190521154417"]
    # paths_list = [f"./experiments/final/rand_exp_dir_{exp_num}/opt_vals" for exp_num in exp_nums]
    # name = "explorer_qed"
    # plot_paths(name, paths_list)
