from flask import  render_template, request, redirect, session, flash
from flask_app.models.models_users import Users
from flask_app.models.models_sightings import Sightings
from flask_app.models.believes_functions import link_believe,dislink_believe
from flask_app import app

@app.route('/new/sighting')
def create_sighting():
    if 'id' not in session:
        return redirect('/')
    user = Users.get_one({'id':session['id']})
    return render_template('sighting_new.html',user=user)


@app.route('/new/sighting/processing', methods=['post'])
def creating_sighting():
    data = {**request.form}
    print(request.form)
    if not Sightings.validate_sighting(data):
        return redirect('/new/sighting')
    
    # print(request.form)
    data = {
        **request.form,
        'user_id' : session['id']
    }
    Sightings.add(data)
    return redirect('/dashboard')



@app.route('/show/<int:id>')
def view_recipe(id):
    if 'id' not in session:
        return redirect('/')
    user = Users.get_one({'id':session['id']})
    sighting = Sightings.get_one_with_skeptics({'id':id})
    reporter = Users.get_one({'id':sighting.user_id})
    id_storage=[]
    for skeptic in sighting.skeptics:
        id_storage.append(skeptic.id)
    check = False
    if user.id in id_storage:
        check = True
    
    return render_template('sighting_show.html',sighting=sighting,user = user,reporter=reporter,check=check)


@app.route('/delete_sighting/<int:id>')
def delete_sighting(id):
    Sightings.delete({'id':id})
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_sighting(id):
    if 'id' not in session:
        return redirect('/')
    
    
    sighting = Sightings.get_one({'id':id})
    user = Users.get_one({'id':session['id']})
    return render_template('sighting_edit.html',sighting=sighting,user=user)

@app.route('/sighting/editing/<int:id>',methods=['post'])
def editing_sighting(id):
    data = {**request.form}
    print(request.form)
    if not Sightings.validate_sighting(data):
        return redirect(f'/edit/{id}')
    data = {
        **request.form,
        'id' : id
    }
    Sightings.update(data)
    return redirect('/dashboard')


@app.route('/link_believe/<int:id>')
def linking_believe(id):
    data ={
        "sighting_id" : id,
        "user_id" : session['id']
    }
    
    link_believe(data)
    
    return redirect(f'/show/{id}')


@app.route('/dislink_believe/<int:sighting_id>')
def dislinking_believe(sighting_id):
    data ={
        "sighting_id" : sighting_id,
        "user_id" : session['id']
    }
    
    dislink_believe(data)
    
    return redirect(f'/show/{sighting_id}')