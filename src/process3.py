en_voc, ch_voc = set(), set()
with open('en_res_2.txt', 'r') as f:
	for line in f.read().split('\n'):
		for word in line.split(' '):
			if word != '':
				en_voc.add(word)
	f.close()
with open('ch_res_2.txt', 'r') as f:
	for line in f.read().split('\n'):
		for word in line.split(' '):
			if word != '':
				ch_voc.add(word)
	f.close()

en_voc_list = ['<unk>', '<s>', '</s>'] + list(en_voc)
ch_voc_list = ['<unk>', '<s>', '</s>'] + list(ch_voc)

print(ch_voc_list[:1000])

with open('en_voc.txt', 'w') as f:
	f.write('\n'.join(en_voc_list))
	f.close()
with open('ch_voc.txt', 'w') as f:
	f.write('\n'.join(ch_voc_list))
	f.close()