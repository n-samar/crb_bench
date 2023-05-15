import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

data_file = Path("data/bitchopper_main")
data_dict = eval(data_file.read_text())

naive = data_dict["naive"]
bitchopper = data_dict["bitchopper"]
x = list(naive.keys())
x.sort()

fig, ax = plt.subplots()

ax.set_xlabel("LogScale")
ax.set_ylabel("Execution Time")
ax.plot(x, [int(bitchopper[val]) for val in x], label="BitChopper", linewidth=2.5)
ax.plot(x, [int(naive[val]) for val in x], label="WPRS (Prior Work)", linewidth=2.5)

ax.legend()
fig.set_size_inches(7/1.5, 3.5/1.5)
fig.tight_layout()
fig.savefig("plots/main_figure.pdf")
