 - Using a TP-LINK TL-WN722N usb wifi dongle
 - start unencrypted AP with tracing:

    nltrace -d /tmp hostapd hostapd_no.conf 2>&1 | tee log.txt
    
 


hostapd_no.conf (replace interface with your ifname):

    cat hostapd_no.conf
    interface=wlxf4f20d1cda6a
    driver=nl80211
    ssid=hostapPass
    hw_mode=g
    channel=6
    macaddr_acl=0
    auth_algs=3
    ignore_broadcast_ssid=0
    wpa=0

