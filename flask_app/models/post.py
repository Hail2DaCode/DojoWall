from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, comment
db = "posts"

class Post:
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        self.comments = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    @classmethod
    def get_all_posts_with_creator(cls):
        # Get all tweets, and their one associated User that created it
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL(db).query_db(query)
        all_posts = []
        for row in results:
            # Create a Tweet class instance from the information from each db row
            one_post = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_post_creator_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            creator = user.User(one_post_creator_info)
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            one_post.creator = creator
            # Append the Tweet containing the associated User to your list of tweets
            all_posts.append(one_post)
        return all_posts
    @classmethod
    def get_all_posts_with_creator_and_comments(cls):
        # Get all tweets, and their one associated User that created it
        query = """SELECT * FROM posts 
                LEFT JOIN comments ON posts.id = comments.post_id 
                LEFT JOIN users ON users.id = comments.user_id
                LEFT JOIN users as creators on creators.id = posts.user_id   
                ORDER BY posts.created_at DESC;"""
        results = connectToMySQL(db).query_db(query)
        all_posts = []
        for row in results:
            if len(all_posts) < 1 or all_posts[-1].id != row['id']:

            # Create a Tweet class instance from the information from each db row
                one_post = cls(row)
                all_posts.append(one_post)
            # Prepare to make a User class instance, looking at the class in models/user.py
                one_post_creator_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                    "id": row['creators.id'], 
                    "first_name": row['creators.first_name'],
                    "last_name": row['creators.last_name'],
                    "email": row['creators.email'],
                    "password": row['creators.password'],
                    "created_at": row['creators.created_at'],
                    "updated_at": row['creators.updated_at']
                }
                
            # Create the User class instance that's in the user.py model file
                creator_post = user.User(one_post_creator_info)
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
                one_post.creator = creator_post
            if row['comments.id'] == None:
                continue
            comment_data = {
                "id": row['comments.id'],
                "comment": row['comment'],
                "user_id": row['comments.user_id'],
                "post_id": row['post_id'],
                "created_at": row['comments.created_at'],
                "updated_at": row['comments.updated_at']
            }
            user_comment_data = {
                "id": row['users.id'], 
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
            }
            comment_creator = user.User(user_comment_data)
            comment1 = comment.Comment(comment_data)
            comment1.maker = comment_creator
            one_post.comments.append(comment1)
            # Append the Tweet containing the associated User to your list of tweets
            
        return all_posts
    @classmethod
    def get_all_posts_with_creator_and_comment_2_queries(cls):
        # Get all tweets, and their one associated User that created it
        query1 = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL(db).query_db(query1)
        all_posts = []
        for row in results:
            # Create a Tweet class instance from the information from each db row
            one_post = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_post_creator_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            creator1 = user.User(one_post_creator_info)
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            one_post.creator = creator1
            # Append the Tweet containing the associated User to your list of tweets
            all_posts.append(one_post)
        query2 = "SELECT * FROM comments JOIN users ON comments.user_id = users.id;"
        comments_from_db =  connectToMySQL(db).query_db(query2)
        comments =[]
        for c in comments_from_db:
            one_comment = comment.Comment(c)
            one_comment_creator_info = {
                "id": c['users.id'], 
                "first_name": c['first_name'],
                "last_name": c['last_name'],
                "email": c['email'],
                "password": c['password'],
                "created_at": c['users.created_at'],
                "updated_at": c['users.updated_at']
            }
            creator2 = user.User(one_comment_creator_info)
            print(creator2.first_name)
            one_comment.maker = creator2
            comments.append(one_comment)
        for post in all_posts:
            for comm in comments:
                if post.id == comm.post_id:
                    post.comments.append(comm)
        return all_posts


    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def save_2(cls, data):
        query = "INSERT INTO comments (post_id, user_id) VALUES (%(post_id)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def save_3(cls, data):
        query = "INSERT INTO comments (post_id, user_id, comment) VALUES (%(post_id)s, %(user_id)s, %(comment)s);"
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])
    @classmethod
    def delete(cls, data):
        query = """
                DELETE FROM posts
                WHERE id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query, data)
        return results