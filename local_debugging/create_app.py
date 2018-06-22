import sys
sys.path.append('/var/azureml-app/')
import traceback
from app import main
from flask import Flask

def create():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app

if __name__ == "__main__":
    app = create()
    app.run(host='0.0.0.0', port=9090)
