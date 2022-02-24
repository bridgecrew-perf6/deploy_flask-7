from flask import  render_template, request, redirect, session, flash
from flask_app.models.models_users import Users
from flask_app.models.models_sightings import Sightings

from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

@app.route('/')
def index():
    if 'id' in session:
        del session['id']
    
    return render_template('index.html')

@app.route('/registering', methods=['post'])
def registering():
    if not Users.validate(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password" : pw_hash
    }
    session['id'] = Users.add(data)
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/')
    # user = Users.get_user_with_recipes( {'id':session['id']} )
    all_sightings = Sightings.get_user_with_sightings() 
    user = Users.get_one({'id':session['id']})
    return render_template('dashboard.html',user=user,all_sightings=all_sightings)


@app.route('/logining', methods=['post'])
def logining():
    data = {'email' : request.form['email']}
    user_db = Users.get_by_mail(data)
    if not Users.validate_login(request.form):
        return redirect('/')
    if not user_db:
        flash("Invalid Email/Password",'login_error')
        return redirect("/")
    if not bcrypt.check_password_hash(user_db.password, request.form['password']):
        flash("Invalid Email/Password",'login_error')
        return redirect("/")    
    
    session['id'] = user_db.id
    return redirect('/dashboard')

