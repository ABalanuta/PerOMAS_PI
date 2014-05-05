#!/usr/bin/env python
"""Web server based on Flask"""

__author__ = "Artur Balanuta"
__version__ = "1.0.2"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


from flask import Flask, render_template, flash, redirect, send_from_directory
from time import sleep
from multiprocessing import Process

class WebManager:
	
	app = Flask(__name__)
	#hub = None
	
	def __init__(self, local_hub):
		#hub = local_hub
		self.app.config.update(
			CSRF_ENABLED = True,
			SECRET_KEY = '2c1de198f4d30fa5d342ab60c31eeb308b6de0f063e20efb9322940e3888d51c'
			)
			
	@app.route('/')
	@app.route('/index')
	def index():
		
		#Ambient values
		t = "--"
		h = "--"
		d = "--"
		
		#Users
		u = [
			{ 'author': "Artur", 'body': 'Test post #1' },
			{ 'author': "Joao", 'body': 'Test post #2' }
		]
		
		if False:
			if self.hub.temp_humid:
				t = hub.temp_humid.temp
				h = hub.temp_humid.humid
				d = str(hub.temp_humid.last_update).split(".")[0]
		
			return render_template("index.html",
				title = 'Home',
				temp = t,
				humid = h,
				last_update = d,
				users = u
				)
		else:
			return render_template("index.html",
				title = 'Home',
				temp = 00,
				humid = 00,
				last_update = 0,
				users = u
				)

	@app.route('/settings')
	def settings():
		return render_template("settings.html")
	
	@app.route('/gateway')
	def gateway():
		return render_template("gateway.html")


	def start(self):
		self.app.run(debug = True, host='0.0.0.0', use_reloader=False)
		
#@app.route('/login', methods = ['GET', 'POST'])
#def login():
#    form = LoginForm()
#    
#    if form.validate_on_submit():
#        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
#        print form.openid.data, form.remember_me.data
#        return redirect('/index')
#        
#    return render_template('login.html', 
#        title = 'Sign In',
#        form = form)
 
 
class WebHandler():

	def __init__(self, hub):

		self.hub = hub
		self.web_manager = WebManager(hub)
		self.server = Process(target=self.web_manager.start)

	def start(self):
	 	self.server.start()

	def stop(self):
	 	self.server.terminate()
	 	self.server.join()

if __name__ == "__main__":
	#app
	
	
	
	wh = WebHandler(None)
	wh.start()
	sleep(10)
	wh.stop()
