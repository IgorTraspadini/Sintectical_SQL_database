# About the Project

In some tasks we need a simple database with a large quantity of data to perform some labs or optimization tests,        
however to find it in the internet is not soo easy, the size of the file is soo large or need to be converted to a         
specific format.       

Intended to solve this issue, I've created this project that I'll using after to perform some optimization tasks and 
best practices in SQL querry.

**Table of contents**
- [About the Project](#about-the-project)
- [Language](#language)
- [Library](#library)
- [Getting started](#getting-started)
- [Rum Project](#rum-project)
- [References](#references)
- [Author](#author)

## Language
- Python  3.9.12
- SQL

## Library
- Faker   x.x.x
- Pandas  2.0.1
- Sqlite  

## Getting started
- [Import the library](#import-the-library)
- [Building the database](#building-the-database)
- [Create the tables](#create-the-tables)
- [Normalize the database](#normalize-the-database)
- [Check the database](#check-the-database)

### Import the library
```python
from faker import Faker
import pandas as pd
import sqlite3

# create a instance of the faker class and set a seed to have the same behaviour
fake = Faker()
fake.seed_instance(121)
```

### Building the database
```python
# set a cursor to the database
# whether the database doesn't exist sqlite create it.
conn = sqlite3.connect('db_test.db')
cursor = conn.cursor()
``` 

### Create the tables
```python
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
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
print(table_as_df(cursor))

#       name
#0   Address
#1      City
#2   Country
#3  Customer

# check the contents on the table "Customer"
cursor.execute("PRAGMA table_info({})".format(Customer))
print(table_as_df(cursor))

#   cid         name     type  notnull dflt_value  pk
#0    0  customer_id  INTEGER        1       None   1
#1    1         Name     TEXT        0       None   0
#2    2   Address_id  INTEGER        0       None   0
#3    3        Email     TEXT        0       None   0
#4    4        Phone     TEXT        0       None   0
#5    5          Job     TEXT        0       None   0
#6    6      Company     TEXT        0       None   0

```
### Populate the tables
```python
# It will created just one hundred of records in order to test it.
# later it will be populated with 2M of data.
for x in range(10):
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



```
### Normalize the database



### Check the database

|  Name|Age|Experience|
|:----:|:-:|:--------:|
| Summy| 31|        10|
|  Anna| 30|         8|
|Amanda| 29|         4|

## Rum Project
```bash
# Clone the reposotiry 
git clone https://github.com/IgorTraspadini/Sintectical_SQL_database.git

# Import
requirements.txt

# Run the project
python sintectical_db.py
```

## References 
- [Faker Documentation](https://faker.readthedocs.io/en/master/)
- [Database normalization](https://en.wikipedia.org/wiki/Database_normalization)


## Author
[Igor Traspadini](https://www.linkedin.com/in/igor-chieppe-traspadini/?locale=en_US)
