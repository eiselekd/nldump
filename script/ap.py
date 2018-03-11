#!/usr/bin/python
from pprint import pprint;
import argparse, os, re, sys
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "pyroute2"))

from pyroute2.netlink import *
from pyroute2.iwutil import IW
from pyroute2.netlink.nl80211 import *

##########################################################

class AP(NL80211):
    def __init__(self, *argv, **kwarg):
        # get specific groups kwarg
        if 'groups' in kwarg:
            groups = kwarg['groups']
            del kwarg['groups']
        else:
            groups = None

        # get specific async kwarg
        if 'async' in kwarg:
            async = kwarg['async']
            del kwarg['async']
        else:
            async = False

        # align groups with async
        if groups is None:
            groups = ~0 if async else 0

        # continue with init
        super(AP, self).__init__(*argv, **kwarg)

        # do automatic bind
        # FIXME: unfortunately we can not omit it here
        self.bind(groups, async)


    def startap(self):

        msg = nl80211cmd()
        msg['cmd'] = NL80211_CMD_NEW_WIPHY;
        msg['attrs'] = [['NL80211_ATTR_WIPHY_NAME', 'nlctrl']];
        r = self.nlm_request(msg, msg_type=16, msg_flags=NLM_F_REQUEST | NLM_F_ACK);
        pprint(r);

        return
    


