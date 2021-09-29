import json
from flaskext.mysql import MySQL

def lambda_handler(event, context):
    # data from MQTT comes from event
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = ''
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = ''
    app.config['MYSQL_DATABASE_HOST'] = ''
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute('select * from test')
    query_result = cursor.fetchall()

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(query_result)
    }
    
    