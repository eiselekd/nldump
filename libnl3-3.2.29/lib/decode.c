#include <netlink-private/netlink.h>
#include <netlink-private/socket.h>
#include <netlink-private/utils.h>
#include <netlink/netlink.h>
#include <netlink/utils.h>
#include <netlink/handlers.h>
#include <netlink/msg.h>
#include <netlink/attr.h>
#include <linux/socket.h>

static int idx = 0;

void nlmsg_decode_call(char *decode, struct nl_msg *msg, char *dir)
{
	int proto = msg->nm_protocol;
	int len = msg->nm_size;
	char b[256], cmd[256];
	sprintf(b, "/tmp/nl_%08d_%08d_%s", idx, proto, dir);
	idx++;
	FILE *f = fopen(b, "w");
	if (f) {
		fwrite((char*)msg, 1, len, f);
		fclose(f);

		sprintf(cmd, "%s %s", decode, b);
		int r = system(cmd);
		(void)r;
	}
}
