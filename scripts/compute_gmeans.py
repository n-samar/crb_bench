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

nj_gmean = []
perf_gmean = []
traffic_gmean = []
nj_gmean_64 = []
perf_gmean_64 = []
traffic_gmean_64 = []
for benchmark in data_dict.keys():
    nj_gmean.append((10/9 if benchmark == "fhelipe_logreg" or benchmark == "fhelipe_squeezenet" else 1) * data_dict[benchmark][19]["naive"][28]["nj_total"] / data_dict[benchmark][19]["bitchopper"][28]["nj_total"])
    traffic_gmean.append((10/9 if benchmark == "fhelipe_logreg" or benchmark == "fhelipe_squeezenet" else 1) * (data_dict[benchmark][19]["naive"][28]["loads"] + data_dict[benchmark][19]["naive"][28]["stores"])/ (data_dict[benchmark][19]["bitchopper"][28]["loads"] + data_dict[benchmark][19]["bitchopper"][28]["stores"]))
    perf_gmean.append((10/9 if benchmark == "fhelipe_logreg" or benchmark == "fhelipe_squeezenet" else 1) * data_dict[benchmark][19]["naive"][28]["total"] / data_dict[benchmark][19]["bitchopper"][28]["total"])

    nj_gmean_64.append(data_dict[benchmark][19]["naive"][64]["nj_total"] / data_dict[benchmark][19]["bitchopper"][28]["nj_total"])
    traffic_gmean_64.append((data_dict[benchmark][19]["naive"][64]["loads"] + data_dict[benchmark][19]["naive"][64]["stores"])/ (data_dict[benchmark][19]["bitchopper"][28]["loads"] + data_dict[benchmark][19]["bitchopper"][28]["stores"]))
    perf_gmean_64.append(data_dict[benchmark][19]["naive"][64]["total"] / data_dict[benchmark][19]["bitchopper"][28]["total"])

print(f"traffic gmean vs. 28-bit: {gmean(traffic_gmean):.2f}")
print(f"nj gmean vs. 28-bit: {gmean(nj_gmean):.2f}")
print(f"perf gmean vs. 28-bit: {gmean(perf_gmean):.2f}")
print(f"edp gmean vs. 28-bit: {gmean(perf_gmean) * gmean(nj_gmean):.2f}")
print()
print(f"traffic gmean vs. 64-bit: {gmean(traffic_gmean_64):.2f}")
print(f"nj gmean vs. 64-bit: {gmean(nj_gmean_64):.2f}")
print(f"perf gmean vs. 64-bit: {gmean(perf_gmean_64):.2f}")
print(f"edp gmean vs. 64-bit: {gmean(perf_gmean_64) * gmean(nj_gmean_64):.2f}")
