#computes the 32-bit Fletchers's checksum of the data
#data is expected to be a binary string
#output is a binary string
def fletch_sum(data):
	a = 0
	b = 0
	i = 0
	while i < len(data):
		a = (a + int(data[i:max(i+16,len(data)-1)],2)) % 65536
		b = (b + a) % 65536
		i += 16
	return bin((b << 16) | a)

#makes the packet given binary sequence number and data (expected to be binary strings)
#checksum used is 32-bit Fletcher checksum
#returns binary packet (binary string)
def makepkt(data,seqnum):
	sn = seqnum
	chksum = fletch_sum(data)
	packet = '0b'

	packet = packet + sn[2:len(sn)]
	packet = packet + data[2:len(data)]
	packet = packet + chksum[2:len(chksum)]

	return packet

def data_splitter(data,packet_size):
	packets = [data[i:i+packet_size] for i in range(2,len(data),packet_size)]
	return packets

def data_to_packets(data,packet_size,max_seqnum):
	packets = data_splitter(data,packet_size)
	send_pkts = []
	seqnum = 0
	for packet in packets:
		send_pkts.append(makepkt(packet,bin(seqnum)))
		seqnum = (seqnum + 1) % max_seqnum
	return send_pkts

print data_to_packets(bin(123456789876543210123456789876543210123456789876543210123456789876543210123456789876543210123456789876543210),16,16)