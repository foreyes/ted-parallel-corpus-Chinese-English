import jieba

def split_en(s):
	s_cut = jieba.lcut(s)
	s_cut = [x for x in s_cut if x != ' ']
	return ' '.join(s_cut)

en_res, ch_res = [], []
with open('en_res.txt', 'r') as f:
	for line in f:
		s = ' '.join(line.split(' ')[1:])
		en_res.append(split_en(s))
	f.close()
with open('ch_res.txt', 'r') as f:
	for line in f:
		ch_res.append(' '.join(line.split(' ')[1:]))
	f.close()

with open('en_res_2.txt', 'w') as f:
	f.write('\n'.join(en_res))
	f.close()

with open('ch_res_2.txt', 'w') as f:
	f.write('\n'.join(ch_res))
	f.close()

print(en_res[10230])
print(ch_res[10230])
