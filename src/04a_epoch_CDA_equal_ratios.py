

import numpy as np

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







	print(fns)
	exit()








if __name__ == '__main__':
	main()