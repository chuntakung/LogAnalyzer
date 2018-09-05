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

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

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

        plotly.tools.set_credentials_file(username='chuntakung', api_key='bEecqEVf7mXmdWQJr75g')

        # statistical counts
        self.disconnection_events = 0
        self.good_disconnection_events = 0
        self.unidentified_events = 0

        # messages
        self.msg_list = msgls
        self.msg_list.sort(key=lambda x: x[0])

        # disconnection periods
        self.rtw_connection_evt = []
        self.wpas_disconnections = []
        self.WSM_disconnections = []
        self.restSDK_disconnections = []
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
                self.rtw_connection_evt.append({'index':i, 'connection_status':0})
            elif ("cfg80211_rtw_connect(wlan0)" in obj[MsgStats.MSG_COL]) or \
                ("rtw_cfg80211_indicate_connect" in obj[MsgStats.MSG_COL]) or \
                ("Start to Connection" in obj[MsgStats.MSG_COL]):
                print("{0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.rtw_connection_evt.append({'index':i, 'connection_status':1})

    def print_msg(self):
        print(self.msg_list)

    def plot_disconnection(self):
        x = [ x[0] for x in self.msg_list ]
        y = [0]* len(x)
        for i, x in enumerate(self.msg_list):
            if i in self.rtw_connection_evt:
                y[i] = 0
            elif i in self.rtw_connection_evt:
                y[i] = 1
        data = [go.Scatter(x=x, y=y)]
        fig = go.Figure(data=data)
        py.iplot(fig)


