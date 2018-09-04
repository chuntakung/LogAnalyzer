# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 15:37:13 2018
@author: kung_c

=============================== EDIT HISTORY ==================================
DATE        INITIAL     CONTENTS
===============================================================================
20180822    ck          initial version
20180903    ck          added extraction of RTW layer disconnection events
"""

#==============================================================================
# function to extract message content
#==============================================================================
def extract_content(raw_uni):
    """extract_content from raw unicode message
    """
    index1 = raw_uni.find('==>')
    index2 = raw_uni.find(':')
    if(index1 == -1 or index2 < index1):
        return raw_uni[index2+2:]
    else:
        return raw_uni[index1+4:]

class MsgStats:
    """ Class used to store statistical data for message
    """
    DATETIME_COL = 0
    DATE_COL = 1
    TIME_COL = 2
    CATEGORY_COL = 3
    MSG_COL = 4

    def __init__(self, msgls):
        # statistical counts
        self.disconnection_events = 0
        self.good_disconnection_events = 0
        self.unidentified_events = 0

        # messages
        self.msg_list = msgls
        self.msg_list.sort(key=lambda x: x[0])

        # disconnection periods
        self.RTW_disconnections = []
        self.wpas_disconnections = []
        self.WSM_disconnections = []
        self.restSDK_disconnections = []
        self.RTW_connections = []
        self.parse_disconnections()

    def count_disconnection(self):
        self.disconnection_events += 1

    def count_good_disconnection(self):
        self.good_disconnection_events += 1

    def count_unidentified_disconnection(self):
        self.unidentified_events += 1

    def parse_disconnections(self):
        for i, obj in enumerate(self.msg_list):
            #print("{0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
            if ("OnDeAuth" in obj[MsgStats.MSG_COL]) or \
                ("cfg80211_rtw_disconnect(wlan0)" in obj[MsgStats.MSG_COL]) or \
                ("rtw_cfg80211_indicate_disconnect" in obj[MsgStats.MSG_COL]) or \
                ("Start to Disconnect" in obj[MsgStats.MSG_COL]):
                print("{0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.RTW_disconnections.append([i,obj[MsgStats.DATETIME_COL]])
            elif ("cfg80211_rtw_connect(wlan0)" in obj[MsgStats.MSG_COL]) or \
                ("rtw_cfg80211_indicate_connect" in obj[MsgStats.MSG_COL]) or \
                ("Start to Connection" in obj[MsgStats.MSG_COL]):
                print("{0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.RTW_connections.append([i,obj[MsgStats.DATETIME_COL]])

    def print_msg(self):
        print(self.msg_list)



