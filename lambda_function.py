#!/usr/bin/python
# import psycopg2
import psycopg2
import json


db_host = 'host'
db_port = 5642
db_name = "db"
db_user = "root"
db_pass = "pass"
db_table = "Employees"
def make_conn():
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port=%s password='%s'" % (db_name, db_user, db_host, db_port, db_pass))
    except:
        print ("Connection Error")
        return None;
    return conn


def fetch_data(conn, query):
    result = []
    print ("Now executing: %s" % (query))
    cursor = conn.cursor()
    cursor.execute(query)

    raw = cursor.fetchall()
    for line in raw:
        result.append(line)

    return result
    
def query_data(conn, query):
    print ("Now executing: %s" % (query))
    cursor = conn.cursor()
    cursor.execute(query)
    count = cursor.fetchall()
    conn.commit()
    return count

def lambda_handler(event, context):
    connection = make_conn()
    if connection == None:
        return {
            'statusCode': 200,
            'body': json.dumps("Connection Failed")
        }
    
    queryData = fetch_data(connection, "SELECT * FROM \"Employees\" WHERE first_name = 'George'")
    insertedNum = query_data(connection, "INSERT INTO \"Employees\" (first_name, last_name, role) VALUES ('Test', 'User', 'Test') RETURNING id;")
    modifyedRow = query_data(connection, "UPDATE \"Employees\" SET role = 'Python Star' WHERE first_name = 'Test' RETURNING id;")
    return {
        'statusCode': 200,
        'body': json.dumps("Success")
    }

