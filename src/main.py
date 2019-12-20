from bs4 import BeautifulSoup
from urllib.request import urlopen
import codecs
import os, glob

page_nums = 90
ted_path_template = 'https://www.ted.com/talks?sort=popular&language=zh-cn&page={}'

def safe_urlopen(path):
	cnt = 0
	while True:
		try:
			return urlopen(path).read(), True
		except Exception as e:
			print(e)
			import time
			time.sleep(1)
		cnt += 1
		if cnt > 10:
			return '', False

def get_talk_names(path, name_set):
	r, ok = safe_urlopen(path)
	if not ok:
		return
	soup = BeautifulSoup(r)
	talks = soup.find_all('a')
	for i in talks:
		if i.attrs['href'].find('/talks/') == 0:
			name_set.add(i.attrs['href'])

def process_en_lines(lines):
	res, cur = [], ''
	for line in lines:
		if cur != '':
			cur += ' '
		cur += line
		if line[-1] == '\"':
			line = line[:-1]
		if line[-1] in '.?!' or (line[0] == '(' and line[-1] == ')'):
			# if cur != '(Applause)' and cur != '(Laughter)':
			# 	res.append(cur)
			res.append(cur)
			cur = ''
	if cur != '':# and cur != '(Applause)' and cur != '(Laughter)':
		res.append(cur)
	return res

def process_ch_lines(lines):
	res, cur = [], ''
	for line in lines:
		if not line:
			if cur != '':
				res.append(cur)
				cur = ''
			continue
		cur += line
		if line[-1] in '\"”':
			line = line[:-1]
		if line[-1] in '。？！.?!' or (line[0] in '(（' and line[-1] in '）)'):
			# if cur != '（掌声）' and cur != '（笑声）':
			# 	res.append(cur)
			res.append(cur)
			cur = ''
	if cur != '':# and cur != '（掌声）' and cur != '（笑声）':
		res.append(cur)
	return res


def parse_sentences(en_path, ch_path):
	print(en_path, ch_path)
	en_r, ok = safe_urlopen(en_path)
	if not ok:
		return [], []
	ch_r, ok = safe_urlopen(ch_path)
	if not ok:
		return [], []
	print('gocha!')
	en_soup = BeautifulSoup(en_r)
	ch_soup = BeautifulSoup(ch_r)
	# wtf
	en_lines, ch_lines = [], []
	for piece in list(en_soup.findAll('p'))[:-2]:
		line_items = str(piece).replace('\t', '').split('\n')[1: -1]
		line_items = process_en_lines(line_items)
		en_lines.append(line_items)
	for piece in list(ch_soup.findAll('p'))[:-2]:
		line_items = str(piece).replace('\t', '').split('\n')[1: -1]
		line_items = process_ch_lines(line_items)
		ch_lines.append(line_items)
	#wtf
	if len(en_lines) != len(ch_lines):
		print('block number different!')
		return [], []
	en_res, ch_res = [], []
	for i in range(len(en_lines)):
		if len(en_lines[i]) != len(ch_lines[i]):
			continue
		en_res += en_lines[i]
		ch_res += ch_lines[i]
	# for i in range(len(en_res)):
	# 	print(ch_res[i])
	# 	print(en_res[i])
	return en_res, ch_res

def save_talk_list(talk_list):
	str_data = '\n'.join(talk_list)
	with open('talk_list.txt', 'w') as f:
		f.write(str_data)
		f.close()

if __name__ == '__main__':
	# get talk lists
	all_talk_names = set()
	if os.path.isfile('talk_list.txt'):
		with open('talk_list.txt', 'r') as f:
			for line in f:
				all_talk_names.add(line)
			f.close()
		all_talk_names = list(all_talk_names)
	else:
		for i in range(1, page_nums):
			print('getting page {}'.format(i))
			path = ted_path_template.format(i)
			get_talk_names(path, all_talk_names)
		all_talk_names = list(all_talk_names)
		save_talk_list(all_talk_names)

	print('Have {} talks'.format(len(all_talk_names)))
	# get urls for transcript
	prefix = 'https://www.ted.com'
	suffix_en, suffix_ch = '/transcript', '/transcript?language=zh-cn'

	talk_list = [x[:-15] for x in all_talk_names]
	talk_list = [(prefix + x + suffix_en, prefix + x + suffix_ch) for x in talk_list]

	#print(talk_list)

	cnt, cur_cnt = 0, 0
	en_sentences, ch_sentences = [], []
	for talk_pair in talk_list:
		try:
			en_res, ch_res = parse_sentences(talk_pair[0], talk_pair[1])
			if len(en_res) > 0:
				en_sentences += en_res
				ch_sentences += ch_res
				while os.path.isfile('data_en{}.txt'.format(cnt)):
					cnt += 1
				filename_en = 'data_en{}.txt'.format(cnt)
				filename_ch = 'data_ch{}.txt'.format(cnt)
				# if os.path.isfile(filename_en):
				# 	continue
				str_data_en = '\n'.join(en_res)
				str_data_ch = '\n'.join(ch_res)
				with open(filename_en, 'w') as f:
					f.write(str_data_en)
					f.close()
				with open(filename_ch, 'w') as f:
					f.write(str_data_ch)
					f.close()
		except Exception as e:
			print(e)
			pass
		cur_cnt += 1
		if cur_cnt % 10 == 0:
			save_talk_list(all_talk_names[cur_cnt:])
	save_talk_list([])