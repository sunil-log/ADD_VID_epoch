

from glob import glob


def main():

	"""
	CDA 용 1:1:1 training validation set
	"""

	npy_dir = "crop_raw_fif"
	fns = sorted(glob(f"{npy_dir}/*.npy"))

	print(fns)
	exit()








if __name__ == '__main__':
	main()