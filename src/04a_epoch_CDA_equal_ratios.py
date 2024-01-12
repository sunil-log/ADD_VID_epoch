

from glob import glob
from utils.dir_manage import recreate_directory


def main():

	"""
	CDA 용 1:1:1 training validation set

	저장된 npz 변수:
		np.savez(new_fn, X=epoch_data, y=label_data)
	"""

	# specify directories
	npz_dir = "crop_raw_fif"
	cda_dir = "epochs_cda"
	recreate_directory(cda_dir)


	# fid npzs
	fns = sorted(glob(f"{npz_dir}/*.npz"))


	# for all npzs
	for fn in fns:
		# load npz
		npz = np.load(fn)
		X = npz['X']
		y = npz['y']
		print(f"X.shape: {X.shape}")
		print(f"y.shape: {y.shape}")
		print(f"y: {y}")
		exit()

		# get indices
		idx_0 = np.where(y == 0)[0]
		idx_1 = np.where(y == 1)[0]
		idx_2 = np.where(y == 2)[0]
		print(f"idx_0: {idx_0}")
		print(f"idx_1: {idx_1}")
		print(f"idx_2: {idx_2}")
		exit()

		# get min length
		min_len = min(len(idx_0), len(idx_1), len(idx_2))
		print(f"min_len: {min_len}")
		exit()

		# get random indices
		idx_0 = np.random.choice(idx_0, min_len, replace=False)
		idx_1 = np.random.choice(idx_1, min_len, replace=False)
		idx_2 = np.random.choice(idx_2, min_len, replace=False)
		print(f"idx_0: {idx_0}")
		print(f"idx_1: {idx_1}")
		print(f"idx_2: {idx_2}")
		exit()

		# get data
		X_0 = X[idx_0]
		X_1 = X[idx_1]
		X_2 = X[idx_2]
		print(f"X_0.shape: {X_0.shape}")
		print(f"X_1.shape: {X_1.shape}")
		print(f"X_2.shape: {X_2.shape}")
		exit()

		# get label
		y_0 = y[idx_0]
		y_1 = y[idx_1]
		y_2 = y[idx_2]
		print(f"y_0.shape: {y_0.shape}")
		print(f"y_1.shape: {y_1.shape}")
		print(f"y_2.shape: {y_2.shape}")
		exit()





	print(fns)
	exit()








if __name__ == '__main__':
	main()