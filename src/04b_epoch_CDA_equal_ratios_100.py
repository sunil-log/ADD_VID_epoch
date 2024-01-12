
"""
Tartget 을 제외한 나머지를 모음
"""

from glob import glob
import numpy as np



def concat_except_AB(subs):
	"""
	Parameters
		subs: list
			모든 npy 파일이 있는 디렉토리
	Returns
		data: list
			모든 npy 파일을 load 한 list
	"""
	train_X = []
	train_y = []
	valid_X = []
	valid_y = []
	for sub in subs:
		npy_train_X = np.load(f"{sub}/timeseries_train.npy")
		npy_train_y = np.load(f"{sub}/label_train.npy")
		npy_valid_X = np.load(f"{sub}/timeseries_val.npy")
		npy_valid_y = np.load(f"{sub}/label_val.npy")

		train_X.append(npy_train_X)
		train_y.append(npy_train_y)
		valid_X.append(npy_valid_X)
		valid_y.append(npy_valid_y)

	train_X = np.concatenate(train_X, axis=0)
	train_y = np.concatenate(train_y, axis=0)
	valid_X = np.concatenate(valid_X, axis=0)
	valid_y = np.concatenate(valid_y, axis=0)
	print(f"train_X.shape: {train_X.shape}")
	print(f"train_y.shape: {train_y.shape}")
	print(f"valid_X.shape: {valid_X.shape}")
	print(f"valid_y.shape: {valid_y.shape}")


	return train_X, train_y, valid_X, valid_y




def extract_subject_index_from_dir(sub_dir):

	# extract subject index from sub_dir
	sub_index = sub_dir.split('_')[-1]
	sub_index = int(sub_index)

	return sub_index




def main():

	# find subjects
	main_dir = "add_cda_red_A"
	subjects = sorted(glob(f"{main_dir}/subject_*"))
	"""
	['add_cda_red_A/subject_0', ..., 'add_cda_red_A/subject_9']
	"""

	# for all subjects
	for sub_A in subjects:

		# print
		print(f"processing...: {sub_A}")

		# generate dirs
		sub_A_index = extract_subject_index_from_dir(sub_A)
		dir_source = f"{main_dir}/subject_{sub_A_index+100}"
		dir_target = f"{main_dir}/subject_{sub_A_index+1000}"
		print(f"dir_source: {dir_source}")
		print(f"dir_target: {dir_target}")


		# extract sub_A from subjects
		subs = subjects.copy()
		subs = [sub for sub in subs if sub != sub_A]

		# choose sub_B randomly from subs
		sub_B = np.random.choice(subs)
		subs = [sub for sub in subs if sub != sub_B]

		# load all npys in subs
		concat_except_AB(subs)










if __name__ == '__main__':
	main()