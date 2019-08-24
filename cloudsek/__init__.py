"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)
#app = Flask(__name__, static_url_path='/home/vinoth/Desktop/cloudsek/new/cloudsek001/cloudsek001/static')
#app._static_folder = "'/home/vinoth/Desktop/cloudsek/new/cloudsek001/cloudsek001/static/"

import cloudsek001.views
