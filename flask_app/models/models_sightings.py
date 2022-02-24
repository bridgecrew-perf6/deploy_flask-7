from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
import re
from flask import flash
from flask_app.models import models_users

Database = 'sight_with_believe'
class Sightings:
    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.happened = data['happened']
        self.siting_date = data['siting_date']
        self.sasquatches = data['sasquatches']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner_first_name = ''
        self.owner_last_name = ''
        self.skeptics = []
        self.num_skeptics= 0
        
        

    
    
    @classmethod
    def add(cls,data):
        query = "INSERT INTO sightings (location,happened,siting_date,sasquatches,user_id) VALUES ( %(location)s,%(happened)s,%(siting_date)s,%(sasquatches)s,%(user_id)s);"    
        return connectToMySQL(Database).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM sightings WHERE id=%(id)s;"    
        return connectToMySQL(Database).query_db(query,data)
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(Database).query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return []
        
    @classmethod
    def update(cls,data):
        query = "UPDATE sightings SET location=%(location)s,happened=%(happened)s, siting_date=%(siting_date)s,sasquatches=%(sasquatches)s WHERE id = %(id)s;"    
        return connectToMySQL(Database).query_db(query,data)
    
    
    
    @classmethod
    def get_user_with_sightings(cls):
        query = 'SELECT * FROM sightings LEFT JOIN users ON users.id = sightings.user_id;'
        results = connectToMySQL(Database).query_db( query)
        all_sightings = []
        for one_sight in results:
            one_sight_temp = cls(one_sight)
            one_sight_temp.owner_first_name = one_sight['first_name']
            one_sight_temp.owner_last_name = one_sight['last_name']
            temp = cls.get_one_with_skeptics({'id':one_sight["id"]})
            print(temp.skeptics)
            if temp.skeptics:
                one_sight_temp.num_skeptics = len(temp.skeptics)
            else:
                one_sight_temp.num_skeptics = 0
            all_sightings.append(one_sight_temp)

        return all_sightings
    
    @staticmethod
    def validate_sighting(new):
        is_valid = True # we assume this is true
        if not new.get('location'):
            flash("location need to be filled",'sighting_error')

            is_valid = False
        
        if not new.get('happened'):
            flash("happened need to be filled",'sighting_error')
            is_valid = False
        
        if not new.get('siting_date'):
            flash("siting_date need to be filled",'sighting_error')
            is_valid = False
        
        if int(new['sasquatches'])<1:
            flash("sasquatches must be at least 1 ",'sighting_error')
            is_valid = False
        
        return is_valid
    
    
    @classmethod
    def get_one_with_skeptics(cls,data):
        query = "SELECT * FROM sightings LEFT JOIN believes ON sightings.id = believes.sighting_id LEFT JOIN users ON users.id = believes.user_id WHERE sightings.id = %(id)s;"
        results = connectToMySQL(Database).query_db(query,data)
        sightings = cls(results[0])
        for right_tab in results:
            users_data = {
                'id':right_tab["users.id"],
                'first_name':right_tab['first_name'],
                'last_name':right_tab['last_name'],
                'email':right_tab['email'],
                'password':right_tab['password'],
                "created_at" : right_tab["believes.created_at"],
                "updated_at" : right_tab["believes.updated_at"]
            }
            if users_data['id']:
                sightings.skeptics.append(models_users.Users(users_data))
        return sightings