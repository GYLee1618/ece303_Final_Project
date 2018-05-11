import math
import struct
import hashlib

def fixlength(number,length):
	if len(number) - 2 < length:
		number = bytearray((length - len(number)) * [0]) + number[0:len(number)]
	return number

#computes the 32-bit Fletchers's checksum of the data
#data is expected to be a binary string
#output is a binary string
'''
def fletch_sum(data):
	a = 0
	b = 0
	i = 0
	while i < len(data):
		a = (a + data[i] << 24 + data[i+1] << 16 + data[i+2] << 8 + data[i+3] ) % 65535
		b = (b + a) % 65535
		i += 4
	x = (b << 16) + a
	return bytearray.fromhex('{:08x}'.format(x))
'''
def checkpkt(data):
	act_data = data[0:-16]	#-32 for checksum and -1 for count from 0

	rcv_chksum = data[-16:len(data)]

	comp_chksum = bytearray.fromhex((hashlib.md5(act_data).hexdigest()))

	return (comp_chksum == rcv_chksum) #If the checksum that was recieved matches the one generated from the received data then we are ready to roll.

#makes the packet given binary sequence number and data (expected to be binary strings)
#checksum used is 32-bit Fletcher checksum
#returns binary packet (binary string)	
def makepkt(data,seqnum):
	packet = seqnum + data

	#hksum = hashlib.md5(packet)
	
	packet = packet + bytearray.fromhex((hashlib.md5(packet).hexdigest()))

	return packet


def data_splitter(data,packet_size):
	packets = [data[i:i+packet_size] for i in range(0,len(data),packet_size)]
	if len(packets[-1]) < packet_size:
		packets[-1] =  packets[-1] + bytearray([4]) + bytearray([0]) * (packet_size-len(packets[-1])-1)
	return packets

def ba_to_int(ba):
	it = 0
	for i in range(len(ba)-1,-1):
		it += it + 256**(len(it)-1-i)*signal_length_b[i]
	return it	

def data_to_packets(data,packet_size,max_seqnum):
	packets = data_splitter(data,packet_size)
	send_pkts = []
	seqnum = 0
	for packet in packets:
		send_pkts.append(makepkt(packet,bytearray.fromhex('{:06x}'.format(seqnum))))
		seqnum = (seqnum + 1) % max_seqnum	
	return send_pkts

if __name__ == '__main__':
	st = raw_input('Message: ')
	bst = bytearray(st)

	pkts = data_to_packets(bst,18,64)
	print list(pkts[0])
	print checkpkt(pkts[0])
	pkts[1][6] = 1
	print list(pkts[1])
	print checkpkt(pkts[1])

