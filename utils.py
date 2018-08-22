# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 15:37:13 2018
@author: kung_c

=============================== EDIT HISTORY ==================================
DATE        INITIAL     CONTENTS
===============================================================================
20180822    ck          initial version
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
    def __init__(self, msgls, msgdf):
        # statistical counts
        self.disconnection_events = 0
        self.good_disconnection_events = 0
        self.unidentified_events = 0

        # messages
        self.msg_list = msgls
        self.msg_df = msgdf

        # helper buffers to make statistics

    def count_disconnection(self):
        self.disconnection_events += 1

    def count_good_disconnection(self):
        self.good_disconnection_events += 1

    def count_unidentified_disconnection(self):
        self.unidentified_events += 1

    def make_event_statistics(self, msg, category):
        for cur_index in range(len(msg)):
            if ((category == 6 or category == 11) and 'wifi disconnected' in msg)\
                or 'OnDeAuth' in msg\
                or 'CTRL_EVENT_DISCONNECTED' in msg\
                or 'rtw_cfg80211_indicate_disconnect' in msg\
                or 'Start to Disconnect' in msg\
                or 'DHCP FAILURE' in msg:
                print("found disconnection:" + msg)
            else:
                continue

            # find_disconnection_period
            # is it roaming and the disconnection event not longer than 5 minutes?
            # is it rebooting and disconnection event not last longer than 5 minutes
            # is it triggered by ifdu and disconnection not last longer than 5 minutes
            # it it identified DHCP failure?
            # is it OnDeAuth disconnection?
            # is it connected back?