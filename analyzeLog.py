# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 22:20:58 2018
@author: kung_c

=============================== EDIT HISTORY ==================================
DATE        INITIAL     CONTENTS
===============================================================================
20180822    ck          initial version
20180903    ck          added db time constraints, rowcount display,
                        datetime inclusion
"""

import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
from datetime import timedelta
import utils
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
    print(err)
else:
  print(logtag+"Connected to sumodb successfully")
  cursor = cnx.cursor()


#==============================================================================
# download data of interest from db
#==============================================================================
db = "sumodb"
tb = "`00:14:ee:0c:6e:f2`"
since_day = (datetime.today().date()-timedelta(days=1)).strftime("'%Y-%m-%d'")
since = "'2018-8-31'"
limit = 500000
query = "SELECT raw,sourcecategory,mtime FROM {0}.{1} where mtime >= {2}".format(db,tb, since)
print (logtag + "trying to query with command:\t"+ query)

cursor.execute(query)
query_ret = cursor.fetchall()

print (logtag + "%d rows returned from database" % (cursor.rowcount))

#==============================================================================
# parse message time and content
# store into data structure pandas.dataframe
#==============================================================================
parsing_start = time.clock()

date_position_end = 10
time_position_end = 23
column_name = ['data-time', 'date', 'time', 'category', 'message']
msgls = [] # [[datatime, date, time, category, msg], ...]
for line in query_ret:
    msg_date_time = line[2]
    msgdate = msg_date_time.date()
    msgtime = msg_date_time.time()
    msg = utils.extract_content(line[0][time_position_end+1:])
    msgls.append([msg_date_time, msgdate, msgtime, line[1], msg])
msg_stat = utils.MsgStats(msgls)
msg_stat.plot_disconnection()
#msg_stat.print_msg()

parsing_end = time.clock()
print ("time elapsed for parsing " + str(parsing_end - parsing_start))





