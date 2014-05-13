#!/usr/bin/env python
"""Web server based on Flask"""

__author__ = "Artur Balanuta"
__version__ = "1.0.2"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


from flask import Flask, request, render_template, flash, redirect, send_from_directory, url_for
from flask.ext.cache import Cache, make_template_fragment_key
from flask.ext.compress import Compress
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, validators
from wtforms.validators import Required

from multiprocessing import Process
from threading import Thread
from time import sleep

from UserManager import UserManager 

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app,config={'CACHE_TYPE': 'simple'})
Compress(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



#############
# From
############
class LoginForm(Form):
    username = TextField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.Length(min=8, max=100)])
    remember_me = BooleanField('remember_me', default = False)

class RegisterForm(Form):
    username = TextField('username',[
    	validators.Required(),
    	validators.Length(min=4, max=25)
    ])

    password = PasswordField('New Password', [
        validators.Required(),
        validators.Length(min=8, max=100),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])

    password_confirm = PasswordField('password_confirm')
    
    key = PasswordField('password',[
    	validators.Required(),
    	validators.Length(min=4)
    ])





#######################################################################################
#    Flask Routes
#######################################################################################		
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

	if request.method == 'POST':
		process_index_post()


	#Ambient values
	actual_temperature = "--"
	actual_humidity = "--"
	last_update = "--"
	actual_luminosity = "--"
	actual_current = "--"
	ac_speed = "--"
	present_devices = None
	
	if app.config["HUB"]:
		hub = app.config["HUB"]

		if "TEMPERATURE" in hub.keys():
			actual_temperature = round(hub["TEMPERATURE"].getTemperature(), 1)
			actual_humidity = round(hub["TEMPERATURE"].getHumidity(), 1)
			last_update = hub["TEMPERATURE"].getLastUpdate()

		if "CURRENT" in hub.keys():
			actual_current = hub["CURRENT"].getValue()
			
		if "LUMINOSITY" in hub.keys():
			actual_luminosity = hub["LUMINOSITY"].getValue()			

		if "RELAY" in hub.keys():	
			ac_speed = hub["RELAY"].get_ac_speed()
		
		if "BLUETOOTH" in hub.keys():	
			present_devices = hub["BLUETOOTH"].get_traked_devices()

	return render_template("index.html",
							title = 'Home',
							temp = actual_temperature,
							humid = actual_humidity,
							last_update = last_update,
							lux = actual_luminosity,
							current = actual_current,
							speed = ac_speed,
							present_devices = present_devices
							)

@app.route('/settings')
@login_required
def settings():
	return render_template("settings.html")


@app.route('/gateway')
@login_required
def gateway():
	return render_template("gateway.html")

@app.route('/graph')
@app.cache.cached(timeout=30)
def graph():

	data = {}

	if app.config["HUB"]:
		hub = app.config["HUB"]

		if "STORAGE HANDLER" in hub.keys():
			data = hub["STORAGE HANDLER"].getGraphData()

	return render_template("graphs.html", data=data)


@app.route('/login' , methods=['GET','POST'])
def login():

	form = LoginForm()

	if form.validate_on_submit():
		flash("Username: "+form.username.data + "Pass:"+ form.password.data+ ", remember_me= "+ str(form.remember_me.data))
		return redirect('/index')

	
	return render_template('login.html',
		form = form)
	#app.cache.clear()



@app.route('/logout' , methods=['GET','POST'])
def logout():
	app.cache.clear()
	return redirect(url_for('index'))
	


@app.route('/register' , methods=['GET','POST'])
def register():

	form = RegisterForm()

	if form.validate_on_submit():
		
		if app.config["USER MANAGER"] and app.config["API KEY"]:
			um = app.config["USER MANAGER"]
			key = app.config["API KEY"]

			if not form.key.data == key:
				form.errors["key"] = ["Invalid Key"]
				return render_template('register.html', form=form)

			if um.existsUser(form.username.data):
				form.errors["username"] = ["Username Exists"]
				return render_template('register.html', form=form)

			else:
				um.addUser(form.username.data, form.password.data)

		flash('Thanks for registering')
		return redirect(url_for('login'))

	return render_template('register.html', form=form)

@login_manager.user_loader
def load_user(id):
	print "-------------------------", id

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def process_index_post():
	
	#print str(request.form.keys())
	
	if "HUB" in app.config.keys() and app.config["HUB"]:

		if "RELAY" in app.config["HUB"].keys():
			
			relay = app.config["HUB"]["RELAY"]
			if "AC_OFF" in request.form.keys():
				relay.set_ac_speed(0)
			elif "AC_1" in request.form.keys():
				relay.set_ac_speed(1)
			elif "AC_2" in request.form.keys():
				relay.set_ac_speed(2)
			elif "AC_3" in request.form.keys():
				relay.set_ac_speed(3)


class WebHandler(Thread):
	
	def __init__(self, hub):
		Thread.__init__(self)
		app.config["HUB"] = hub
		app.config["USER MANAGER"] = UserManager()
		app.config["API KEY"] = "0000"
		app.config.update(
			CSRF_ENABLED = True,
			SECRET_KEY = '2c1de198f4d30fa5d342ab60c31eeb308sb6de0f063e20efb9322940e3888d51c'
			)
		self.server = Process(target=app.run(debug = True, 
											host='0.0.0.0',
											use_reloader=False))

	def run(self):
		self.server.start()
		print "-------------------------------"

	def stop(self):
	 	self.server.join()

if __name__ == "__main__":
	
	wh = WebHandler(None)
	wh.start()
	sleep(10)
	wh.stop()
