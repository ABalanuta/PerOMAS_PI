#!/usr/bin/env python
"""Web server based on Flask"""

__author__ = "Artur Balanuta"
__version__ = "1.0.2"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


from flask import Flask, request, render_template, flash, redirect, send_from_directory, url_for, g
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
app.cache = Cache(app, config={'CACHE_TYPE': 'simple'})
Compress(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"


#
# Forms
#
class LoginForm(Form):
    username = TextField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.Length(min=8, max=100)])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(Form):
    username = TextField('username', [
        validators.Required(),
        validators.Length(min=4, max=25)
    ])

    password = PasswordField('New Password', [
        validators.Required(),
        validators.Length(min=8, max=100),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])

    password_confirm = PasswordField('password_confirm')

    key = PasswordField('password', [
        validators.Required(),
        validators.Length(min=4)
    ])

#
#    Flask Routes
#


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        process_index_post()

    # Ambient values
    actual_temperature = "--"
    actual_humidity = "--"
    last_update = "--"
    actual_luminosity = "--"
    actual_current = "--"
    ac_speed = "--"
    present_devices = None
    logs = getLogData(20)

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
                           temp=actual_temperature,
                           humid=actual_humidity,
                           last_update=last_update,
                           lux=actual_luminosity,
                           current=actual_current,
                           speed=ac_speed,
                           present_devices=present_devices,
                           logs=logs
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
@login_required
@app.cache.cached(timeout=180)
def graph():

    data = getGraphData()

    return render_template("graphs.html", data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        # session['remember_me'] = form.remember_me.data
        if app.config["USER MANAGER"]:
            um = app.config["USER MANAGER"]

            if um.existsUser(form.username.data) and um.validatePassword(
                form.username.data,
                form.password.data):

            	print "Remember-me?: "+str(form.remember_me.data)
                user = um.getUser(form.username.data)

                login_user(user, form.remember_me.data)
                flash("Logged in successfully.")
                return redirect(request.args.get("next") or url_for("index"))

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logged Out successfully.")
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
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
    print "Load:" + id
    if app.config["USER MANAGER"]:
        um = app.config["USER MANAGER"]
        return um.getUser(id)

@app.before_request
def before_request():
    g.user = current_user

#@app.cache.cached(timeout=30, key_prefix='GraphData')
def getGraphData():

    if app.config["HUB"]:
        hub = app.config["HUB"]

        if "STORAGE HANDLER" in hub.keys():
            return hub["STORAGE HANDLER"].getGraphData()
    else:
        return {}

@app.cache.cached(timeout=30, key_prefix='LogData')
def getLogData(num):
    if app.config["HUB"]:
        hub = app.config["HUB"]

        if "STORAGE HANDLER" in hub.keys():
            return hub["STORAGE HANDLER"].getLogs(num)
    else:
        return {}

def process_index_post():

    if app.config["HUB"]:
        hub = app.config["HUB"]

        if "RELAY" in hub.keys() and "STORAGE HANDLER" in hub.keys():
            
            relay = hub["RELAY"]
            storage = hub["STORAGE HANDLER"]
            user = g.user.username

            if "AC_OFF" in request.form.keys():
                if relay.get_ac_speed() != 0:
                    relay.set_ac_speed(0)
                    storage.log("Turned OFF AC Fan", user)

            elif "AC_1" in request.form.keys():
                if relay.get_ac_speed() != 1:
                    relay.set_ac_speed(1)
                    storage.log("Turned AC Fan to speed 1", user)

            elif "AC_2" in request.form.keys():
                if relay.get_ac_speed() != 2:
                    relay.set_ac_speed(2)
                    storage.log("Turned AC Fan to speed 2", user)

            elif "AC_3" in request.form.keys():
                if relay.get_ac_speed() != 3:
                    relay.set_ac_speed(3)
                    storage.log("Turned AC Fan to speed 3", user)


class WebHandler(Thread):

    def __init__(self, hub):
        Thread.__init__(self)
        app.config["HUB"] = hub
        app.config["USER MANAGER"] = UserManager(hub)
        app.config["API KEY"] = "0000"
        app.config.update(
            CSRF_ENABLED=True,
            SECRET_KEY='2c1de198f4d30fa5d342ab60c31eeb308sb6de0f063e20efb9322940e3888d51c'
        )
        self.server = Process(target=app.run(debug=True,
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
