two_digit_fudge = 1
boot_precision = [19, 26]
benchmark_names = ["fhelipe_resnet", "fhelipe_squeezenet", "fhelipe_rnn", "fhelipe_logreg"]
backend_to_frontend_names = {"fhelipe_resnet" : "ResNet-20", "fhelipe_logreg": "LogReg", "fhelipe_rnn": "RNN", "fhelipe_squeezenet": "SqueezeNet"}
def gmean(values):
    result = 1.0
    for val in values:
        result *= val
    return result ** (1.0 / len(values))
