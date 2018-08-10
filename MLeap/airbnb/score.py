import sys, os
import json
import re
from aml_response  import AMLResponse
from shutil import copyfile
# Needed for scoring
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *

import urllib.request, json 

'''
Spark driver will not recognize the scoring jar file on initial load.
To solve this issue, we need to alter the Spark config in main.py and restart the Spark process.
'''
def init():
    global model
    # Change contents of main.py
    if not 'mleap-airbnb-assembly-0.0.1.jar' in open('main.py').read():
        with open('main.py') as f:
            lines = f.readlines()

        regex = re.compile("config\.set*")
        idx = [i for i, item in enumerate(lines) if re.search(regex, item)][0]
        lines.insert(idx + 1, '''config.set("spark.jars", "model/mleap-airbnb-assembly-0.0.1.jar")\n''')
        with open('main.py', 'w') as f:
            for l in lines:
                f.write(l)
        # Process will automatically restart
        exit()

    sc = SparkSession.builder.getOrCreate()
    model = sc._jvm.AirbnbScoring
    model.init()    

def run(request):
    try:
        # Score with spark model
        output = model.score(request)
        # Convert to python array
        res = [[prediction for prediction in row] for row in output]
        return res

    except Exception as e:
        return str(e)

