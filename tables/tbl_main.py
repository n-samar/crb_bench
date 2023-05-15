from pathlib import Path
from utils import gmean
import math

two_digit_fudge = 1

def two_digits(value):
    return f"{float(-value):.2f}"

def round_me(value):
    return f"{int(math.floor(-value))}"

def formatted_speedup(lhs, rhs):
    return two_digits(float(rhs) / float(lhs))

def cycles_to_ms(cycles):
    return f"{float(cycles) / (10.0**6):.2f}"

def preprocess():
    performance_file = Path("../data/performance_data")
    performance_dict = eval(performance_file.read_text())
    precision_file = Path("../data/precision_data")
    precision_dict = eval(precision_file.read_text())

    result = dict()
    bitwidth = 28
    boot_prec = 19
    benchmarks = {"fhelipe_resnet": "ResNetBP", "fhelipe_rnn": "RnnBP", "fhelipe_logreg": "LogRegBP", "fhelipe_squeezenet": "SqueezeNetBP"}

    gmean_values = []
    for benchmark in benchmarks.keys():
        result[benchmarks[benchmark]] = cycles_to_ms(two_digit_fudge * performance_dict[benchmark][boot_prec]["bitchopper"][bitwidth]["total"])
        result[benchmarks[benchmark][:-2] + "Speedup"] = formatted_speedup(performance_dict[benchmark][boot_prec]["bitchopper"][bitwidth]["total"], performance_dict[benchmark][boot_prec]["naive"][bitwidth]["total"])
        gmean_values.append(result[benchmarks[benchmark][:-2] + "Speedup"])
        result["PrecMed" + benchmarks[benchmark]] = two_digits(precision_dict["condor_" + benchmark + "_28"]["median"])
        result["PrecMed" + benchmarks[benchmark][:-2] + "RC"] = two_digits(precision_dict["condor_" + benchmark]["median"])
        result["PrecWC" + benchmarks[benchmark]] = round_me(precision_dict["condor_" + benchmark + "_28"]["max"])
        result["PrecWC" + benchmarks[benchmark][:-2] + "RC"] = round_me(precision_dict["condor_" + benchmark]["max"])

    result["GmeanSpeedup"] = two_digits(gmean(gmean_values))

    return result

if __name__ == "__main__":
    print(preprocess())
