from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Phonebook, phonebook_schema, phonebooks_schema
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():

    user = {'username': 'Faiz'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): #validate the username and password on submit. it's declared in form.py class. this will only return true if only both username and password are valid
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    form = EmptyForm()
    return render_template('user.html', title='User',user=user, posts=posts, form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('USer {} not found'.format(username))
            return redirect(url_for('index'))
        if user== current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
###
###
###
###P
###
###
###
@app.route('/phonebook')
def phonebook():
    all_contacts =Phonebook.query.all()
    result = phonebooks_schema.dump(all_contacts)   
    return render_template('phonebook.html', title='Phone', contacts=result)

@app.route('/api/phonebook', methods=['GET'])
def get_contacts():
    all_contacts =Phonebook.query.all()
    result = phonebooks_schema.dump(all_contacts)   
    return jsonify(result)

@app.route('/api/phonebook', methods=['POST'])
def new_contact():
    name = request.json['name']
    address = request.json['address']
    city = request.json['city']
    phonenumber = request.json['phonenumber']

    new_phonebook = Phonebook(name, phonenumber, address,city)
    
    db.session.add(new_phonebook)
    db.session.commit()
    
    return phonebook_schema.jsonify(new_phonebook)

@app.route('/api/phonebook/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Phonebook.query.get(id)
    return phonebook_schema.jsonify(contact)    

@app.route('/api/phonebook/<int:id>', methods=['PUT'])
def update_contact(id):
    contact =Phonebook.query.get(id)

    name = request.json['name']
    address = request.json['address']
    city = request.json['city']
    phonenumber = request.json['phonenumber']

    contact.name = name
    contact.address = address
    contact.city = city
    contact.phonenumber = phonenumber

    db.session.commit()

    return phonebook_schema.jsonify(contact)    

@app.route('/api/phonebook/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Phonebook.query.get(id)
    
    db.session.delete(contact)
    db.session.commit()
    return phonebook_schema.jsonify(contact)    