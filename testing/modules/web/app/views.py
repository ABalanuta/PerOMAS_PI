from flask import render_template, flash, redirect, send_from_directory
from forms import LoginForm
from web.app import app
import os

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/index')
def index():
	user = { 'nickname': 'Miguel' } # fake user
	return render_template("index.html",
        title = 'Home',
        user = user)
        
@app.route('/settings')
def settings():
	return render_template("settings.html")

@app.route('/gateway')
def gateway():
	return render_template("gateway.html")

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

