
"""
Tartget 을 제외한 나머지를 모음
"""

from glob import glob


def main():

	# find subjects
	main_dir = "add_cda_red_A"
	subjects = sorted(glob(f"{main_dir}/subject_*"))


	# for all subjects
	for sub_A in subjects:

		# extract sub_A from subjects
		subs = subjects.copy().remove(sub_A)
		print(subs)
		exit()






if __name__ == '__main__':
	main()