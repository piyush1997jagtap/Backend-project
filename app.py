from flask import Flask

app = Flask(__name__)

try:
    from Controllers import *
except Exception as e:
    print(e)


