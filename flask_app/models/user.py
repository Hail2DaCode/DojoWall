from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = "posts"
date = datetime.datetime.now()
year = date.year
month = date.month
day = date.day
year_slice = slice(4)
month_slice = slice(5,7)
day_slice = slice(8, 10)
programming_languages = ['java', 'javascript', 'c', 'python','html', 'c++', 'c#', "css", 'pascal', 'codejutsu']
print(type(date))

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(user, users):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False
        password = user['password']
        password_list = [*password]
        print(password_list)
        has_upper = False
        has_number = False
        for character in password_list:
            if character.isupper() == True:
                has_upper = True
                continue
            if character.isnumeric() == True:
                has_number = True
                continue
        if not has_upper or not has_number:
            flash("Password must have at least one capital letter and one number")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Invalid password")
            is_valid = False
        for u in users:
            if user['email'] == u.email:
                flash("Email is already taken.  Please use another one")
                is_valid = False
                break
        '''if len(user['dateofbirth']) < 2:
            flash("Please select date of birth!")
            is_valid = False
        elif (int(year) + int(month)/12 + (int(day)/32)/12) - ((int(user['dateofbirth'][year_slice])) + (int(user['dateofbirth'][month_slice])/12) + ((int(user['dateofbirth'][day_slice])/32))/12) < 10:
            flash("You must be 10 years or older to register")
            is_valid = False
        for language in programming_languages:
            if language in user:
                break
            if language == 'codejutsu' and language not in user:
                flash('Must select one programming language')
                is_valid = False
        if 'interests' not in user:
            flash("Please select one interest")
            is_valid = False'''
        return is_valid