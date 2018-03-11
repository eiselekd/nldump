#!/usr/bin/python

import argparse, os, re, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "pyroute2"))
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from pyroute2.netlink import *
from pyroute2.iwutil import IW
from pyroute2.netlink.nl80211 import *
from pprint import pprint;

from ap import AP;

ifaces = {}; desc = []


def main():
    global opts
    
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

    def do_list(opts):
        getifaces();
        print("\n".join(desc))
        exit(0)

    def do_ap(opts):
        ap = AP(opts)
        ap.startap();

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-l", "--list", action="count", help="list interfaces", default=0)

    subparsers = parser.add_subparsers(help='sub-commands help')
    
    # create the parser for the "list" command
    parser_list = subparsers.add_parser('list', help='list interface indexes')
    parser_list.set_defaults(func=do_list)
    
    # create the parser for the "ap" command
    parser_ap = subparsers.add_parser('ap', help='accesspoint help')
    parser_ap.add_argument('--ifindex', help='force ifindex', default=-1)
    parser_ap.add_argument('--iface', help='interface name', default=None)
    parser_ap.add_argument('args', nargs='*')
    parser_ap.set_defaults(func=do_ap)
    
    opts = parser.parse_args()

    try:
        opts.func(opts);
    except AP.NoIface:
        print("Inferface needed:")
        do_list(opts)
    


if __name__ == "__main__":
    main()
    
