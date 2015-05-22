__author__ = 'Adetola'


import psycopg2
import argparse
import StringIO
from config import database_settings

DEFAULT_TRIP_FILE = "\'/Users/Adetola/Documents/Ade Labs/Uber Data 03-06-15 0105 PM.csv\'"
DEFAULT_SCHEDULE_FILE = "\'/Users/Adetola/Documents/Ade Labs/WhenIworkSampleSpreadsheet.csv\'"
ANOTHER_SCHEDULE_FILE = "\'/Users/Adetola/Documents/Ade Labs/JET - Timesheets - Mar 2 - Mar 8, 2015.csv\'"
DEFAULT_OUTPUT_FILE ="\'/Users/Adetola/Documents/Ade Labs/uberwithscheduledata.csv\'"

settings = database_settings["local"]

database_str = "dbname=%s user=%s password=%s host=%s port=5432" \
               % (settings["DATABASE"],settings["USERNAME"],
                  settings["PASSWORD"], settings["URL"])

conn = psycopg2.connect(database_str)

cur = conn.cursor()

def copy_lines_to_table(columns, csv_file, table):


    csv_file.readline()

    lines = csv_file.readlines()
    for line in lines:
        # print line
        line = StringIO.StringIO(line)
        line.seek(0)
        # print line

        cur.copy_from(line, table, sep=',', null='', columns=columns)
    conn.commit()


def create_trip_table(csv_file):

    # create table 1
    try:

        # check if a table is available
        cur.execute('select table_name from information_schema.tables where table_name = \'trip\'')

        # if available then drop table
        if cur.fetchone() != None:
            cur.execute('drop TABLE trip');
            conn.commit()

        cur.execute('CREATE TABLE trip \
    ( \
        id            SERIAL, \
        \"drivername\"        VARCHAR(255), \
        type       VARCHAR(255),\
        date          timestamp, \
        tripDate         timestamp, \
        tripTime TIME, \
        dateTime   timestamp, \
        tripDuration   int, \
        dayOfWeek VARCHAR(255), \
        description VARCHAR(255), \
        trip VARCHAR(255), \
        grossFare	money, \
        toll money, \
        misc	VARCHAR(255), \
        other	VARCHAR(255), \
        meterRate	money, \
        gratuity	money, \
        commission	money, \
        taxOnFee	money, \
        totalPayment money, \
        decimal_grossfare decimal(10,2), \
        decimal_commission decimal(10,2),  \
        decimal_totalpayment decimal(10,2) \
    );')

        conn.commit()

    except psycopg2.ProgrammingError as e:

        print 'relation "Trip" already exists'


    columns = (
    'drivername', 'type', 'date', 'tripDate', 'tripTime', 'dateTime', 'tripDuration', 'dayOfWeek', 'description',
    'trip', 'grossFare', 'toll', 'misc', 'other', 'meterRate', 'gratuity', 'commission', 'taxOnFee', 'totalPayment')

    csv_file = open(DEFAULT_TRIP_FILE.replace("'", ""), 'r')

    # load csv data into table 1
    copy_lines_to_table(columns, csv_file, "trip")

    # set decimal columns with money columns
    cur.execute('update trip '
                'set decimal_grossfare = grossfare, '
                'decimal_commission = commission, '
                'decimal_totalpayment = totalpayment')
    conn.commit()


def copy_data_csv():
    # Open and close the file so that the file is created
    file = open(DEFAULT_OUTPUT_FILE.replace("'", ""), 'w')
    file.close()
    # join table 1 and table 2 and output to csv file
    copy_to_csv_statement = 'COPY ' \
                            '(select distinct on (u.id) u.*, t.day, t.starttime, t.endtime, t.hourlyrate, t.laborcost, t.location, t.notes,' \
                            ' t."position", t.site,  t.totalhours, t.unpaidbreak ' \
                            'from Trip as u join Schedule as t on u.drivername = t.drivername and u.tripdate = t.scheduledate' \
                            ' and u.dayOfWeek = t.dayOfWeek)' \
                            'To ' + DEFAULT_OUTPUT_FILE + '' \
                                                          'With CSV HEADER;'
    cur.execute(copy_to_csv_statement)
    conn.commit()


def create_schedule_table(csv_file):

    # create table 2
    try:
        cur.execute('select table_name from information_schema.tables where table_name = \'schedule\'')
        if cur.fetchone() != None:
            cur.execute('drop TABLE schedule');
            conn.commit()

        cur.execute('CREATE TABLE Schedule ( \
        id SERIAL,\
       scheduledate DATE,\
        "drivername" VARCHAR(255),\
        day int, \
       dayOfWeek VARCHAR(255), \
       position VARCHAR(255), \
       location VARCHAR(255), \
       site VARCHAR(255), \
       startTime Time, \
       endTime Time, \
       unpaidBreak int, \
       totalHours   int, \
        hourlyRate	money, \
        laborCost	money, \
        notes VARCHAR(255), \
        decimal_hourlyrate decimal(10,2), \
        decimal_laborcost decimal(10,2),\
        decimal_total decimal(10,2)\
    );')


    except psycopg2.ProgrammingError as e:

        print 'relation "Schedule" already exists'
    conn.commit()
    # load csv data into table 2
    copy_csv_file_statement = """COPY Schedule (scheduledate,drivername,day,dayOfWeek,position,location,site,""" \
              """startTime,endTime, unpaidBreak, totalHours, hourlyRate, laborCost, notes) FROM""" \
              """ ' + csv_file + ' WITH CSV HEADER;"""
    # print copy_csv_file_statement


    columns = (
        'scheduledate', 'drivername', 'day', 'dayOfWeek', 'position', 'location', 'site', 'startTime', 'endTime',
        'unpaidBreak', 'totalHours', 'hourlyRate', 'laborCost', 'notes')

    csv_file = open(DEFAULT_SCHEDULE_FILE.replace("'", ""), 'r')

    copy_lines_to_table(columns, csv_file, "schedule")

    # set decimal columns with money columns
    cur.execute('update Schedule '
                'set decimal_hourlyrate = hourlyrate, '
                'decimal_laborcost = laborcost')
    conn.commit()




def create_schedule_clocked_table(csv_file):

    # create table 3
    try:
        cur.execute('CREATE TABLE ScheduleClocked ( \
        id            SERIAL,\
       date          timestamp,\
        firstname VARCHAR(255),\
        lastname VARCHAR(255),\
        "drivername"        VARCHAR(255),\
       position VARCHAR(255), \
       location VARCHAR(255), \
       site VARCHAR(255), \
       startTime Time, \
       endTime Time, \
        length decimal(5,2), \
        hourlyRate	money, \
        total	money, \
        laborCost	money, \
        notes VARCHAR(255), \
        userId VARCHAR(255), \
        positionId VARCHAR(255), \
        locationId VARCHAR(255), \
        employeeId VARCHAR(255), \
        decimal_hourlyrate decimal(10,2), \
        decimal_total decimal(10,2)\
    );')

    except psycopg2.ProgrammingError as e:

        print 'relation "ScheduleClocked" already exists'
    conn.commit()


    cur.execute('copy ScheduleClocked ( date, firstname,lastname, position, location,'
                'site, startTime, endTime, length, hourlyRate, total, notes,'
                'userId,positionId, locationId, employeeId) from ' +
                csv_file +
                ' WITH CSV HEADER');
    conn.commit()
    cur.execute('update ScheduleClocked '
                'set drivername = concat(firstname , \' \' , lastname), '
                'decimal_hourlyrate = hourlyrate, '
                'decimal_total = total')
    conn.commit()








# # join table 1 and table 2 and output to another table
# try:
#     cur.execute('create table TripScheduled as '
#                 '(select t.day, t.endtime, t.hourlyrate, t.laborcost, t.location, t.notes, t."position",'
#                 ' t.site, t.starttime, t.totalhours, t.unpaidbreak, u.* '
#                 'from Trip as u join Schedule as t on u.drivername = t.drivername and u.date = t.date)')
#
# except psycopg2.ProgrammingError as e:
#
#     print 'relation "TripScheduled" already exists'
#
#     # copy data instead
#
# conn.commit()





def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--trip_file', dest='trip_file', default=DEFAULT_TRIP_FILE, type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-s', '--schedule_file', dest='schedule_file', default=DEFAULT_SCHEDULE_FILE, type=str, help='Search location (default: %(default)s)')
    parser.add_argument('-s2', '--schedule_file_2', dest='another_schedule_file', default=ANOTHER_SCHEDULE_FILE, type=str, help='Search location (default: %(default)s)')

    parser.add_argument('-o', '--output_file', dest='output_file', default=DEFAULT_OUTPUT_FILE, type=str, help='Search location (default: %(default)s)')



    input_values = parser.parse_args()

    # create_trip_table(input_values.trip_file)
    # create_schedule_table(input_values.schedule_file)
    copy_data_csv()
    # create_schedule_clocked_table(input_values.another_schedule_file)

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
