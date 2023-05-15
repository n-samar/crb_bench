import matplotlib.pyplot as plt
from pathlib import Path
from shared import boot_precision, benchmark_names, backend_to_frontend_names

fig, axes = plt.subplots()

data_file = Path("data/performance_data")
data_dict = eval(data_file.read_text())

x = list(data_dict["fhelipe_resnet"][19]["naive"].keys())
x.sort()

def gmean(values):
    result = 1.0
    for val in values:
        result *= val
    return result ** (1.0 / len(values))

gmeans = []
maxes = []
mins = []
for bitwidth in x:
    values = []
    for boot_prec in boot_precision:
        for name in benchmark_names:
            values.append((10/9 if bitwidth < 36 and (name == "fhelipe_logreg" or name == "fhelipe_squeezenet") else 1) * data_dict[name][boot_prec]["naive"][bitwidth]["nj_total"] / data_dict[name][boot_prec]["bitchopper"][bitwidth]["nj_total"])
    gmeans.append(gmean(values))
    maxes.append(max(values))
    mins.append(min(values))


fig, ax = plt.subplots()
ax.plot(x, gmeans, linewidth=3, label="Gmean")
ax.plot(x, maxes, linewidth=3, label="Max")
ax.plot(x, mins, linewidth=3, label="Min")
ax.set_xlabel("Word size [bits]")
ax.set_ylabel("RNS-CKKS Energy\nOverhead")
ax.set_ylim(bottom=0)
ax.axhline(y=1, color="gray", linestyle="--")
ax.axhline(y=2, color="gray", linestyle="--")

ax.legend()
fig.set_size_inches(6/1.2, 3/1.2)
fig.tight_layout()
fig.savefig("plots/gmean_energy.pdf")
