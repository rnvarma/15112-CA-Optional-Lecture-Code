import psycopg2

#Make sure to create a database using the psql application!
db = "livedemo" #Database with this name must exist!
user = "postgres"
password = "postgres"

conn = psycopg2.connect(database=db, user=user, password=password)
conn.autocommit = True
cur = conn.cursor()
print("Connected!")
#Get rid of a table in the DB
def drop():
	query = """DROP TABLE students;"""
	cur.execute(query)
drop()

#Create a table students within livedemo DB
def create():
	query = """CREATE TABLE students(andrew_id varchar, age int);"""
	cur.execute(query)

create()

#Insert andrew_ids and age into table students
def insertion(andrew_id, age):
	query = """
	INSERT INTO students VALUES(%s, %s)
	"""
	args = (andrew_id, age)
	cur.execute(query, args)
	print("yahoo!")

insertion("jstapins", 19)

#Livedemo has one table -> students
#Show everything
def selectAll():
	query = """
	SELECT *
	FROM students;
	"""
	cur.execute(query)
	results = cur.fetchall()
	print(results)


selectAll()


#Show where age = something
#Hint brackets for numbers!
def selectAge(age):
	query = """
	SELECT andrew_id
	FROM students
	WHERE age = %s;
	"""
	cur.execute(query, [age])
	results = cur.fetchall()
	print(results)

selectAge(19)

def updateAge(oldAge, newAge):
	query = """
	UPDATE students
	SET age = %s
	WHERE age = %s;
	"""
	args = (newAge, oldAge)
	cur.execute(query, args)
	print("Done")

updateAge(19, 20)
selectAll()
