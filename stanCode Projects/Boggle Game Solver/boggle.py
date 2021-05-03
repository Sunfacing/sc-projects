"""
File: boggle.py
Name: Ko Wei CHEN
----------------------------------------
This file will play the boggle game by a recursive approach
and return the results if found any and return how many can be found
"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'


def main():
	"""
	TODO: This program asks user to set up the 4 x 4 grid of boggle board, and loop every grid as starting point, then return results
	"""
	row_n = 1
	lst = [[], [], [], []]
	while row_n != 5:
		row = input(f'{row_n} row of letters: ')
		for i in range(len(row)):
			if i % 2 == 1 and row[i] != ' ' or len(row) != 7 or row[i].isdigit():
				print('Illegal Format')
				return "1"
			elif i % 2 == 0:
				char = row[i].lower()
				lst[row_n - 1].append(char)
		row_n += 1

	ans_lst = []
	for i in range(4):
		for j in range(4):
			boggle_finder(lst, i, j, [], ans_lst)
	print(ans_lst)
	print(f'There are {len(ans_lst)} words in total')


def boggle_finder(lst, row, col, word_index_lst, ans_lst):
	"""
	:param lst: list, boggle grid input by user
	:param row: int, the row where the point is
	:param col: int, the col where the point is
	:param word_index_lst: lst of [row, col], store the path the program passes
	:return: ans_lst, stores all the found words
	"""
	if len(word_index_lst) >= 3 and not has_prefix(lst, word_index_lst):
		return
	else:
		if len(word_index_lst) >= 4 and has_prefix(lst, word_index_lst) == 'match':
			ans = ''
			for position in word_index_lst:
				p_row = int(position[0])
				p_col = int(position[1])
				ans += lst[p_row][p_col]
			if ans not in ans_lst:
				ans_lst.append(ans)
				print(f'Found "{ans}"')

	if [row, col] in word_index_lst:
		pass
	else:
		word_index_lst.append([row, col])
		for k in range(-1, 2):
			for l in range(-1, 2):
				if 0 <= row + k <= 3 and 0 <= col + l <= 3:
					boggle_finder(lst, row + k, col + l, word_index_lst, ans_lst)
		word_index_lst.pop()


def read_dictionary():
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	with open(FILE, 'r') as f:
		return [line[:-1] for line in f]


def has_prefix(sub_s, sub_i):
	"""
	:param dict_: a dictionary for matching boggle
	:param sub_i: a list contains the index of each character in sub_s
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	dict_ = read_dictionary()
	ans = ''
	for position in sub_i:
		row = int(position[0])
		col = int(position[1])
		ans += sub_s[row][col]

	# Slicing Dictionary for faster searching
	if ans[0] in ['a', 'b', 'c', 'd']:
		sliced_dict = dict_[:34133]
	elif ans[0] in ['e', 'f', 'g', 'h']:
		sliced_dict = dict_[34133:53822]
	elif ans[0] in ['i', 'j', 'k', 'l']:
		sliced_dict = dict_[53822:65484]
	elif ans[0] in ['m', 'n', 'o', 'p']:
		sliced_dict = dict_[65484:88509]
	elif ans[0] in ['q', 'r', 's', 't']:
		sliced_dict = dict_[88509:117646]
	else:
		sliced_dict = dict_[117646:]

	for word in sliced_dict:
		if word.startswith(ans):
			if word == ans:
				return 'match'
			return True
	return False


if __name__ == '__main__':
	main()
