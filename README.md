# Lwazi Web Service Project


### Technologies Used

* [VIRTUALENV] - Python Tool to create virtual environments
* [FLASK] - Micro Web Framework
* [SQL-ALCHEMY] - The Python SQL Toolkit and Object Relational Mapper
* [Flask-SQLAlchemy] - An extension for Flask that supports SQL-Alchemy
* [PSYCOPG] - Postgres Adapter for Python to access Postgres data

### Pre-requisites

Install Virtualenv
```sh
pip install virtualenv
```

Create a Flask Virtual Environment
```sh
virtualenv ~/flask-env - Creates Flask Python VM
```

To Run the Flask Virtual Environment
```sh
source ~/flask-env/bin/activate
```

Install Flask and associated libraries from requirements
```sh
pip install -r requirements.txt
```

Note: To install psycopg2 on mac, run the following: 
```sh
PATH=$PATH:[POSTGRES_HOME]/bin pip install psycopg2
```

To Install Postgres on Ubuntu:
```sh
sudo apt-get install postgresql postgresql-contrib

```

To change the password
```sh
sudo -u postgres psql postgres # login as postgres user
\password postgres
```
Here is more information to install Ubuntu [INSTALL POSTGRES ON UBUNTU]


### Edit config.py to use your own local database setting for the application and load script
```sh
database_settings = {
    "local": {
       "DATABASE":"Your database",
        "URL":"your url",
        "PASSWORD":"your password",
        "USERNAME":"your usename"
    }
}
```

### Optional Pre-requisite to start web service
To load the data from the spread sheets:
```sh
python load_and_join.py
```
To load data from your own files on your machine do the following
```sh
python load_and_join.py -t="'path/to/uber file'" 
-s="'path/to/schedule file" 
-s2="'path/to/schedule 2 file'"
```

Here is an example: 
```sh
python load_and_join.py -t="'/Users/Adetola/Uber Data 03-06-15 0105 PM.csv'" 
-s="'/Users/Adetola/WhenIworkSampleSpreadsheet.csv'" 
-s2="'/Users/Adetola/JET - Timesheets - Mar 2 - Mar 8, 2015.csv'"
```

To run the web service:
```sh
python main.py
```

Go to the links below to see the trip and schedules resources:
http://[url]:5000/trips
http://[url]:5000/schedules

http://[url]:5000/trips?[query parameter]=[query value]
http://[url]:5000/schedules?[query parameter]=[query value]


Optional query parameters are: 

page 

http://[url]/schedules?page=2

perpage
https://[url]/schedules?perpage=50&page=2

date
http://[url]/trips?date=2/28/15

starttime
http://[url]/schedules?date=3/1/15&starttime=08:00

endtime
http://[url]/schedules?date=2/1/15&starttime=00:00&endtime=12:00

drivername
http://[url]/schedules?drivername=Earnest%20Jackson
http://[url]/trips?drivername=Carolyn%20Chambers

Start Postgres
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql postgres

[VIRTUALENV]:https://virtualenv.pypa.io/en/latest/
[FLASK]:http://flask.pocoo.org/
[SQL-ALCHEMY]:http://www.sqlalchemy.org/
[Flask-SQLAlchemy]:https://pythonhosted.org/Flask-SQLAlchemy/
[POSTGRESQL]:http://www.postgresql.org/
[PSYCOPG]:http://initd.org/psycopg/
[INSTALL POSTGRES ON UBUNTU]:https://help.ubuntu.com/community/PostgreSQL
commit test
