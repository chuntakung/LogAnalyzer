#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 21:35:32 2018
@author: kung_c
=============================== EDIT HISTORY ==================================
DATE        INITIAL     CONTENTS
===============================================================================
20180918    ck          initial version
"""

from sumologic import sumologic 
import time
from datetime import datetime
from datetime import timedelta

# Conditions to query 
LIMIT = 500
sumo = sumologic.SumoLogic('suVVXHRI0ZEYAb', 'M3OgHheE4wiQ74YmZkO8UHzYD33OAOe88WgGq58jaQQTeWt4Stii3sdS5iO2rxMi')
from_time = '2018-09-17T21:15:00'
to_time = '2018-09-17T22:15:00'
time_zone = 'UTC'
by_receipt_time = False
delay = 5
q = '"WifiStateMachine: setDetailed State"'

sj = sumo.search_job(q, from_time, to_time, time_zone, by_receipt_time)

status = sumo.search_job_status(sj)
while status['state'] != 'DONE GATHERING RESULTS':
    print('.')
    if status['state'] == 'CANCELLED':
        break
    time.sleep(delay)
    status = sumo.search_job_status(sj)

print(status['state'])

if status['state'] == 'DONE GATHERING RESULTS':
    count = status['messageCount']
    limit = count if count < LIMIT and count != 0 else LIMIT # compensate bad limit check
    r = sumo.search_job_messages(sj, limit=limit)


