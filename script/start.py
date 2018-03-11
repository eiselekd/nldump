#!/usr/bin/python

import argparse, os, re, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "pyroute2"))
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from pyroute2.netlink import *
from pyroute2.iwutil import IW
from pyroute2.netlink.nl80211 import *

from ap import AP;

ifaces = {}; desc = []

def start_ap():
    ap = AP()
    #ap.startap();

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-l", "--list", action="count", help="list interfaces", default=0)
    parser.add_argument('cmds', nargs='*', default=[])
    opts = parser.parse_args()
    
    cmds = opts.cmds;
    if len(cmds) < 1:
        exit(0);


    def getifaces():
        global ifaces, desc
        iw = IW()
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
        getifaces();
        print("\n".join(desc))
        exit(0)
    elif cmds[0] == 'ap':
        if len(cmds) < 2:
            exit(0);
            #if not (cmds[1] in ifaces):
            #    print("Unknown iface " + cmds[1])
            #iface = ifaces[cmds[1]]
        start_ap();
            
    else:
        print("Usage: [list|ap]"); exit(1);


if __name__ == "__main__":
    main()
    
