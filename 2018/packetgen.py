import math
import struct
import binascii

def fixlength(number,length):
	if len(number) - 2 < length:
		number = bytearray((length - len(number)) * [0]) + number[0:len(number)]
	return number

#computes the 32-bit Fletchers's checksum of the data
#data is expected to be a binary string
#output is a binary string
def fletch_sum(data):
	a = 0
	b = 0
	i = 0
	while i < len(data):
		a = (a + data[i]) % 65535
		b = (b + a) % 65535
		i += 16
	x = (b << 16) + a
	return bytearray.fromhex('{:08x}'.format(x))

def checkpkt(data):
	act_data = data[0:len(data)-32]	#-32 for checksum and -1 for count from 0

	rcv_chksum = data[len(data)-32:len(data)]

	comp_chksum = fletch_sum(act_data)

	return (comp_chksum == rcv_chksum) #If the checksum that was recieved matches the one generated from the received data then we are ready to roll.

#makes the packet given binary sequence number and data (expected to be binary strings)
#checksum used is 32-bit Fletcher checksum
#returns binary packet (binary string)	
def makepkt(data,seqnum):
	packet = seqnum + data

	chksum = fletch_sum(packet)

	packet = packet + chksum[0:len(chksum)]

	return packet


def data_splitter(data,packet_size):
	packets = [data[i:i+packet_size] for i in range(0,len(data),packet_size)]
	if len(packets[len(packets)-1]) < packet_size:
		packets[len(packets)-1] =  bytearray([0] * (packet_size-len(packets[len(packets)-1]))) + packets[len(packets)-1]
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
		send_pkts.append(makepkt(packet,fixlength(bytearray.fromhex('{:06x}'.format(seqnum)),int(math.ceil(math.log(max_seqnum,2))))))
		seqnum = (seqnum + 1) % max_seqnum	
	return send_pkts

if __name__ == '__main__':
	st = raw_input('Message: ')
	bst = '0b'+''.join('{0:08b}'.format(ord(x), 'b') for x in st)

	pkts = data_to_packets(bst,16,64)
	print checkpkt(pkts[0])
	thing = list(pkts[1])
	thing[6] = '1'

	pkts[1] = ''.join(thing)
	print checkpkt(pkts[1])

