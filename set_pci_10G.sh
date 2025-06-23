cat /lib/modules/$(uname -r)/modules.dep |grep myr

rmmod myri10ge

modprobe myri10ge

lsmod |grep myri

ifconfig ens4 down
ifconfig ens4 up 
sleep 1s
ifconfig ens4 192.168.5.10

#sudo ifconfig eth1 192.168.5.2 255.255.255.0 up  #solo para roach_mspec

lspci -nn | grep -i net

sysctl -w net.core.wmem_max=838860800
sysctl -w net.core.rmem_max=838860800
sysctl -w net.core.rmem_default=819260800
sysctl -w net.ipv4.udp_rmem_min=8192000

ifconfig ens4
