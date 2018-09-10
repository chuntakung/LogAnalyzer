# -*- coding: utf-8 -*-
"""
Created on Sun Sep 9 17:50:50 2018
@author: kung_c

=============================== EDIT HISTORY ==================================
DATE        INITIAL     CONTENTS
===============================================================================
20180909    ck          initial version
"""

from datetime import datetime
from datetime import timedelta
import utils
import time
import csv


logtag = "ParseLog: "
#==============================================================================
# export data from csv
#==============================================================================
parsing_start = time.clock()

column_name = ['data-time', 'date', 'time', 'message']
msgls = []
with open("sample_6ef2.csv", 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        msg_date_time = row[0]
        msgdate = msg_date_time.date()
        msgtime = msg_date_time.time()        
        msg = msg[1]
        msgls.append([msg_date_time, msgdate, msgtime, msg])
        
parsing_end = time.clock()
print ("time elapsed for parsing " + str(parsing_end - parsing_start))

msg_stat = utils.MsgStats(msgls)
msg_stat.plot_disconnection_plotly()







