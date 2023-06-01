# import the library
from faker import Faker
import pandas as pd
import sqlite3

# create a instance of the faker class and set a seed to have the same behaviour
fake = Faker()
fake.seed_instance(121)

# building the database
conn = sqlite3.connect('db_test.db')
cursor = conn.cursor()

# create the tables
cursor.execute("CREATE TABLE Customer (customer_id INTEGER NOT NULL PRIMARY KEY,\
                                         Name TEXT,\
                                         Address_id INTEGER,\
                                         Email TEXT,\
                                         Phone TEXT,\
                                         Job TEXT,\
                                         Company TEXT\
                                         );")
cursor.execute("CREATE TABLE Address (Address_id INTEGER NOT NULL PRIMARY KEY,\
                                         Address TEXT,\
                                         Zipcode TEXT,\
                                         City_id INTEGER,\
                                         City TEXT,\
                                         Country_id INTEGER,\
                                         Country TEXT\
                                         );")
cursor.execute("CREATE TABLE Country (Country_id INTEGER NOT NULL PRIMARY KEY,\
                                         Country TEXT\
                                         );")
cursor.execute("CREATE TABLE City (City_id INTEGER NOT NULL PRIMARY KEY,\
                                         City TEXT\
                                         );")
conn.commit()

# function to extract the data from the database as a dataframe
def table_as_df(cursor):
    columns = [col[0] for col in cursor.description]
    return pd.DataFrame([dict(zip(columns, row)) for row in cursor.fetchall()])

# check if the tables were created on the database
print("----------------------------check if the tables were created on the database-----------------------------")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
df = table_as_df(cursor)
print(df)
Tables = [x for x in df.name]

# check the contents of the tables
print("-------------------------------------check the structure of the tables------------------------------------")
for x in Tables:
    print(x)
    cursor.execute("PRAGMA table_info({})".format(x))
    print(table_as_df(cursor))

# populate the tables
for x in range(100):
    cursor.execute("INSERT INTO Customer (customer_id, Name, Address_id, Email, Phone, Job, Company)\
                    VALUES (?,?,?,?,?,?,?)",(x,
                                        str(fake.name()),
                                        x+100,
                                        str(fake.email()),
                                        str(fake.phone_number()),
                                        str(fake.job()),
                                        str(fake.company())                                    
                                        ))
    cursor.execute("INSERT INTO Address (Address_id, Address, Zipcode, City, Country)\
                    VALUES (?,?,?,?,?)",(x+100,
                                        str(fake.address()),
                                        str(fake.zipcode()),
                                        str(fake.city()),
                                        str(fake.country()), 
                                        ))

conn.commit()

# Normalize the database
cursor.execute("SELECT DISTINCT City FROM Address")
df_city = table_as_df(cursor)
city_list = []
for a, b in enumerate(df_city.City):
    city_list.append((a, b))

cursor.execute("SELECT DISTINCT Country FROM Address")
df_country = table_as_df(cursor)
country_list = []
for a, b in enumerate(df_country.Country):
    country_list.append((a, b))

cursor.executemany("INSERT INTO City (City_id, City) VALUES(?,?)",city_list)
cursor.executemany("INSERT INTO Country (Country_id, Country) VALUES(?,?)",country_list)
cursor.executemany("UPDATE Address SET Country_id = ? WHERE Country = ?",country_list)
cursor.executemany("UPDATE Address SET City_id = ? WHERE City = ?",city_list)
cursor.execute("ALTER TABLE Address DROP COLUMN City")
cursor.execute("ALTER TABLE Address DROP COLUMN Country")
conn.commit()

# check the tables
print("-------------------------------------------------------check the tables------------------------------------------")
for x in Tables:
    print(x)
    cursor.execute("SELECT * FROM "+ x + " LIMIT 3")
    print(table_as_df(cursor))

conn.close()
