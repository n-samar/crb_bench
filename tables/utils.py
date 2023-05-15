import numpy as np

def gmean(values):
    values = list(filter(lambda x: x != "TODO", values))
    return np.array([float(x) for x in values]).prod()**(1.0/len(values))
