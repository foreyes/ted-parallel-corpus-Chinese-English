import os, jieba

def process_ch(line):
	return ' '.join(jieba.lcut(line))

en_res, ch_res = [], []
path_root = 'corpus/'
idx = -1
while idx < 3000:
	idx += 1
	print(idx)
	en_file = path_root + 'data_en{}.txt'.format(idx)
	ch_file = path_root + 'data_ch{}.txt'.format(idx)
	if not os.path.isfile(en_file) or not os.path.isfile(ch_file):
		continue
	en_items, ch_items = [], []
	with open(en_file, 'r') as f:
		en_items = f.read().split('\n')
		f.close()
	with open(ch_file, 'r') as f:
		ch_items = f.read().split('\n')
		f.close()
	# print(len(en_items), len(ch_items))
	if len(en_items) == len(ch_items):
		en_res += en_items
		ch_res += ch_items
	# print(len(en_res))
	# break

en_res = [str(i) + ' ' + en_res[i] for i in range(len(en_res))]
ch_res = [str(i) + ' ' + process_ch(ch_res[i]) for i in range(len(ch_res))]

en_data = '\n'.join(en_res)
ch_data = '\n'.join(ch_res)
with open('en_res.txt', 'w') as f:
	f.write(en_data)
with open('ch_res.txt', 'w') as f:
	f.write(ch_data)