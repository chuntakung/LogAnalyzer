# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 15:37:13 2018
@author: kung_c

=============================== EDIT HISTORY ==================================
DATE        INITIAL     CONTENTS
===============================================================================
20180822    ck          initial version
20180903    ck          added extraction of RTW layer disconnection events
20180907    ck          plotting of rtw disconnection using plotly and matplotpy
20180917    ck          added plots and annotations in all layers
"""

import plotly
import plotly.plotly as py
import plotly.offline as po
po.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import matplotlib.pyplot as plt

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
        self.wpas_connection_evt = []
        self.wsm_connection_evt = []
        self.restSDK_connection_evt = []
        self.dhcp_failure_evt = []
        self.ifdu_evt = []
        self.cannot_ping_gateway_evt = []
        self.parse_disconnections()
        self.evt_types = ['rtw', 'wpa_supplicant', 'WifiStateMachine', 'restsdk']
    
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
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.rtw_connection_evt.append({'index':i, 'connection_status':0})
            elif ("cfg80211_rtw_connect(wlan0)" in obj[MsgStats.MSG_COL]) or \
                ("rtw_cfg80211_indicate_connect" in obj[MsgStats.MSG_COL]) or \
                ("Start to Connection" in obj[MsgStats.MSG_COL]):
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.rtw_connection_evt.append({'index':i, 'connection_status':1})
            elif ("CTRL-EVENT-DISCONNECTED" in obj[MsgStats.MSG_COL]):
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.wpas_connection_evt.append({'index':i, 'connection_status':0})
            elif ("CTRL-EVENT-CONNECTED" in obj[MsgStats.MSG_COL]):
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.wpas_connection_evt.append({'index':i, 'connection_status':1})
            elif ("processMsg: DisconnectedState" in obj[MsgStats.MSG_COL]) or \
                ("new state=DISCONNECTED" in obj[MsgStats.MSG_COL]):
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.wsm_connection_evt.append({'index':i, 'connection_status':0})
            elif ("processMsg: ConnectedState" in obj[MsgStats.MSG_COL]) or \
                ("new state=CONNECTED" in obj[MsgStats.MSG_COL]):
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.wsm_connection_evt.append({'index':i, 'connection_status':1})
            elif ("wifi disconnected" in obj[MsgStats.MSG_COL] and \
                "restsdk" in obj[MsgStats.MSG_COL]):
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.restSDK_connection_evt.append({'index':i, 'connection_status':0})
            elif ("wifi connected" in obj[MsgStats.MSG_COL] and \
                "restsdk" in obj[MsgStats.MSG_COL]):
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.restSDK_connection_evt.append({'index':i, 'connection_status':1})
            elif "DHCP FAILURE" in obj[MsgStats.MSG_COL]:
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.dhcp_failure_evt.append({'index':i})
            elif "Starting service 'ifdu(0)" in obj[MsgStats.MSG_COL]:
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.ifdu_evt.append({'index':i})
            elif "Cannot ping gateway" in obj[MsgStats.MSG_COL]:
                print("dbg: {0} ==> {1}".format(i, obj[MsgStats.MSG_COL]))
                self.cannot_ping_gateway_evt.append({'index':i})

        self.rtw_connection_evt.sort(key=lambda x: x['index'])
        self.wpas_connection_evt.sort(key=lambda x: x['index'])
        self.wsm_connection_evt.sort(key=lambda x: x['index'])
        self.restSDK_connection_evt.sort(key=lambda x: x['index'])


    def prepare_disconnection_xy(self, evt):
        x = [ x[0] for x in self.msg_list ]
        y = []
        for i, item in enumerate(evt):
            print("dbg: {0} {1}".format(i, item))
            # interpolation
            if len(y) > 0:
                y = y + [y[-1]]*(item['index']-len(y))

            if item['connection_status'] == 0:
                # initialize
                if len(y) == 0:
                    y = [1]*item['index']

                # appened latest status
                y.append(0)
            else:
                # initialize
                if len(y) == 0:
                    y = [0]*item['index'] # TODO: check upper later message to determine

                # appened latest status
                y.append(1)

        # padding to end
        if len(y) > 0:
            y = y + [y[-1]]*(len(x)-len(y))
            return x,y,True
        else:
            return x,y,False

    def get_all_disconnection_xy_in_list(self, evt_types):
        events = []
        for item in evt_types:
            if item == 'rtw':
                events.append(self.rtw_connection_evt)
            elif item == 'wpa_supplicant':
                events.append(self.wpas_connection_evt)
            if item == 'WifiStateMachine':
                events.append(self.wsm_connection_evt)
            if item == 'restsdk':
                events.append(self.restSDK_connection_evt)                
        all_disc_xy = []
        for item in events:
            all_disc_xy.append(self.prepare_disconnection_xy(item))            
        return all_disc_xy

    def prepare_rtw_disconnection_xy(self):
        x = [ x[0] for x in self.msg_list ]
        y = None
        for i, item in enumerate(self.rtw_connection_evt):
            print("dbg: {0} {1}".format(i, item))
            # interpolation with the latest status
            if y != None:
                y = y + [y[-1]]*(item['index']-len(y))

            if item['connection_status'] == 0:
                # initialize with opposite one ?? maybe leave blank ?? 
                if y == None:
                    y = [1]*item['index']

                # appened latest status
                y.append(0)
            else:
                # initialize
                if y == None:
                    y = [0]*item['index'] # TODO: check upper later message to determine

                # appened latest status
                y.append(1)

        # padding to end
        y = y + [y[-1]]*(len(x)-len(y))
        return x,y

    def plot_disconnection_matplot(self):
        x,y = self.prepare_rtw_disconnection_xy()
        # plotting
        plt.plot(x, y,'r')
        plt.ylim(-0.5, 1.5)
        for i, item in enumerate(self.rtw_connection_evt):
            if item['connection_status'] == 0:
                plt.annotate('disconnected', xy=(x[item['index']],0), xytext=(x[item['index']], 1.2))
        plt.show() # does not matter when in interactive mode

    def plot_disconnection_plotly(self):
        xy_list = self.get_all_disconnection_xy_in_list(self.evt_types)
        trace_list = []
        evt_name = []
        for i, item in enumerate(xy_list):
            if item[2] == True:
                trace_list.append(go.Scatter(x = item[0], y = item[1]))            
                evt_name.append(self.evt_types[i])
        fig = plotly.tools.make_subplots(rows = len(trace_list), cols = 1, subplot_titles = evt_name)
        for i, tr in enumerate(trace_list):
            fig.append_trace(tr, i+1, 1)
            fig['layout']['xaxis{0}'.format(i)].update(title='time')            
        po.plot(fig, filename='disconnection.html')

    def plot_disconnection_plotly_jupyter(self):
        x,y = self.prepare_rtw_disconnection_xy()
        data = [go.Scatter(x=x, y=y)]
        fig = go.Figure(data=data)
        # plot in jupyter notebook
        po.iplot(fig, filename='disconnection.html')

    def plot_disconnection_plotly_online(self):
        x,y = self.prepare_rtw_disconnection_xy()
        data = [go.Scatter(x=x, y=y)]
        fig = go.Figure(data=data)
        py.plot(fig, filename='disconnection.html')
