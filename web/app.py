from flask import Flask, jsonify
from urllib2 import urlopen
import collections
import psycopg2
import stringcase
import json
import re

app = Flask(__name__)

conn = None

def get_db():
	global conn
	if conn is None:
		conn = connect_db()
	return conn

def connect_db():
	global conn
	conn = psycopg2.connect(database="postgres", user = "postgres", host = "postgres", port = "5432")

def check_table():
	db = get_db()
	cur = db.cursor()
	cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('netskope_data',))
	if cur.fetchone()[0] is True:
		print ("Inside alrealy existing!")
	else:
		cur.execute("CREATE TABLE netskope_data (ID INT PRIMARY KEY NOT NULL, DATA TEXT NOT NULL)")
		print ("Table created successfully!")
	db.commit()

def get_db_data():
	db = get_db()
	cur = db.cursor()
	cur.execute("SELECT * FROM netskope_data")
	result = convert_to_sentencecase(cur.fetchone()[1])
	return result

def convert_to_camelcase(s): 
    if(len(s) == 0): 
        return
    s1 = '' 
    s1 += s[0].upper() 
    for i in range(1, len(s) - 1): 
        if (s[i] == ' '): 
            s1 += s[i + 1].upper() 
            i += 1
        elif(s[i - 1] != ' '): 
            s1 += s[i]  
    return s1

def convert_to_snakecase(s):
	if(len(s) == 0): 
		return
	s1 = '' 
	for i in range(0, len(s) - 1): 
		if (s[i] == ' '): 
			s1 +='_'
		else: 
			s1 += s[i].lower()  
	return s1

def convert_to_sentencecase(s):
	if(len(s) == 0): 
		return
	s1 = '' 
	for i in range(0, len(s) - 1): 
		if (s[i] == '_'): 
			s1 +=' '
		else: 
			s1 += s[i]  
	return s1

@app.teardown_appcontext
def close_db(error):
    if conn is not None:
        conn.close()
        conn = None

@app.route('/import')
def import_data():
	txt = urlopen("http://dataservice/harrypotter").read()
	text = txt.replace('\'', "''")
	db = get_db()
	try:
		cur = db.cursor()
		cur.execute("INSERT INTO netskope_data (ID,DATA) VALUES (1, '"+convert_to_snakecase(text)+"')");
	except:
		print("Failed to insert as the data already exists!")
	finally:
		db.commit()

	abb = convert_to_camelcase(txt)
	obj = {"result":abb}
	return jsonify(obj)

@app.route('/wordscount')
def words_count():
	result = get_db_data()
	words = collections.Counter()
	words.update(result.split())
	d = {}                              
	for word, count in words.iteritems():
	    d[word] = count
	obj = {"result":d}	
	return jsonify(obj)

@app.route('/wordcount/<word>')
def words(word):
	result = get_db_data()
	count = sum(1 for match in re.finditer(r"\b"+word+r"\b", result))

	obj = {"result":count}
	return jsonify(obj)

@app.route('/matchword/<pattern>')
def pattern(pattern):
	result = get_db_data()
	words = set()
	for word in result.split():
		if pattern in word:
			words.add(word)
	obj = {"result":list(words)}
	return jsonify(obj)

if __name__ == '__main__':
	connect_db()
	check_table()
	app.run(debug=True,host='0.0.0.0')