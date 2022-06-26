import psycopg2

con = psycopg2.connect("postgres://postgres:postgrespw@localhost:49153")

cur = con.cursor()

cur.execute('''CREATE TABLE test."test" ("id" serial PRIMARY KEY, "name" text);''')

con.commit()
