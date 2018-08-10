import sys, os
import numpy as np
import csv

from cntk.ops.functions import load_model
from aml_response  import AMLResponse

# Normalizing value to make inputs between 0.0 and 1.0 range
MAX_VAL = 20000

def init():
    global model
    # Load CNTK model
    model = load_model("model/solar_2000ep.dnn")

def run(request):
    try:
        data = request.get_data(False).decode('utf-8')
        reader = csv.reader(data.splitlines())
        input = []
        for row in reader:
            input.append(np.array([float(x) for x in row], dtype='float32') / MAX_VAL)
        
        res = model.eval({model.arguments[0]: input})
        res = (res[:,0] * MAX_VAL).tolist()
        return res

    except Exception as e:
        return str(e)

