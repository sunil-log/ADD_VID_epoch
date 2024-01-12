
"""
Tartget 을 제외한 나머지를 모음
"""

from glob import glob
import numpy as np



def concat_except_AB(subs, dir_source):
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


	# save
	np.save(f"{dir_source}/timeseries_train.npy", train_X)
	np.save(f"{dir_source}/label_train.npy", train_y)
	np.save(f"{dir_source}/timeseries_val.npy", valid_X)
	np.save(f"{dir_source}/label_val.npy", valid_y)

def load_half_data(sub_dir):

	npy_train_X = np.load(f"{sub_dir}/timeseries_train.npy")
	npy_train_y = np.load(f"{sub_dir}/label_train.npy")
	npy_valid_X = np.load(f"{sub_dir}/timeseries_val.npy")
	npy_valid_y = np.load(f"{sub_dir}/label_val.npy")

	index_half = int(npy_train_X.shape[0] / 2)
	npy_train_X1 = npy_train_X[:index_half]
	npy_train_X2 = npy_train_X[index_half:]
	npy_train_y1 = npy_train_y[:index_half]
	npy_train_y2 = npy_train_y[index_half:]

	index_half = int(npy_valid_X.shape[0] / 2)
	npy_valid_X1 = npy_valid_X[:index_half]
	npy_valid_X2 = npy_valid_X[index_half:]
	npy_valid_y1 = npy_valid_y[:index_half]
	npy_valid_y2 = npy_valid_y[index_half:]


	d = {
		"train_1_X": npy_train_X1,
		"train_1_y": npy_train_y1,
		"train_2_X": npy_train_X2,
		"train_2_y": npy_train_y2,

		"valid_1_X": npy_valid_X1,
		"valid_1_y": npy_valid_y1,
		"valid_2_X": npy_valid_X2,
		"valid_2_y": npy_valid_y2,
	}

	return d











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

		# concat except sub_A (save source)
		concat_except_AB(subs, dir_source)
		exit()














if __name__ == '__main__':
	main()