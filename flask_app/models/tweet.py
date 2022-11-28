from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Tweet:
    db_name = 'twitter'
    def __init__(self,data):
        self.id = data['id'],
        self.content = data['content'],
        self.user_id = data['user_id'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def createTweet(cls,data):
        query = 'INSERT INTO tweets ( content, user_id ) VALUES ( %(content)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod    #you get info about all tweets : likes, user_id etc
    def getAllTweets(cls):
        query = 'SELECT tweets.id , tweets.content, COUNT(likes.id) AS likesNr, users.first_name AS creator_name, email, users.id AS creator_id FROM tweets LEFT JOIN users ON tweets.user_id = users.id LEFT JOIN likes ON likes.tweet_id = tweets.id GROUP BY tweets.id;'
        results = connectToMySQL(cls.db_name).query_db(query)
        tweets = []
        for row in results:
            tweets.append(row)
        return tweets

    



    @classmethod
    def getTweetByID(cls,data):
        query = 'SELECT * FROM tweets WHERE id = %(tweet_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if results:
            return results[0]
        return False



    @classmethod
    def updateTweet(cls,data):
        query = 'UPDATE tweets SET content = %(content)s, user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data) 


    @classmethod
    def likeTweet(cls,data):
        query = 'INSERT INTO likes ( user_id, tweet_id) VALUES ( %(user_id)s, %(tweet_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    @classmethod
    def unlikeTweet(cls,data):
        query = 'DELETE FROM likes WHERE tweet_id = %(tweet_id)s AND user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod      #delete
    def deleteLikes(cls,data):
        query = 'DELETE FROM likes WHERE likes.tweet_id = %(tweet_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
        
    @classmethod
    def destroyTweet(cls,data):
        query= 'DELETE FROM tweets WHERE tweets.id = %(tweet_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)


    @staticmethod
    def validate_tweet(tweet):
        is_valid = True
        if len(tweet['content']) < 1:
            flash("Please dont submit empty content", 'content')
            is_valid = False
        return is_valid
