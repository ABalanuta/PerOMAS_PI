from flask import Flask
import os


app = Flask(__name__)
#this_dir = os.path.dirname(os.path.realpath(__file__))
#print this_dir
#app.config.from_object(this_dir+'/config.py')


from web.app import views
