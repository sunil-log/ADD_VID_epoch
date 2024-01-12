

import numpy as np

from glob import glob
from utils.dir_manage import recreate_directory
import os

def balanced_sampling_indices(arr, classes):
	"""
	주어진 배열에서 각 클래스의 개수를 균등하게 맞추기 위한 샘플링 인덱스를 반환합니다.

	Parameters:
	arr: numpy array
		샘플링할 대상이 되는 NumPy 배열입니다.
	classes: list
		균등하게 샘플링할 클래스의 리스트입니다.

	Returns:
	List
		균등하게 샘플링된 인덱스의 리스트입니다.
	"""
	indices = []
	min_count = min([np.sum(arr == c) for c in classes])
	for c in classes:
		c_indices = np.where(arr == c)[0]
		c_sampled_indices = np.random.choice(c_indices, min_count, replace=False)
		indices.extend(c_sampled_indices)
	return sorted(indices)


def main():

	"""
	CDA 용 1:1:1 training validation set

	저장된 npz 변수:
		np.savez(new_fn, X=epoch_data, y=label_data)
	"""

	# specify directories
	npz_dir = "crop_raw_fif"
	cda_dir = "add_cda_red_A"
	recreate_directory(cda_dir)


	# fid npzs
	fns = sorted(glob(f"{npz_dir}/*.npz"))

	# for all npzs
	for i, fn in enumerate(fns):
		print(f"processing...: {fn}")

		# load npz
		npz = np.load(fn)
		X = npz['X']
		y = npz['y']
		"""
		X.shape: (480, 65, 500)
		y.shape: (480,)
		
		Target shape
			timeseries_train.shape = (batch_size, 128, 3) = (batch, ts, dimension)
			label_train.shape = (batch_size,)
		"""

		# reshape X into (batch, ts, dimension)
		X = X.transpose((0, 2, 1))      # X.shape: (480, 500, 65)

		# even sampling
		sampled_indices = balanced_sampling_indices(y, [0, 1, 2])
		X = X[sampled_indices]
		y = y[sampled_indices]

		# number of samples
		idx_split = int(X.shape[0] * 0.8)
		X_train = X[:idx_split]
		X_val = X[idx_split:]
		y_train = y[:idx_split]
		y_val = y[idx_split:]
		"""
		X_train.shape: (76, 500, 65)
		y_train.shape: (76,)
		X_val.shape: (20, 500, 65)
		y_val.shape: (20,)
		"""

		# save npy
		dir_subject = f"{cda_dir}/subject_{i}"
		if not os.path.exists(dir_subject):
			os.mkdir(dir_subject)

		np.save(f"{dir_subject}/timeseries_train.npy", X_train)
		np.save(f"{dir_subject}/label_train.npy", y_train)

		np.save(f"{dir_subject}/timeseries_val.npy", X_val)
		np.save(f"{dir_subject}/label_val.npy", y_val)

		np.save(f"{dir_subject}/timeseries_test.npy", X_val)
		np.save(f"{dir_subject}/label_test.npy", y_val)


if __name__ == '__main__':
	main()