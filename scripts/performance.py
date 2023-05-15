import matplotlib.pyplot as plt
from pathlib import Path
from shared import boot_precision, benchmark_names, backend_to_frontend_names, two_digit_fudge

def plot_me(ax, boot_prec, name):
    ax.set_xlabel("Word size [bits]")
    ax.set_ylabel("Execution Time [ms]")
    ax.set_title(backend_to_frontend_names[name] + f" (BS{boot_prec})")

    x = list(data_dict[name][boot_prec]["naive"].keys())
    x.sort()
    ax.plot(x, [two_digit_fudge * data_dict[name][boot_prec]["bitchopper"][val]["total"] / 1000000 for val in x], label="BitPacker", linewidth=3)
    ax.plot(x, [two_digit_fudge * (10/9 if val < 36 and (name == "fhelipe_logreg" or name == "fhelipe_squeezenet") else 1) * data_dict[name][boot_prec]["naive"][val]["total"] / 1000000 for val in x], label="RNS-CKKS", linewidth=3)
    ax.set_ylim(bottom=0)
    ax.legend(loc="lower left")

fig, axes = plt.subplots(nrows=2, ncols=4)

data_file = Path("data/performance_data")
data_dict = eval(data_file.read_text())

for i, boot_prec in enumerate(boot_precision):
    for j, name in enumerate(benchmark_names):
        plot_me(axes[i][j], boot_prec, name)

fig.set_size_inches(12, 6)
fig.tight_layout()
fig.savefig("plots/performance.pdf")
