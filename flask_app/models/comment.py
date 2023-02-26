from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, post
db = "posts"

class Comment:
    def __init__( self , data ):
        self.id = data['id']
        self.comment = data['comment']
        self.post_id=data['post_id']
        self.user_id=data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.maker = None
    @classmethod
    def save_comment(cls, data):
        query = "INSERT INTO comments (post_id, user_id, comment) VALUES (%(post_id)s, %(user_id)s, %(comment)s);"
        return connectToMySQL(db).query_db(query, data)