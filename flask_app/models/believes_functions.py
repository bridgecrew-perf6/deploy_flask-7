from flask_app.config.mysqlconnection import connectToMySQL
Database = 'sight_with_believe'

def link_believe(data):
    query = "INSERT INTO believes(user_id,sighting_id) Values (%(user_id)s,%(sighting_id)s);"    
    return connectToMySQL(Database).query_db(query,data)


def dislink_believe(data):
    query = "DELETE FROM believes WHERE user_id=%(user_id)s and sighting_id=%(sighting_id)s;"    
    return connectToMySQL(Database).query_db(query,data)