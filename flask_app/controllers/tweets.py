from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.tweet import Tweet

@app.route('/tweet', methods = ['POST'])
def createTweets():
    if not Tweet.validate_tweet(request.form):
        return redirect(request.referrer)
    data = {
        'content': request.form['content'],
        'user_id': session['user']
    }
    Tweet.createTweet(data)
    return redirect('/dashboard')


@app.route('/like/<int:id>')
def like(id):
    data = {
        'tweet_id': id,
        'user_id': session['user']
    }
    Tweet.likeTweet(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def unlike(id):
    data = {
        'tweet_id': id,
        'user_id': session['user']
    }
    Tweet.unlikeTweet(data)
    return redirect(request.referrer)

@app.route('/delete/<int:id>')
def delete(id):
    if 'user' not in session:
        return redirect('/logout')

    data = {
        'tweet_id': id
    }
    tweet = Tweet.getTweetByID(data)
    if session['user'] == tweet['user_id']:
        Tweet.deleteLikes(data)
        Tweet.destroyTweet(data)
        return redirect(request.referrer)
    if not session['user'] == tweet['user_id']:
        return render_template("404Error.html")
    return redirect(request.referrer)


@app.route('/edit/<int:id>')
def edit(id):
    if 'user' not in session:
        return redirect('/logout')
    
    data = {
        'tweet_id' : id
    }
    dataInfo = {
        'user_id' : session['user']
    }
    
    tweets = Tweet.getTweetByID(data)
    if not session['user'] == tweets['user_id']:
        return render_template("404Error.html")
    loggedUser = User.getUserByID(dataInfo)
    return render_template('editTweet.html', tweets = tweets, loggedUser =loggedUser)

@app.route('/editTweet', methods = ['POST'])
def update():
    if not Tweet.validate_tweet(request.form):
        flash("Do not submit empty content", 'contentUpdate')
        return redirect(request.referrer)

    data = {
        'content': request.form['content'],
        'user_id' : session['user']
    }
    Tweet.updateTweet(data)
    return redirect('/dashboard')