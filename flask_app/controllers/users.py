from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.tweet import Tweet


@app.route('/')
def index():
    return redirect('/loginPage')

@app.route('/loginPage')
def loginPage():
    return render_template("loginRegister.html")


@app.route('/register', methods = ['POST'])
def registerUser():
    if not User.validate_user(request.form):
        flash("Complete all the fields correctly", 'signUp')
        return redirect(request.referrer)

    if User.getUserByEmail(request.form):
        flash("This email already exists", 'emailRegister')
        return redirect(request.referrer)

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.createUser(data)
    return redirect(request.referrer)


@app.route('/login', methods = ['POST'])
def loginUser():
    data = {
        'email' : request.form['email'],
        'password': request.form['password']
    }
    if len(request.form['email'])< 1:
        flash("Email is required to log in", 'emailLogin')
        return redirect(request.referrer)
    if not User.getUserByEmail(data):
        flash("This email doesn't exits mate", 'emailLogin')
        return redirect(request.referrer)
    user = User.getUserByEmail(data)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Incorrect password", 'passwordLogin')
        return redirect(request.referrer)
    
    session['user'] = user['id']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    userLikedTweets = User.loggedUserLikedTweets(data)
    tweets = Tweet.getAllTweets()
    return render_template("dashboard.html", loggedUser = loggedUser, tweets = tweets, userLikedTweets = userLikedTweets)


@app.route('/usersProfile/<int:id>')
def profile(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id' : id
    }
    print(data)
    tweets = User.getAllUserInfo(data)
    user = User.getUserByID(data)
    return render_template("profile.html", user=user, tweets=tweets)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')