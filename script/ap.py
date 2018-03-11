#!/usr/bin/python

from pprint import pprint;
import argparse, os, re, sys
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "pyroute2"))
from pyroute2.netlink import *
from pyroute2.iwutil import IW
from pyroute2.netlink.nl80211 import *

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="count", default=0)
parser.add_argument("-l", "--list", action="count", help="list interfaces", default=0)
parser.add_argument('cmds', nargs='*', default=[])
opts = parser.parse_args()

cmds = opts.cmds;
if len(cmds) < 1:
    exit(0);

iw = IW()
ifaces = {}; desc = []
for q in iw.get_interfaces_dump():
    phyname = 'phy%i' % int(q.get_attr('NL80211_ATTR_WIPHY'))
    ifname = q.get_attr('NL80211_ATTR_IFNAME');
    mac = q.get_attr('NL80211_ATTR_MAC');
    desc.append('%s\t%s\t%s\t%s' % (q.get_attr('NL80211_ATTR_IFINDEX'), phyname,
                                    ifname, mac))
    i = { 'NL80211_ATTR_WIPHY': int(q.get_attr('NL80211_ATTR_WIPHY')),
          'NL80211_ATTR_IFINDEX' : q.get_attr('NL80211_ATTR_IFINDEX'),
          'NL80211_ATTR_IFNAME' : ifname,
          'NL80211_ATTR_MAC' : mac };
    ifaces[ifname] = i;
    ifaces[phyname] = i;
    ifaces[mac] = i;
    iw.close()

if cmds[0] == 'list':
    print("\n".join(desc))
    exit(0)
elif cmds[0] == 'ap':
    if len(cmds) < 2:
        exit(0);
    if not (cmds[1] in ifaces):
        print("Unknown iface " + cmds[1])
    iface = ifaces[cmds[1]]
else:
    print("Usage: [list|ap]"); exit(1);

seqcnt = 0;
def seq():
    global seqcnt
    seqcnt = seqcnt + 1;
    return seqcnt

WIPHY   = iface['NL80211_ATTR_WIPHY']
IFINDEX = iface['NL80211_ATTR_IFINDEX']
IFNAME  = iface['NL80211_ATTR_IFNAME']
MAC     = iface['NL80211_ATTR_MAC']

##########################################################

def msgheader(cmd,flags):
    msg = nl80211cmd()
    msg['header']['flags'] = flags
    msg['header']['pid'] = os.getpid()
    msg['header']['type'] = 26
    msg['cmd'] = cmd;
    return msg

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
        # query
        print ("query")
        msg = msgheader(NL80211_NAMES['NL80211_CMD_NEW_WIPHY'], NLM_F_REQUEST | NLM_F_ACK );
        msg['attrs'] = [['NL80211_ATTR_WIPHY_NAME', 'nl80211']];
        #pprint(msg);
        r = self.nlm_request(msg, msg_type=16, msg_flags=NLM_F_REQUEST | NLM_F_ACK);
        pprint(r);

        print ("new whi")
        msg = msgheader(NL80211_NAMES['NL80211_CMD_NEW_WIPHY'], NLM_F_REQUEST | NLM_F_ACK);
        msg['attrs'] = [['NL80211_ATTR_WIPHY_NAME', 'nlctrl']];
        r = self.nlm_request(msg, msg_type=16, msg_flags=NLM_F_REQUEST | NLM_F_ACK);
        pprint(r);

        return
    
        # delete keyslots
        print ("delete keyslots")
        msg = msgheader(NL80211_NAMES['NL80211_CMD_DEL_KEY'], NLM_F_REQUEST | NLM_F_ACK);
        msg['attrs'] = [['NL80211_ATTR_IFINDEX', IFINDEX], ['NL80211_ATTR_KEY_IDX', '00']];
        r = self.nlm_request(msg, msg_type=26, msg_flags=NLM_F_REQUEST | NLM_F_ACK);

        # start beacon
        print ("start beacon")
        msg = msgheader(NL80211_NAMES['NL80211_CMD_START_AP'], NLM_F_REQUEST | NLM_F_ACK);
        msg['attrs'] = [('NL80211_ATTR_IFINDEX', IFINDEX),
                        ('NL80211_ATTR_BEACON_HEAD', '80:00:00:00:ff:ff:ff:ff:ff:ff:f4:f2:6d:1c:df:6a:f4:f2:6d:1c:df:6a:00:00:00:00:00:00:00:00:00:00:64:00:01:04:00:0a:68:6f:73:74:61:70:50:61:73:73:01:08:82:84:8b:96:0c:12:18:24:03:01:06'),
                        ('NL80211_ATTR_BEACON_TAIL', '2a:01:04:32:04:30:48:60:6c:7f:08:00:00:00:02:00:00:00:40'),
                        ('NL80211_ATTR_BEACON_INTERVAL', '64:00:00:00'),
                        ('NL80211_ATTR_DTIM_PERIOD', '02:00:00:00'),
                        ('NL80211_ATTR_SSID', 'hostapPass'),
                        ('NL80211_ATTR_HIDDEN_SSID', '00:00:00:00'),
                        ('NL80211_ATTR_SMPS_MODE', '00:00:00:00'),
                        ('NL80211_ATTR_IE', '7f:08:00:00:00:02:00:00:00:40'),
                        ('NL80211_ATTR_IE_PROBE_RESP', '7f:08:00:00:00:02:00:00:00:40'),
                        ('NL80211_ATTR_IE_ASSOC_RESP', '7f:08:00:00:00:02:00:00:00:40')];
        self.nlm_request(msg, msg_type=26, msg_flags=NLM_F_REQUEST | NLM_F_ACK);

        # set bss
        print ("set bss")
        msg = msgheader(NL80211_NAMES['NL80211_CMD_SET_BSS'], NLM_F_REQUEST | NLM_F_ACK);
        msg['attrs'] = [('NL80211_ATTR_IFINDEX', IFINDEX),
                        ('NL80211_ATTR_BSS_CTS_PROT', '00'),
                        ('NL80211_ATTR_BSS_SHORT_PREAMBLE', '00'),
                        ('NL80211_ATTR_BSS_SHORT_SLOT_TIME', '01'),
                        ('NL80211_ATTR_AP_ISOLATE', '00'),
                        ('NL80211_ATTR_BSS_BASIC_RATES', '02:04:0b:16')];
        self.nlm_request(msg, msg_type=26, msg_flags=NLM_F_REQUEST | NLM_F_ACK);




ap = AP()
ap.startap();
