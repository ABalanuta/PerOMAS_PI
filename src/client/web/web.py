#!/usr/bin/env python
"""Web server based on Flask"""

__author__ = "Artur Balanuta"
__version__ = "1.0.2"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from Task import Task

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from flask import Flask, request, render_template, flash, redirect, url_for, g
from flask.ext.cache import Cache
from flask.ext.compress import Compress
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, validators
from wtforms.validators import Required

from multiprocessing import Process
from threading import Thread
from time import sleep
from datetime import datetime

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
        validators.Length(min=4, max=10)
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
    ac_mode = "--"
    ac_setpoint = None
    ac_heat_or_cool = None
    present_devices = dict()
    logs = getLogData(10)
    light_bulb = [False, False]


    if app.config["HUB"]:
        hub = app.config["HUB"]

        if "TEMPERATURE" in hub.keys():
            actual_temperature = round(hub["TEMPERATURE"].getTemperature(), 1)
            actual_humidity = round(hub["TEMPERATURE"].getHumidity(), 1)
            last_update = hub["TEMPERATURE"].getLastUpdate()

        if "CURRENT" in hub.keys():
            actual_current = round(hub["CURRENT"].getValue(), 1)

        if "LUMINOSITY" in hub.keys():
            actual_luminosity = hub["LUMINOSITY"].getValue()

        if "RELAY" in hub.keys():
            ac_speed = hub["RELAY"].get_ac_speed()
            ac_heat_or_cool = hub["RELAY"].get_ac_mode()
            light_bulb = hub["RELAY"].get_lights_state()

        if "BLUETOOTH" in hub.keys():
            present_dev = hub["BLUETOOTH"].get_traked_devices()
            
            if "USER MANAGER" in app.config.keys():
                um = app.config["USER MANAGER"]
                for username, user in um.users.items():
                    if user.phone in present_dev:
                        present_devices[username] = user.phone

        if "LOGIC ENGINE" in hub.keys():
            ac_mode = hub["LOGIC ENGINE"].getACMode()
            ac_setpoint = hub["LOGIC ENGINE"].get_AC_Setpoint()

    return render_template("index.html",
                           temp=actual_temperature,
                           humid=actual_humidity,
                           last_update=last_update,
                           lux=actual_luminosity,
                           current=actual_current,
                           mode=ac_mode,
                           setpoint=ac_setpoint,
                           speed=ac_speed,
                           present_devices=present_devices,
                           ac_heat_or_cool=ac_heat_or_cool,
                           logs=logs,
                           light_bulb=light_bulb
                           )


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

    if request.method == 'POST':
        process_settings_post()
    
    last_seen_devices = []

    if app.config["HUB"]:
        hub = app.config["HUB"]

        if "BLUETOOTH" in hub.keys():
            last_seen_devices = hub["BLUETOOTH"].get_discovered_devices()

    return render_template("settings.html",
                        last_seen_devices=last_seen_devices
                        )


@app.route('/gateway', methods=['GET', 'POST'])
@login_required
def gateway():
    if request.method == 'POST':
        if app.config["HUB"]:
            hub = app.config["HUB"]
            sm = hub['SCHEDULE MANAGER']

            if 'REBOOT' in request.form.keys():
                sm.tasks.append(Task(sm.reboot_device, 0, one_time_task = True, var=str(g.user)))

            if 'SHUTDOWN' in request.form.keys():
                sm.tasks.append(Task(sm.shutdown_device, 0, one_time_task = True, var=str(g.user)))
                

    return render_template("gateway.html")


@app.route('/graph')
@login_required
#@app.cache.cached(timeout=180)
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

                user = um.getUser(form.username.data)

                login_user(user, form.remember_me.data)
                flash("Logged in successfully.", "success")
                return redirect(request.args.get("next") or url_for("index"))

    return render_template('login.html', form=form)


@app.route('/admin')
@login_required
def admin():

	if app.config["HUB"]:
		hub = app.config["HUB"]
		cm = hub["CLI MANAGER"]
		nodesData = cm.getBatmanNodes()
        return render_template('admin.html', nodes=nodesData)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logged Out successfully.", "success")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        if app.config["USER MANAGER"] and app.config["HUB"]["API KEY"]:
            um = app.config["USER MANAGER"]
            key = app.config["HUB"]["API KEY"]

            if not form.key.data == key:
                form.errors["key"] = ["Invalid Key"]
                return render_template('register.html', form=form)

            if um.existsUser(form.username.data):
                form.errors["username"] = ["Username Exists"]
                return render_template('register.html', form=form)

            else:
                um.addUser(form.username.data, form.password.data)

        flash('Thanks for registering', "info")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(id):
    if app.config["USER MANAGER"]:
        um = app.config["USER MANAGER"]
        return um.getUser(id)

@app.before_request
def before_request():
    g.user = current_user

@app.cache.cached(timeout=30, key_prefix='GraphData')
def getGraphData():

    if app.config["HUB"]:
        hub = app.config["HUB"]

        if "STORAGE HANDLER" in hub.keys():
            return hub["STORAGE HANDLER"].getGraphData()
    else:
        return {}

@app.cache.cached(timeout=10, key_prefix='LogData')
def getLogData(num):
    if app.config["HUB"]:
        hub = app.config["HUB"]

        if "STORAGE HANDLER" in hub.keys():
            return hub["STORAGE HANDLER"].getLogs(num)
    else:
        return {}

def process_settings_post():

    if app.config["HUB"]:
        hub = app.config["HUB"]
        user = g.user.username
        storage = None
        bluetooth = None

        if "STORAGE HANDLER" in hub.keys():
            storage = hub["STORAGE HANDLER"]

        if "BLUETOOTH" in hub.keys():
            bluetooth = hub["BLUETOOTH"]

        #print request.form.items()

        if storage and bluetooth:
            
            if "Phone_Set" in request.form.keys():
                new_Phone = request.form["Phone_Set"]
                old_Phone = g.user.get_phone()

                if new_Phone != old_Phone:
                    g.user.set_phone(new_Phone)
                    bluetooth.track_device(new_Phone)
                    storage.log("Changed Traking Phone from "+str(old_Phone)+
                                " to "+new_Phone, user)

            if "Phone_Delete" in request.form.keys():
                new_Phone = None
                old_Phone = g.user.get_phone()

                g.user.set_phone(new_Phone)
                bluetooth.stop_tracking_device(old_Phone)
                storage.log("Changed Traking Phone from "+str(old_Phone)+
                            " to "+str(new_Phone), user)

        if storage:

            if "Add_Action" in request.form.keys():

                if not "Action_Alias" in request.form.keys() or len(request.form["Action_Alias"]) < 1:
                    flash("Invalid Action Alias", 'error')
                    return

                if g.user.has_action_alias(request.form["Action_Alias"]):
                    flash("Alias Already Exists", 'error')
                    return

                if not "Action_Name" in request.form.keys():
                    flash("Invalid Action", 'error')
                    return

                action      = request.form["Action_Name"]  
                alias       = request.form["Action_Alias"]
                arg_type    = None
                arguments   = None

                if action == "Set_Lights":
                    arg_type = "checkbox"
                    arguments = [False, False]
                    if "Light_Bulb_1" in request.form.keys():
                        arguments[0] = True
                    if "Light_Bulb_2" in request.form.keys():
                        arguments[1] = True

                elif action == "Set_Setpoint":
                    arg_type = "text"
                    try:
                        arguments = float(request.form["Setpoint"])
                    except ValueError:
                        flash("Invalid Argument Value", 'error')
                        return
                else:
                    flash("Invalid Action", 'error')
                    return

                g.user.add_action(alias, action, arg_type, arguments)
                storage.log("Created new Action: alias="+alias+" action="+action+
                            " arguments="+str(arguments), user)
                flash("Operation finished successfully.", "success")

            if "Delete_User_Action" in request.form.keys():
                action_alias = request.form["Delete_User_Action"]
                
                if g.user.has_action_alias(action_alias):
                    g.user.del_action(action_alias)
                    storage.log("Deleted Action: alias="+action_alias, user)
                    flash("Operation finished successfully.", "success")

            if "Add_Event" in request.form.keys():

                if not "Event_Alias" in request.form.keys() or len(request.form["Event_Alias"]) < 1:
                    flash("Invalid Event Alias", 'error')
                    return

                if not "Event_Name" in request.form.keys():
                    flash("Invalid Event", 'error')
                    return

                if g.user.has_event_alias(request.form["Event_Alias"]):
                    flash("Alias Event Exists", 'error')
                    return

                event       = request.form["Event_Name"]  
                alias       = request.form["Event_Alias"]
                condition   = request.form[event+"_Condition"]
                argument    = request.form["argument"]

                if event == "Time":
                    try:
                        times = argument.split('-')
                        time_1 = times[0]
                        time_2 = times[1]

                        datetime.strptime(time_1, "%H:%M")
                        datetime.strptime(time_2, "%H:%M")

                        g.user.add_event(alias, event, condition, argument)
                        storage.log("Created new Event: alias="+alias+" event="+event+" condition="+str(condition)+
                                    " argument="+str(argument), user)
                        flash("Operation finished successfully.", "success")
                    except:
                        flash("Invalid Argument Value: Does not match format <Hour:Minutes-Hour:Minutes>", 'error')
                        return

                elif event == "In_the_Office":
                    g.user.add_event(alias, event, condition)
                    storage.log("Created new Event: alias="+alias+" event="+event+" condition="+str(condition), user)
                    flash("Operation finished successfully.", "success")

                else:
                    flash("Invalid Event", 'error')
                    return

            if "Delete_User_Event" in request.form.keys():
                event_alias = request.form["Delete_User_Event"]
                
                if g.user.has_event_alias(event_alias):
                    g.user.del_event(event_alias)
                    storage.log("Deleted Event: alias="+event_alias, user)
                    flash("Operation finished successfully.", "success")
                return

            if "Delete_Rule" in request.form.keys():
                rule_alias = request.form["Delete_Rule"]

                if g.user.has_rule_alias(rule_alias):
                    g.user.del_rule(rule_alias)
                    storage.log("Deleted Rule: alias="+rule_alias, user)
                    flash("Operation finished successfully.", "success")
                return


            
            if "Add_Rule" in request.form.keys():

                if not "Rule_Alias" in request.form.keys() or len(request.form["Rule_Alias"]) < 1:
                    flash("Invalid Event Alias", 'error')
                    return

                if not "Rule_Events" in request.form.keys():
                    flash("Invalid Event", 'error')
                    return

                if not "Rule_Action" in request.form.keys():
                    flash("Invalid Action", 'error')
                    return

                if g.user.has_rule_alias(request.form["Rule_Alias"]):
                    flash("Rule alias already Exists", 'error')
                    return

                rule_alias      = request.form["Rule_Alias"]
                events_alias    = request.form.getlist('Rule_Events')  
                action_alias    = request.form["Rule_Action"]

                if not g.user.has_action_alias(action_alias):
                    flash("Action does Not Exists", 'error')
                    return

                for event in events_alias:
                    if not g.user.has_event_alias(event):
                        flash("Event with Alias: "+event+" does Not Exists", 'error')
                        return

                g.user.add_rule(rule_alias, events_alias, action_alias)
                storage.log("Created new Rule: alias="+rule_alias+" events="+str(events_alias)+" action="+action_alias, user)
                flash("Operation finished successfully.", "success")

def process_index_post():

    if app.config["HUB"]:
        hub = app.config["HUB"]
        user = g.user.username
        storage = None
        relay = None
        logic = None

        if "STORAGE HANDLER" in hub.keys():
            storage = hub["STORAGE HANDLER"]

        if "LOGIC ENGINE" in hub.keys():
            logic = hub["LOGIC ENGINE"]
        
        if "RELAY" in hub.keys():
            relay = hub["RELAY"]

        if logic and storage:

            if "Setpoint" in request.form.keys():
                new_setpoint = float(request.form["Setpoint"])
                old_setpoint = logic.get_AC_Setpoint()

                if new_setpoint != old_setpoint:
                    logic.set_AC_Setpoint(new_setpoint)
                    storage.log("AC Setpoint changed to " + str(new_setpoint), user)

            if "AC_Auto" in request.form.keys():
                if logic.getACMode() != "Auto":
                    logic.setACMode("Auto")
                    storage.log("Turned Automatic AC Mode", user)
                
            elif "AC_Manual" in request.form.keys():
                if logic.getACMode() != "Manual":
                    logic.setACMode("Manual")
                    storage.log("Turned Manual AC Mode", user)

        if relay and storage:
            
            if "AC_COOL" in request.form.keys():
                if relay.get_ac_mode() != "Cool":
                    relay.set_ac_mode("Cool")
                    storage.log("Changed AC Mode to Cooling", user)

            if "AC_HEAT" in request.form.keys():
                if relay.get_ac_mode() != "Heat":
                    relay.set_ac_mode("Heat")
                    storage.log("Changed AC Mode to Heating", user)

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

            elif "Light_1" in request.form.keys():
                current_state = relay.get_lights_x1_state()
                relay.set_lights_x1_state( not current_state)
                if current_state:
                    storage.log("Turned off Lights 1", user)
                else:
                    storage.log("Turned on Lights 1", user)

            elif "Light_2" in request.form.keys():
                current_state = relay.get_lights_x2_state()
                relay.set_lights_x2_state( not current_state)
                if current_state:
                    storage.log("Turned off Lights 2", user)
                else:
                    storage.log("Turned on Lights 2", user)      

class WebHandler(Thread):

    def __init__(self, hub):
        Thread.__init__(self)
        app.config["HUB"] = hub

        um = UserManager(hub)
        app.config["USER MANAGER"] = um
        hub["USER MANAGER"] = um

        app.config.update(
            CSRF_ENABLED=True,
            SECRET_KEY='2c1de198f4d30fa5d342ab60c31eeb308sb6de0f063e20efb9322940e3888d51c'
        )
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(5000)
        self.server = Process(target=IOLoop.instance().start())

    def run(self):
        self.server.start()

    def stop(self):
        self.server.join()

if __name__ == "__main__":

    wh = WebHandler(None)
    wh.start()
    sleep(10)
    wh.stop()
