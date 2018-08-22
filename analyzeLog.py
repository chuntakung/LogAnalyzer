# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 22:20:58 2018
@author: kung_c

=============================== EDIT HISTORY ==================================
DATE        INITIAL     CONTENTS
===============================================================================
20180822    ck          initial version
"""


import mysql.connector
from mysql.connector import errorcode
import datetime
import utils
import pandas as pd
import time


logtag = "ParseLog: "

#==============================================================================
# connect to db
#==============================================================================


try:
    cnx = mysql.connector.connect(user='root', password='123456',
                                  host='10.200.140.28', database='sumodb')
except mysql.connector.Error as err: # catching "mysql.connector.Error" exception
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print err
else:
  print(logtag+"Connected to sumodb successfully")
  cursor = cnx.cursor()


#==============================================================================
# download data of interest from db
#==============================================================================
db = "sumodb"
tb = "`00:00:c0:0b:71:bd`"
limit = 500
query = "SELECT raw,sourcecategory FROM {0}.{1} LIMIT {2}".format(db,tb,limit)
print (logtag + "trying to query with command:\t"+ query)

cursor.execute(query)

#==============================================================================
# parse message time and content
# store into data structure pandas.dataframe
#==============================================================================
msg_stat = utils.MsgStats()
parsing_start = time.clock()

date_position_end = 10
time_position_end = 23
column_name = ['date', 'time', 'category', 'message']
msgls = [] # [[date, time, category, msg], ...]
for line in cursor:
    msg_datetime_str = line[0][0:time_position_end]
    msg_date_time = datetime.datetime.strptime(msg_datetime_str,"%Y-%m-%dT%H:%M:%S.%f")
    msgdate = msg_date_time.date()
    msgtime = msg_date_time.time()
    msg = utils.extract_content(line[0][time_position_end+1:])
    msgls.append([msgdate, msgtime, line[1], msg])
msgdf = pd.DataFrame(msgls, columns=column_name)
msg_stat = msg

parsing_end = time.clock()
print "time elapsed for parsing" + str(parsing_end - parsing_start)





