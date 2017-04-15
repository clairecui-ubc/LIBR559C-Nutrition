#!flask/bin/python
from app import app
import xml
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

app.run(debug = True)