import sys, os
sys.path.append(os.path.join(os.getcwd(), "model"))

import inception
import json
from aml_response  import AMLResponse

def init():
    global node_lookup

    # Creates graph from saved graph_def.pb.
    inception.create_graph('model/classify_image_graph_def.pb')
    node_lookup = inception.NodeLookup('model/imagenet_2012_challenge_label_map_proto.pbtxt',
                                    'model/imagenet_synset_to_human_label_map.txt')

def run(request):
    try:
        input = request.get_data(False)
        count = request.args.get('count')
        
        if count:
            res = inception.run_inference_on_image(node_lookup, input, int(count))
        else:
            res = inception.run_inference_on_image(node_lookup, input)

        return res

    except Exception as e:
        return str(e)
