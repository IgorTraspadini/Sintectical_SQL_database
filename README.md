# About the Project

In some tasks we need a simple database with a large quantity of data to perform some labs or optimization tests,        
however to find it in the internet is not soo easy, the size of the file is soo large or need to be converted to a         
specific format.       

Intended to solve this issue, I've created this project that I'll using after to perform some [optimization tasks and 
best practices in SQL querry](https://github.com/IgorTraspadini/SQL_Optimization).

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
- Faker   18.7.0
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

'''
check if the tables were created on the database

    Table name
0   Address
1      City
2   Country
3  Customer

check the tables structure"

Customer
cid       name     type  notnull dflt_value  pk
0  customer_id  INTEGER        1       None   1
1         Name     TEXT        0       None   0
2   Address_id  INTEGER        0       None   0
3        Email     TEXT        0       None   0
4        Phone     TEXT        0       None   0
5          Job     TEXT        0       None   0
6      Company     TEXT        0       None   0

Address
cid      name     type  notnull dflt_value  pk
0  Address_id  INTEGER        1       None   1
1     Address     TEXT        0       None   0
2     Zipcode     TEXT        0       None   0
3     City_id  INTEGER        0       None   0
4        City     TEXT        0       None   0
5  Country_id  INTEGER        0       None   0
6     Country     TEXT        0       None   0

City
cid   name     type  notnull dflt_value  pk
0  City_id  INTEGER        1       None   1
1     City     TEXT        0       None   0

Country
cid      name     type  notnull dflt_value  pk
0  Country_id  INTEGER        1       None   1
1     Country     TEXT        0       None   0
'''
```
### Populate the tables
```python
# It will created just one hundred of records in order to test it.
# later it will be populated with 2M of data.
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
```
### Normalize the database
```Python
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
```
### Check the database
Customer Table
|customer_id|              Name|Address_id|                      Email|  Phone           |   Job                     |  Company         |
|:---------:|:----------------:|:--------:|:-------------------------:|:----------------:|:-------------------------:|:----------------:| 
|          0|     Kevin Sanders|       100| christinamills@example.com| 260-962-0765x7932|Loss adjuster, chartered   | Jordan Inc       |
|          1|      Justin Patel|       101|  victoriahogan@example.org|    3637991023    | Engineer, aeronautical    |Harris, White & Mc| 
|          2|Matthew Hughes Jr.|       102|  jonesadrienne@example.com| (742)425-3943x211| Further education lecturer|Hubbard-Navarro   |

Address Table
|Address_id|                                          Address  | Zipcode| City_id | Country_id |  
|:--------:|:-------------------------------------------------:|:------:|:-------:|:----------:|
|       100|           687 Denise Creek\nJohnsonmouth, NH 48492|   49306|        0|           0| 
|       101|  6159 Lindsey Islands Suite 946\nHughestown, MN...|   95586|        1|           1|
|       102|                           USS Howard\nFPO AE 68571|   35641|        2|           2|

City Table                            
|City_id|        City      |          
|:-----:|:----------------:|           
|      0|   New Derricktown|          
|      1|      Rayborough  |          
|      2| North Andrewbury |          

Country Table
|Country_id|     Country      |
|:--------:|:----------------:|
|         0|Puerto Rico       |
|         1|Russian Federation|
|         2|  Ukraine         |

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
