nltrace
=======

nltrace [ -d <packet-save-dir> ] <prog> ...


Netlink packet decoder script/decoder.py
========================================

python script/decoder.py <filename>

Where filename is generated via nltrace or a patched strace.
Filename has to be of format nl_[0-9]_[0-9]_[snd|rec] where
the first number is an index, the second number is the netlink protocol.
pyroute2 needs to be installed. use

   pip[3] install pytoute2


Modified strace
===============

Patched version of strace in under directory strace-4.15.
It will dump netlink packets under /tmp/nl* . If the option -n <prog>
is given then <prog> <file> is called on when a netlink packet is discovered.

   ./strace -n "python script/decoder.py" ip -6 route

Example:
