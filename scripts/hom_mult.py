import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path
import math

data_file = Path("data/hom_mult_data")
data_file_64 = Path("data/hom_mult_64_data")
data_dict = eval(data_file.read_text())
data_dict_64 = eval(data_file_64.read_text())

fig, ax = plt.subplots()

x = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
bar_width = 3

def make_bars(data_dict, offset, bitwidth, labels=True, text=""):

    R = x

    rf_nj = [data_dict["rf_nj"][val] / (10.0 ** 9) for val in R]
    ntt_nj = [data_dict["ntt_nj"][val] / (10.0 ** 9) for val in R]
    print(ntt_nj)
    crb_nj = [data_dict["crb_nj"][val] / (10.0 ** 9) for val in R]
    scalar_op_nj = [data_dict["scalar_op_nj"][val] / (10.0 ** 9) for val in R]

    ntt_bottom = rf_nj
    crb_bottom = [rf_nj[val] + ntt_nj[val] for val in range(len(rf_nj))]
    scalar_op_bottom = [rf_nj[val] + ntt_nj[val] + crb_nj[val] for val in range(len(rf_nj))]
    text_bottom = [rf_nj[val] + ntt_nj[val] + crb_nj[val] + scalar_op_nj[val] for val in range(len(rf_nj))]

    if labels:
        ax.bar([val+offset for val in x], rf_nj, width=bar_width, color='r', label="RF")
        ax.bar([val+offset for val in x], ntt_nj, bottom=ntt_bottom, width=bar_width, color='b', label="NTT")
        ax.bar([val+offset for val in x], crb_nj, bottom=crb_bottom, width=bar_width, color='g', label="CRB")
        rect = ax.bar([val+offset for val in x], scalar_op_nj, bottom=scalar_op_bottom, width=bar_width, color='y', label="Element-wise")
        ax.text(x[0]+offset + bar_width / 2.0, text_bottom[0], text, ha="center", va="bottom", rotation=45)
    else:
        ax.bar([val+offset for val in x], rf_nj, width=bar_width, color='r')
        ax.bar([val+offset for val in x], ntt_nj, bottom=ntt_bottom, width=bar_width, color='b')
        ax.bar([val+offset for val in x], crb_nj, bottom=crb_bottom, width=bar_width, color='g')
        rect = ax.bar([val+offset for val in x], scalar_op_nj, bottom=scalar_op_bottom, width=bar_width, color='y')
        ax.text(x[0]+offset + bar_width / 2.0, text_bottom[0], text, ha="center", va="bottom", rotation=45)

make_bars(data_dict, 0, 28, text="")
# make_bars(data_dict_64, +0.55*bar_width, 64, labels=False, text="64-bit")

ax.set_xlabel("Number of residue moduli [R]")
ax.set_ylabel("Energy [mJ]")
ax.set_xticks(x)

fig.set_size_inches(6/1.2, 3/1.2)
fig.tight_layout()
fig.legend(bbox_to_anchor=(0.1, 0.95), loc="upper left", ncol=1)
fig.savefig("plots/hom_mult.pdf")
