import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from shared import backend_to_frontend_names, boot_precision, benchmark_names

data_file = Path("data/breakdown_data")
data_dict = eval(data_file.read_text())

def gmean(values):
    result = 1.0
    for val in values:
        result *= val
    return result ** (1.0/len(values))

bar_width = 0.25

nj_gmean = []
perf_gmean = []
traffic_gmean = []
nj_gmean_64 = []
perf_gmean_64 = []
traffic_gmean_64 = []
for benchmark in data_dict.keys():
    for boot_prec in [19, 26]:
        nj_gmean.append((10/9 if benchmark == "fhelipe_logreg" or benchmark == "fhelipe_squeezenet" else 1) * data_dict[benchmark][boot_prec]["naive"][28]["nj_total"] / data_dict[benchmark][boot_prec]["bitchopper"][28]["nj_total"])
        traffic_gmean.append((10/9 if benchmark == "fhelipe_logreg" or benchmark == "fhelipe_squeezenet" else 1) * (data_dict[benchmark][boot_prec]["naive"][28]["loads"] + data_dict[benchmark][boot_prec]["naive"][28]["stores"])/ (data_dict[benchmark][boot_prec]["bitchopper"][28]["loads"] + data_dict[benchmark][boot_prec]["bitchopper"][28]["stores"]))
        perf_gmean.append((10/9 if benchmark == "fhelipe_logreg" or benchmark == "fhelipe_squeezenet" else 1) * data_dict[benchmark][boot_prec]["naive"][28]["total"] / data_dict[benchmark][boot_prec]["bitchopper"][28]["total"])

        nj_gmean_64.append(data_dict[benchmark][boot_prec]["naive"][64]["nj_total"] / data_dict[benchmark][boot_prec]["bitchopper"][28]["nj_total"])
        traffic_gmean_64.append((data_dict[benchmark][boot_prec]["naive"][64]["loads"] + data_dict[benchmark][boot_prec]["naive"][64]["stores"])/ (data_dict[benchmark][boot_prec]["bitchopper"][28]["loads"] + data_dict[benchmark][boot_prec]["bitchopper"][28]["stores"]))
        perf_gmean_64.append(data_dict[benchmark][boot_prec]["naive"][64]["total"] / data_dict[benchmark][boot_prec]["bitchopper"][28]["total"])

result = dict()

result["BitPacker"] = dict()
result["BitPacker"]["Traffic"] = 1
result["BitPacker"]["Energy"] = 1
result["BitPacker"]["Exe. Time"] = 1
result["BitPacker"]["EDP"] = 1

result["RNS-CKKS 28-bit"] = dict()
result["RNS-CKKS 28-bit"]["Traffic"] = gmean(traffic_gmean)
result["RNS-CKKS 28-bit"]["Energy"] = gmean(nj_gmean)
result["RNS-CKKS 28-bit"]["Exe. Time"] = gmean(perf_gmean)
result["RNS-CKKS 28-bit"]["EDP"] = gmean(perf_gmean) * gmean(nj_gmean)

result["RNS-CKKS 64-bit"] = dict()
result["RNS-CKKS 64-bit"]["Traffic"] = gmean(traffic_gmean_64)
result["RNS-CKKS 64-bit"]["Energy"] = gmean(nj_gmean_64)
result["RNS-CKKS 64-bit"]["Exe. Time"] = gmean(perf_gmean_64)
result["RNS-CKKS 64-bit"]["EDP"] = gmean(perf_gmean_64) * gmean(nj_gmean_64)

fig, ax = plt.subplots()

representations = ["BitPacker", "RNS-CKKS 28-bit", "RNS-CKKS 64-bit"]
metrics = ["EDP", "Exe. Time", "Energy", "Traffic"]
for i, rep in enumerate(representations):
    ax.bar([x + (i-1)*1.05*bar_width for x in range(len(metrics))], [result[rep][metr] for metr in metrics], width=bar_width, label=rep)

fig.legend(ncols=3)

print(f"traffic gmean vs. 28-bit: {gmean(traffic_gmean):.2f}")
print(f"nj gmean vs. 28-bit: {gmean(nj_gmean):.2f}")
print(f"perf gmean vs. 28-bit: {gmean(perf_gmean):.2f}")
print(f"edp gmean vs. 28-bit: {gmean(perf_gmean) * gmean(nj_gmean):.2f}")
print()
print(f"traffic gmean vs. 64-bit: {gmean(traffic_gmean_64):.2f}")
print(f"nj gmean vs. 64-bit: {gmean(nj_gmean_64):.2f}")
print(f"perf gmean vs. 64-bit: {gmean(perf_gmean_64):.2f}")
print(f"edp gmean vs. 64-bit: {gmean(perf_gmean_64) * gmean(nj_gmean_64):.2f}")

ax.axhline(y=1, color="gray", linestyle="--")
ax.axhline(y=2, color="gray", linestyle="--")
ax.axhline(y=3, color="gray", linestyle="--")

ax.set_xticks(list(range(len(metrics))), metrics)

fig.set_size_inches(6, 3)
fig.tight_layout()
# fig.savefig("plots/gmean_bars.pdf")
