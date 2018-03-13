#!/usr/bin/python
from pprint import pprint;
import argparse, os, re, sys
import os, sys, time
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
        wiphy = r[0]['attrs'][2][1] # 'NL80211_ATTR_WIPHY'
        print(" > wiphy: %d" %(wiphy))

        print("Proto featires")
        msg = nl80211cmd()
        msg['cmd'] = NL80211_CMD_GET_PROTOCOL_FEATURES;
        msg['attrs'] = [];
        r = self.nlm_request(msg, msg_type=28, msg_flags=NLM_F_REQUEST | NLM_F_ACK);
        pprint(r);

        print("Get wiphy")
        msg = nl80211cmd()
        msg['cmd'] = NL80211_CMD_GET_WIPHY;
        msg['attrs'] = [['NL80211_ATTR_IFINDEX', ifindex], ['NL80211_ATTR_SPLIT_WIPHY_DUMP', '']];
        r = self.nlm_request(msg, msg_type=28, msg_flags=NLM_F_REQUEST | NLM_F_ACK | NLM_F_DUMP);
        pprint(r);

        print("Get iface")
        msg = nl80211cmd()
        msg['cmd'] = NL80211_CMD_GET_INTERFACE;
        msg['attrs'] = [['NL80211_ATTR_IFINDEX', ifindex]];
        r = self.nlm_request(msg, msg_type=28, msg_flags=NLM_F_REQUEST | NLM_F_ACK );
        pprint(r);

        print("Set iface")
        msg = nl80211cmd()
        msg['cmd'] = NL80211_CMD_SET_INTERFACE;
        msg['attrs'] = [['NL80211_ATTR_IFINDEX', ifindex],['NL80211_ATTR_IFTYPE', 3]];
        r = self.nlm_request(msg, msg_type=28, msg_flags=NLM_F_REQUEST | NLM_F_ACK );
        pprint(r);
        time.sleep(1)

        #for i in [ 'b0:00', '00:00', '20:00', 'a0:00', 'c0:00', 'd0:00', '40:00']:
        print("Register Actions %d" %(ifindex))
        msg = nl80211cmd()
        msg['cmd'] = NL80211_CMD_REGISTER_FRAME;
        msg['attrs'] = [['NL80211_ATTR_IFINDEX', ifindex],['NL80211_ATTR_FRAME_TYPE', 'b0:00'],['NL80211_ATTR_FRAME_MATCH', '']];
        r = self.nlm_request(msg, msg_type=28, msg_flags=NLM_F_REQUEST | NLM_F_ACK );
        pprint(r);

        # NL80211_CMD_UNEXPECTED_FRAME

        print("Register beacon")
        msg = nl80211cmd()
        msg['cmd'] = NL80211_CMD_REGISTER_BEACONS;
        msg['attrs'] = [['NL80211_ATTR_WIPHY', wiphy]];
        r = self.nlm_request(msg, msg_type=28, msg_flags=NLM_F_REQUEST | NLM_F_ACK );
        pprint(r);

        print("Start ap")
        msg = nl80211cmd()
        msg['cmd'] = NL80211_CMD_START_AP;
        msg['attrs'] = [['NL80211_ATTR_IFINDEX', ifindex],
                        ['NL80211_ATTR_BEACON_HEAD', '80:00:00:00:ff:ff:ff:ff:ff:ff:f4:f2:6d:1c:df:6a:f4:f2:6d:1c:df:6a:00:00:00:00:00:00:00:00:00:00:64:00:01:04:00:0a:68:6f:73:74:61:70:50:61:73:73:01:08:82:84:8b:96:0c:12:18:24:03:01:06'],
                        ['NL80211_ATTR_BEACON_TAIL', '2a:01:04:32:04:30:48:60:6c:7f:08:00:00:00:02:00:00:00:40'],
                        ['NL80211_ATTR_BEACON_INTERVAL', '64:00:00:00'],
                        ['NL80211_ATTR_DTIM_PERIOD', '02:00:00:00'],
                        ['NL80211_ATTR_SSID', 'hostapPass'],
                        ['NL80211_ATTR_HIDDEN_SSID', '00:00:00:00'],
                        ['NL80211_ATTR_SMPS_MODE', '00:00:00:00'],
                        ['NL80211_ATTR_IE', '7f:08:00:00:00:02:00:00:00:40'],
                        ['NL80211_ATTR_IE_PROBE_RESP', '7f:08:00:00:00:02:00:00:00:40'],
                        ['NL80211_ATTR_IE_ASSOC_RESP', '7f:08:00:00:00:02:00:00:00:40']]

        r = self.nlm_request(msg, msg_type=28, msg_flags=NLM_F_REQUEST | NLM_F_ACK );
        pprint(r);






        return
