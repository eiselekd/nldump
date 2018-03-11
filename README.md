Variouse snippets for netlink debugging

nltrace (toplevel)
=======

nltrace [ -d packet-save-dir ] prog ...


Netlink packet decoder script/decoder.py
========================================

python script/decoder.py  filename

Where filename is generated via nltrace or a patched strace.
Filename has to be of format nl_[0-9]_[0-9]_[snd|rec] where
the first number is an index, the second number is the netlink protocol.
pyroute2 needs to be installed. use

   pip[3] install pytoute2


Modified strace
===============

Patched version of strace in under directory strace-4.15.
It will dump netlink packets under /tmp/nl* . If the option -n prog
is given then [prog file] is called when a netlink packet is discovered.

   ./strace -n "python script/decoder.py" ip -6 route

Build on Ubuntu:

   cd strace-4.15; DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage -us -uc -nc

Example:

```c

execve("/sbin/ip", ["ip", "-6", "route"], [/* 34 vars */]) = 0
brk(NULL)                               = 0x55700a572000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=128455, ...}) = 0
mmap(NULL, 128455, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f9304914000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libdl.so.2", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\220\16\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=14632, ...}) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f9304912000
mmap(NULL, 2109712, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f9304509000
mprotect(0x7f930450c000, 2093056, PROT_NONE) = 0
mmap(0x7f930470b000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x7f930470b000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\340\22\2\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0755, st_size=1960656, ...}) = 0
mmap(NULL, 4061792, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f9304129000
mprotect(0x7f93042ff000, 2097152, PROT_NONE) = 0
mmap(0x7f93044ff000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1d6000) = 0x7f93044ff000
mmap(0x7f9304505000, 14944, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f9304505000
close(3)                                = 0
mmap(NULL, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f930490f000
arch_prctl(ARCH_SET_FS, 0x7f930490f740) = 0
mprotect(0x7f93044ff000, 16384, PROT_READ) = 0
mprotect(0x7f930470b000, 4096, PROT_READ) = 0
mprotect(0x55700a1c4000, 8192, PROT_READ) = 0
mprotect(0x7f9304934000, 4096, PROT_READ) = 0
munmap(0x7f9304914000, 128455)          = 0
socket(AF_NETLINK, SOCK_RAW|SOCK_CLOEXEC, NETLINK_ROUTE) = 3
setsockopt(3, SOL_SOCKET, SO_SNDBUF, [32768], 4) = 0
setsockopt(3, SOL_SOCKET, SO_RCVBUF, [1048576], 4) = 0
bind(3, {sa_family=AF_NETLINK, nl_pid=0, nl_groups=00000000}, 12) = 0
getsockname(3, {sa_family=AF_NETLINK, nl_pid=637, nl_groups=00000000}, [12]) = 0
{'attrs': [('RTA_UNSPEC', None),
           ('UNKNOWN', {'header': {'length': 8, 'type': 29}})],
 'cmd': 'RTM_GETROUTE',
 'dst_len': 0,
 'family': 10,
 'flags': 0,
 'header': {'flags': '0x301|NLM_F_REQUEST|NLM_F_DUMP',
            'length': 40,
            'pid': 0,
            'sequence_number': 1520777548,
            'type': 26},
 'proto': 0,
 'scope': 0,
 'src_len': 0,
 'table': 0,
 'tos': 0,
 'type': 0}
sendto(3, {{len=40, type=0x1a /* NLMSG_??? */, flags=NLM_F_REQUEST|0x300, seq=1520777548, pid=0}, "\n\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\10\0\35\0\1\0\0\0"}, 40, 0, NULL, 0) = 40
recvmsg(3, {'attrs': [('RTA_TABLE', 254),
           ('RTA_DST', '::1'),
           ('RTA_PRIORITY', 256),
           ('RTA_OIF', 1),
           ('RTA_CACHEINFO', {'rta_error': 0, 'rta_id': 0, 'rta_expires': 0, 'rta_ts': 0, 'rta_lastuse': 1000238, 'rta_tsage': 0, 'rta_used': 0, 'rta_clntref': 1}),
           ('RTA_PREF', '00')],
 'cmd': 'RTM_NEWROUTE',
 'dst_len': 128,
 'family': 10,
 'flags': 0,
 'header': {'flags': '0x2|NLM_F_MULTI',
            'length': 116,
            'pid': 637,
            'sequence_number': 1520777548,
            'type': 24},
 'proto': 2,
 'scope': 0,
 'src_len': 0,
 'table': 254,
 'tos': 0,
 'type': 2}
{'attrs': [('RTA_TABLE', 254),
           ('RTA_DST', 'fe80::'),
           ('RTA_PRIORITY', 256),
           ('RTA_OIF', 4),
           ('RTA_CACHEINFO', {'rta_error': 0, 'rta_id': 0, 'rta_expires': 0, 'rta_ts': 0, 'rta_lastuse': 998370, 'rta_tsage': 0, 'rta_used': 0, 'rta_clntref': 1}),
           ('RTA_PREF', '00')],
 'cmd': 'RTM_NEWROUTE',
 'dst_len': 64,
 'family': 10,
 'flags': 0,
 'header': {'flags': '0x2|NLM_F_MULTI',
            'length': 116,
            'pid': 637,
            'sequence_number': 1520777548,
            'type': 24},
 'proto': 2,
 'scope': 0,
 'src_len': 0,
 'table': 254,
 'tos': 0,
 'type': 1}
{'attrs': [('RTA_TABLE', 255),
           ('RTA_DST', '::1'),
           ('RTA_PRIORITY', 0),
           ('RTA_OIF', 1),
           ('RTA_CACHEINFO', {'rta_error': 0, 'rta_id': 0, 'rta_expires': 0, 'rta_ts': 0, 'rta_lastuse': 988158, 'rta_tsage': 0, 'rta_used': 15, 'rta_clntref': 6}),
           ('RTA_PREF', '00')],
 'cmd': 'RTM_NEWROUTE',
 'dst_len': 128,
 'family': 10,
 'flags': 0,
 'header': {'flags': '0x2|NLM_F_MULTI',
            'length': 116,
            'pid': 637,
            'sequence_number': 1520777548,
            'type': 24},
 'proto': 2,
 'scope': 0,
 'src_len': 0,
 'table': 255,
 'tos': 0,
 'type': 2}
{'attrs': [('RTA_TABLE', 255),
           ('RTA_DST', 'fe80::6a60:3431:b8a7:db12'),
           ('RTA_PRIORITY', 0),
           ('RTA_OIF', 1),
           ('RTA_CACHEINFO', {'rta_error': 0, 'rta_id': 0, 'rta_expires': 0, 'rta_ts': 0, 'rta_lastuse': 998184, 'rta_tsage': 0, 'rta_used': 3, 'rta_clntref': 3}),
           ('RTA_PREF', '00')],
 'cmd': 'RTM_NEWROUTE',
 'dst_len': 128,
 'family': 10,
 'flags': 0,
 'header': {'flags': '0x2|NLM_F_MULTI',
            'length': 116,
            'pid': 637,
            'sequence_number': 1520777548,
            'type': 24},
 'proto': 2,
 'scope': 0,
 'src_len': 0,
 'table': 255,
 'tos': 0,
 'type': 2}
{'attrs': [('RTA_TABLE', 255),
           ('RTA_DST', 'ff00::'),
           ('RTA_PRIORITY', 256),
           ('RTA_OIF', 4),
           ('RTA_CACHEINFO', {'rta_error': 0, 'rta_id': 0, 'rta_expires': 0, 'rta_ts': 0, 'rta_lastuse': 849, 'rta_tsage': 0, 'rta_used': 2269, 'rta_clntref': 5}),
           ('RTA_PREF', '00')],
 'cmd': 'RTM_NEWROUTE',
 'dst_len': 8,
 'family': 10,
 'flags': 0,
 'header': {'flags': '0x2|NLM_F_MULTI',
            'length': 116,
            'pid': 637,
            'sequence_number': 1520777548,
            'type': 24},
 'proto': 3,
 'scope': 0,
 'src_len': 0,
 'table': 255,
 'tos': 0,
 'type': 1}
{msg_name={sa_family=AF_NETLINK, nl_pid=0, nl_groups=00000000}, msg_namelen=12, msg_iov=[{iov_base=[{{len=116, type=0x18 /* NLMSG_??? */, flags=NLM_F_MULTI, seq=1520777548, pid=637}, "\n\200\0\0\376\2\0\2\0\0\0\0\10\0\17\0\376\0\0\0\24\0\1\0\0\0\0\0\0\0\0\0"...}, {{len=116, type=0x18 /* NLMSG_??? */, flags=NLM_F_MULTI, seq=1520777548, pid=637}, "\n@\0\0\376\2\0\1\0\0\0\0\10\0\17\0\376\0\0\0\24\0\1\0\376\200\0\0\0\0\0\0"...}, {{len=116, type=0x18 /* NLMSG_??? */, flags=NLM_F_MULTI, seq=1520777548, pid=637}, "\n\200\0\0\377\2\0\2\0\0\0\0\10\0\17\0\377\0\0\0\24\0\1\0\0\0\0\0\0\0\0\0"...}, {{len=116, type=0x18 /* NLMSG_??? */, flags=NLM_F_MULTI, seq=1520777548, pid=637}, "\n\200\0\0\377\2\0\2\0\0\0\0\10\0\17\0\377\0\0\0\24\0\1\0\376\200\0\0\0\0\0\0"...}, {{len=116, type=0x18 /* NLMSG_??? */, flags=NLM_F_MULTI, seq=1520777548, pid=637}, "\n\10\0\0\377\3\0\1\0\0\0\0\10\0\17\0\377\0\0\0\24\0\1\0\377\0\0\0\0\0\0\0"...}, {{len=0, type=0 /* NLMSG_??? */, flags=0, seq=0, pid=0}}], iov_len=32768}], msg_iovlen=1, msg_controllen=0, msg_flags=0}, 0) = 580
fstat(1, {st_mode=S_IFIFO|0600, st_size=0, ...}) = 0
brk(NULL)                               = 0x55700a572000
brk(0x55700a593000)                     = 0x55700a593000
access("/proc/net", R_OK)               = 0
access("/proc/net/unix", R_OK)          = 0
socket(AF_UNIX, SOCK_DGRAM|SOCK_CLOEXEC, 0) = 4
ioctl(4, SIOCGIFNAME, {ifr_index=4, ifr_name="wlp3s0"}) = 0
close(4)                                = 0
write(1, "fe80::/64 dev wlp3s0 proto kerne"..., 58fe80::/64 dev wlp3s0 proto kernel metric 256  pref medium
) = 58
recvmsg(3, {'cmd': 0,
 'header': {'flags': '0x2|NLM_F_MULTI',
            'length': 20,
            'pid': 637,
            'sequence_number': 1520777548,
            'type': 3},
 'reserved': 0,
 'version': 0}
{msg_name={sa_family=AF_NETLINK, nl_pid=0, nl_groups=00000000}, msg_namelen=12, msg_iov=[{iov_base=[{{len=20, type=NLMSG_DONE, flags=NLM_F_MULTI, seq=1520777548, pid=637}, "\0\0\0\0"}, {{len=33555198, type=0 /* NLMSG_??? */, flags=0, seq=983048, pid=254}, "\24\0\1\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\1\10\0\6\0\0\1\0\0\10\0\4\0"...}], iov_len=32768}], msg_iovlen=1, msg_controllen=0, msg_flags=0}, 0) = 20
exit_group(0)                           = ?
+++ exited with 0 +++


```
