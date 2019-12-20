en_res, ch_res = [], []
with open('en_res_2.txt', 'r') as f:
	for line in f.read().split('\n'):
		if line == '':
			continue
		en_res.append(line)
	f.close()
with open('ch_res_2.txt', 'r') as f:
	for line in f.read().split('\n'):
		if line == '':
			continue
		ch_res.append(line)
	f.close()

s1, s2= 2000, 4000

with open('en_0.txt', 'w') as f:
	f.write('\n'.join(en_res[:s1]))
	f.close
with open('ch_0.txt', 'w') as f:
	f.write('\n'.join(ch_res[:s1]))
	f.close
with open('en_1.txt', 'w') as f:
	f.write('\n'.join(en_res[s1:s2]))
	f.close
with open('ch_1.txt', 'w') as f:
	f.write('\n'.join(ch_res[s1:s2]))
	f.close
with open('en_2.txt', 'w') as f:
	f.write('\n'.join(en_res[s2:]))
	f.close
with open('ch_2.txt', 'w') as f:
	f.write('\n'.join(ch_res[s2:]))
	f.close