import matplotlib.pyplot as plt
from pathlib import Path
from shared import boot_precision, benchmark_names, backend_to_frontend_names

fig, axes = plt.subplots()

data_file = Path("data/performance_data")
data_dict = eval(data_file.read_text())

x = list(data_dict["fhelipe_resnet"][19]["naive"].keys())
x.sort()

def total_area(bitwidth):
    # Just adjust the size of the NTT... probably good enough
    return 472.3 - (5*2.2 + 28.1) + 5 * 2.2 * ((bitwidth / 28.0)**2) + 28.1 * (bitwidth / 28.0)

print(total_area(64) / total_area(28))

def gmean(values):
    result = 1.0
    for val in values:
        result *= val
    return result ** (1.0 / len(values))

bitchopper_gmeans = []
naive_gmeans = []
for bitwidth in x:
    bitchopper_values = []
    naive_values = []
    for boot_prec in boot_precision:
        for name in benchmark_names:
            naive_values.append(((10/9 if (bitwidth < 36) and (name == "fhelipe_logreg" or name == "fhelipe_squeezenet") else 1) * data_dict[name][boot_prec]["naive"][bitwidth]["total"]))
            bitchopper_values.append((data_dict[name][boot_prec]["bitchopper"][bitwidth]["total"]))
    bitchopper_gmeans.append(gmean(bitchopper_values) * total_area(bitwidth))
    naive_gmeans.append(gmean(naive_values) * total_area(bitwidth))

one = bitchopper_gmeans[0]
for i in range(len(naive_gmeans)):
    naive_gmeans[i] /= one
    bitchopper_gmeans[i] /= one


fig, ax = plt.subplots()
print(f"64-bit R-C gmean vs 64-bit BP: " + str(naive_gmeans[-1]/bitchopper_gmeans[-1]))
ax.plot(x, bitchopper_gmeans, linewidth=3, label="BitPacker")
ax.plot(x, naive_gmeans, linewidth=3, label="RNS-CKKS")
ax.set_xlabel("Word size [bits]")
ax.set_ylabel("Normalized Gmean\nExecution Time x Area")
ax.set_ylim(bottom=0)
ax.axhline(y=1, color="gray", linestyle="--")
ax.axhline(y=1.5, color="gray", linestyle="--")
ax.axhline(y=2, color="gray", linestyle="--")
ax.set_yticks([1.0, 1.5, 2.0])

ax.legend()

fig.set_size_inches(6/1.2, 3/1.2)
fig.tight_layout()
fig.savefig("plots/gmean_performance_per_area.pdf")
