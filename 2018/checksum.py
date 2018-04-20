def fletch_sum(data):
	a = 0
	b = 0
	i = 0
	while i < len(data):
		a = (a + int(data[i:max(i+16,len(data)-1)],2)) % 65536
		b = (b + a) % 65536
		i += 16
	return (b << 16) | a