
from flask_app.config.mysqlconnection import connectToMySQL
import re	#regex thing
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask import flash

class User:
    db_name = 'twitter'
    def __init__(self,data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']
    

    @classmethod
    def createUser(cls,data):
        query = 'INSERT INTO users ( first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def getUserByID(cls,data):
        query = 'SELECT * FROM users WHERE id = %(user_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result[0]

    @classmethod
    def getUserByEmail(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return False

    @classmethod        #you get all the tweets of a user
    def getAllUserInfo(cls, data):
        query= 'SELECT * FROM users LEFT JOIN tweets on tweets.user_id = users.id WHERE users.id = %(user_id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        tweets = []
        for row in results:
            tweets.append(row)
        return tweets
    

    @classmethod        #check if a user has liked a tweet and like it or unlike it
    def loggedUserLikedTweets(cls, data):
        query = 'SELECT tweet_id as id FROM likes LEFT JOIN users on likes.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        tweetsLiked = []
        for row in results:
            tweetsLiked.append(row['id'])
        return tweetsLiked

    
    #method to validate register
    @staticmethod       
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash("First name is required to register", 'first_name')
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Last name is required to register", 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long", 'password')
            is_valid = False
        if user['password'] != user['confirmPassword']:
            flash("Passwords do not match", 'confirmPassword')
            is_valid = False
        return is_valid