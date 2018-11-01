import sys, os
sys.path.append(os.path.join(os.getcwd(), "model"))

# If model was deployed from Windows, then libdarknet.so would not have eXecute file attribute set
os.chmod('model/libdarknet.so', 0o777)

import darknet as dn
import json
from aml_response  import AMLResponse

def init():
    global net
    global meta

    #dn.set_gpu(0)
    net = dn.load_net(b"model/yolov3.cfg", b"model/yolov3.weights", 0)
    meta = dn.load_meta(b"model/coco.data")

def run(request):
    try:
        input = request.get_data(False)

        # Darknet only has file-based APIs for reading images, so we have to write->read files.
        # If you are replacing scoring engine and it supports getting data from memory, then use `input` directly.
        fileIn = 'image.in'
        fileOut = 'image.out'
        with open(fileIn, "wb") as file:
            file.write(input)

        returnImage = request.args.get('output') == 'image'

        res = dn.detect(net, meta, fileIn.encode(), fileOut.encode() if returnImage else None)
        os.remove(fileIn)

        if returnImage:
            fileOut += '.jpg'
            with open(fileOut, "rb") as file:
                outBytes = file.read()

            os.remove(fileOut)

            resp = AMLResponse(outBytes, 200, json_str=False)
            resp.headers['Content-Type'] = 'image/png';
            return resp

        else:
            return res

    except Exception as e:
        return str(e)
