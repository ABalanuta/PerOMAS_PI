#!/usr/bin/env python
"""Web server based on Flask"""

__author__ = "Artur Balanuta"
__version__ = "1.0.2"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


from flask import Flask, render_template, flash, redirect, send_from_directory
from multiprocessing import Process
from time import sleep


app = Flask(__name__)

#######################################################################################
#    Flusk Routes
#######################################################################################		
@app.route('/')
@app.route('/index')
def index():

	#Ambient values
	actual_temperature = "--"
	actual_humidity = "--"
	last_update = "--"
	actual_luminosity = "--"
	actual_current = "--"

	#Users
	u = [
		{ 'author': "Artur", 'body': 'Test post #1' },
		{ 'author': "Joao", 'body': 'Test post #2' }
	]
	
	if app.config["HUB"]:
		hub = app.config["HUB"]

		if "TEMPERATURE" in hub.keys():
			actual_temperature = hub["TEMPERATURE"].getTemperature()
			actual_humidity = hub["TEMPERATURE"].getHumidity()
			last_update = hub["TEMPERATURE"].getLastUpdate()
			print "WEB", actual_temperature, actual_humidity, last_update

		if "CURRENT" in hub.keys():
			actual_current = hub["CURRENT"].getValue()
			
		if "LUMINOSITY" in hub.keys():
			actual_luminosity = hub["LUMINOSITY"].getValue()			

	return render_template("index.html",
							title = 'Home',
							temp = actual_temperature,
							humid = actual_humidity,
							last_update = last_update,
							lux = actual_luminosity,
							current = actual_current
							)

@app.route('/settings')
def settings():
	return render_template("settings.html")
	
@app.route('/gateway')
def gateway():
	return render_template("gateway.html")




class WebHandler():
	
	def __init__(self, hub):
		app.config["HUB"] = hub
		app.config.update(
			CSRF_ENABLED = True,
			SECRET_KEY = '2c1de198f4d30fa5d342ab60c31eeb308sb6de0f063e20efb9322940e3888d51c'
			)

	def start(self):
		self.server = Process(target=app.run(debug = True, 
											host='0.0.0.0',
											use_reloader=False))
		self.server.start()

	def stop(self):
	 	self.server.terminate()
	 	self.server.join()

if __name__ == "__main__":
	
	wh = WebHandler(None)
	wh.start()
	sleep(10)
	wh.stop()
