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

    class NoIface(Exception):
        pass
    
    def __init__(self, opts, *argv, **kwarg):
        self.opts = opts;
        
        groups = None
        async = False

        # align groups with async
        if groups is None:
            groups = ~0 if async else 0

        # continue with init
        super(AP, self).__init__(*argv, **kwarg)
        self.bind(groups, async)

    def startap(self, ifindex=-1):
        
        if (ifindex == -1):
            
            n = None;
            if isinstance(self.opts.iface,str):
                n = self.opts.iface
            elif len(self.opts.args) > 0:
                n = self.opts.args.pop(0)
            try:
                from pyroute2.iwutil import IW
                iw = IW()
                for q in iw.get_interfaces_dump():
                    ifname = q.get_attr('NL80211_ATTR_IFNAME');
                    phyname = 'phy%i' % int(q.get_attr('NL80211_ATTR_WIPHY'))
                    if ifname == n or phyname == n:
                        ifindex = q.get_attr('NL80211_ATTR_IFINDEX')
                        break
            finally:
                pass

        if ifindex == -1:
            raise AP.NoIface();
            
        print("Get interfaces")
        msg = nl80211cmd()
        msg['cmd'] = NL80211_CMD_GET_INTERFACE;
        msg['attrs'] = [['NL80211_ATTR_IFINDEX', ifindex]];
        r = self.nlm_request(msg, msg_type=28, msg_flags=NLM_F_REQUEST | NLM_F_ACK);
        pprint(r);
        
        return
    


