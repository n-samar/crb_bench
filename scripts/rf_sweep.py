import matplotlib.pyplot as plt
from pathlib import Path
from shared import boot_precision, benchmark_names, backend_to_frontend_names, gmean

fig, axes = plt.subplots()

data_file = Path("data/rf_sweep_data")
data_dict = eval(data_file.read_text())

x = list(data_dict.keys())
x.sort()


gmeans = []
gmeans_rns_ckks = []
for scratchpad_MB in x:
    values = []
    values_rns_ckks = []
    for boot_prec in boot_precision:
        for name in benchmark_names:
            values_rns_ckks.append((10/9 if (name == "fhelipe_logreg" or name == "fhelipe_squeezenet") else 1) * data_dict[scratchpad_MB][name][boot_prec]["naive"][28]["total"])
            values.append(data_dict[scratchpad_MB][name][boot_prec]["bitchopper"][28]["total"])
    gmeans.append(gmean(values))
    gmeans_rns_ckks.append(gmean(values_rns_ckks))

divide_by = gmeans[x.index(256)]

fig, ax = plt.subplots()
ax.plot(x, [val / divide_by for val in gmeans], linewidth=3, label="BitPacker")
ax.plot(x, [val / divide_by for val in gmeans_rns_ckks], linewidth=3, label="RNS-CKKS")
ax.set_xlabel("Scratchpad size [MB]")
ax.set_ylabel("Gmean Execution Time\n(Normalized)")
ax.set_ylim(bottom=0)
ax.axhline(y=1, color="gray", linestyle="--")
ax.axhline(y=2, color="gray", linestyle="--")

ax.legend()
fig.set_size_inches(6/1.2, 3/1.2)
fig.tight_layout()
fig.savefig("plots/rf_sweep.pdf")
