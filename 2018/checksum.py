def fletch_sum(data):
	a = 0
	b = 0
	i = 0
	while i < len(data):
		a = (a + int(data[i:max(i+16,len(data)-1)],2)) % 65536
		b = (b + a) % 65536
		i += 16
	return (b << 16) | a

#makes the packet given binary sequence number and data (expected to be binary strings)
#checksum used is 32-bit Fletcher checksum
#returns binary packet (binary string)
def makepkt(data,seqnum):
	sn = seqnum
	chksum = bin(fletch_sum(data))
	packet = '0b'

	packet = packet + sn[2:len(sn)]
	packet = packet + data[2:len(data)]
	packet = packet + chksum[2:len(chksum)]

	return packet