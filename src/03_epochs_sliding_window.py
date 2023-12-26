import numpy as np

from pathlib import Path
import mne
import matplotlib.pyplot as plt

from utils.mne_plot_raw import plot_raw
from utils.mne_modify_raw import rebuild_raw
from utils.mne_channel_info import extract_ch_name_type

import pandas as pd


def process_one_fif(fn_fif, events):

	# load fif
	raw = mne.io.read_raw_fif(fn_fif, preload=True)

	# make it numpy
	raw_data = raw.get_data().astype(np.float32)  # shape = (65, 240000)
	print(f"raw_data.shape: {raw_data.shape}")






def epoch_sliding_window(dir_fif, sample_Hz, events_npy, sliding_window_sec):

	# data_dir
	data_dir = Path('crop_raw_fif')
	fns = sorted(list(data_dir.glob('*.fif')))

	# load events
	events = np.load('answer_sheet.npy')
	"""
	events = 
		[[  5000      0      1]
		 [  8500      0      2]
		 [ 17000      0      1] ...
	"""

	for fn in fns:
		process_one_fif(fn, events)







def main():

	"""
	각 subject (fif 파일을) numpy array 로 load 한다.
	시간축에 따라 sliding_window_size_sec 의 크기의 epoch 을 extract 하고,
	sliding_window_stride_sec 만큼씩 window 를 이동시킨다.
	window 안에 event 가 존재하면 해당 event 의 label 을 저장한다.

	Parameters
		dir_fif: raw fif 파일이 있는 디렉토리
		sample_Hz: EEG 의 sampling rate
		events_npy: 동영상의 event sheet 정보가 담긴 npy 파일
		sliding_window_size_sec: sliding window 의 크기 (초)
		sliding_window_stride_sec: sliding window 의 stride (초)

	"""
	dir_fif = "crop_raw_fif"
	sample_Hz = 500
	events_npy = "answer_sheet.npy"
	sliding_window_size_sec = 1
	sliding_window_stride_sec = 0.5

	# run epoch_sliding_window
	epoch_sliding_window(dir_fif, sample_Hz, events_npy, sliding_window_size_sec)













if __name__ == '__main__':
	main()


