

from glob import glob


def main():

	"""
	CDA 용 1:1:1 training validation set
	"""

	npz_dir = "crop_raw_fif"
	fns = sorted(glob(f"{npz_dir}/*.npz"))

	print(fns)
	exit()








if __name__ == '__main__':
	main()