import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from shared import backend_to_frontend_names, boot_precision, benchmark_names, gmean

font = {'size'   : 12}

matplotlib.rc('font', **font)

def bar_plot(fig, ax, data_dict, bar_names, start, label, color, no_label=False, text=True):

    num_bars = len(list(data_dict.keys()))
    bar_width = 0.25
    sep_coeff = 0.55
    blue_bars =[data_dict[bar_name]["bitchopper"]["total"] for bar_name in bar_names]
    if no_label:
        ax.bar([x+start-sep_coeff*bar_width for x in range(len(bar_names))], blue_bars, width=bar_width, color='C0')
    else:
        ax.bar([x+start-sep_coeff*bar_width for x in range(len(bar_names))], blue_bars, width=bar_width, color='C0', label="BitPacker")

    blue_bars = [data_dict[bar_name]["naive_28"]["total"] for bar_name in bar_names]
    if no_label:
        rect = ax.bar([x+start+sep_coeff*bar_width for x in range(len(bar_names))], blue_bars, width=bar_width, color='C1')
    else:
        rect = ax.bar([x+start+sep_coeff*bar_width for x in range(len(bar_names))], blue_bars, width=bar_width, color='C1', label="RNS-CKKS")

def cross_product_names(types, programs):
    result = []
    for t in types:
        for program in programs:
             result.append((f"{t}_{program}", t, program))
    return result

relevant_programs = ["resnet", "logreg", "rnn"]
relevant_types = ["fhelipe", "manual", "chet"]
tick_name_dict = {"resnet": "ResNet-20", "logreg": "LogReg", "rnn": "RNN", "squeezenet": "SqueezeNet"}
label_name_dict = {"fhelipe": "Fhelipe", "manual": "Manual", "chet": "CHET+"}

def create_bar_plot_dict(data_dict):

    result = dict()

    total_gmean_bp = []
    total_gmean_28 = []

    for boot_prec in boot_precision:
        result[boot_prec] = dict()
        for key in data_dict.keys():
                print(key)
                print(list(data_dict[key][boot_prec]["bitchopper"][28]))
                result[boot_prec][backend_to_frontend_names[key]] = dict()
                result[boot_prec][backend_to_frontend_names[key]]["bitchopper"] = dict()
                divisor = data_dict[key][boot_prec]["bitchopper"][28]["total"]
                result[boot_prec][backend_to_frontend_names[key]]["bitchopper"]["total"] = data_dict[key][boot_prec]["bitchopper"][28]["total"] / divisor

                result[boot_prec][backend_to_frontend_names[key]]["naive_28"] = dict()
                result[boot_prec][backend_to_frontend_names[key]]["naive_28"]["total"] = data_dict[key][boot_prec]["naive"][28]["total"] / divisor * (10/9 if key == "fhelipe_logreg" or key == "fhelipe_squeezenet" else 1)

                result[boot_prec][backend_to_frontend_names[key]]["naive_64"] = dict()
                result[boot_prec][backend_to_frontend_names[key]]["naive_64"]["total"] = data_dict[key][boot_prec]["naive"][64]["total"] / divisor

                total_gmean_bp.append(result[boot_prec][backend_to_frontend_names[key]]["bitchopper"]["total"])

                total_gmean_28.append(result[boot_prec][backend_to_frontend_names[key]]["naive_28"]["total"])

        result["gmean"] = dict()
        result["gmean"]["bitchopper"] = dict()
        result["gmean"]["naive_28"] = dict()
        result["gmean"]["bitchopper"]["total"] = gmean(total_gmean_bp)
        result["gmean"]["naive_28"]["total"] = gmean(total_gmean_28)

    return result


data_file = Path("data/breakdown_data")
data_dict = eval(data_file.read_text())



# set width of bar
fig, ax = plt.subplots()

bar_plot_dict = create_bar_plot_dict(data_dict)

print(bar_plot_dict)

boot_prec_to_color = {19: "blue", 26: "red"}
frontend_names = [backend_to_frontend_names[key] for key in benchmark_names]
for i, boot_prec in enumerate(boot_precision):
    bar_plot(fig, ax, bar_plot_dict[boot_prec], frontend_names, i*len(frontend_names), f"{boot_prec}-bit Bootstrap", boot_prec_to_color[boot_prec], no_label=i, text=(boot_prec==19))

bar_plot(fig, ax, bar_plot_dict, ["gmean"], 2*len(frontend_names), f"{boot_prec}-bit Bootstrap", boot_prec_to_color[boot_prec], no_label=True, text=False)

ax.set_xticks([x for x in range(1 + len(boot_precision) * len(frontend_names))], [x + " (BS19)" for x in frontend_names] + [x + " (BS26)" for x in frontend_names] + ["gmean"], rotation=30, ha="right")
ax.set_ylim((0, 2))
ax.set_yticks([1, 1.5, 2])

ax.set_ylabel("Normalized\nExecution Time")
ax.axhline(y=1, color="gray", linestyle="--")
ax.axhline(y=1.5, color="gray", linestyle="--")
fig.set_size_inches(6, 3)
fig.legend(ncols=2)
fig.tight_layout()
fig.savefig("plots/perf_main.pdf")
