from flask import Flask
# import xml
# try:
    # import xml.etree.cElementTree as ET
# except ImportError:
    # import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config.from_object('config')

from app import views