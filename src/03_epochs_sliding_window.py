import numpy as np

from pathlib import Path
import mne
import matplotlib.pyplot as plt

from utils.mne_plot_raw import plot_raw
from utils.mne_modify_raw import rebuild_raw
from utils.mne_channel_info import extract_ch_name_type

import pandas as pd


def process_one_fif(fn_fif, events, w_size_tick, w_stride_tick):

	# load fif
	raw = mne.io.read_raw_fif(fn_fif, preload=True)

	# make it numpy
	raw_data = raw.get_data().astype(np.float32)  # shape = (65, 240000)

	# for each sliding window
	for i in range(0, len(raw_data[0]), w_stride_tick):

		print(f"i: {i}, sec: {i/500}")


	exit()









def epoch_sliding_window(dir_fif, sample_Hz, events_npy, w_size_sec, w_stride_sec):

	# data_dir
	data_dir = Path(dir_fif)
	fns = sorted(list(data_dir.glob('*.fif')))

	# load events
	events = np.load(events_npy)
	"""
	events = 
		[[  5000      0      1]
		 [  8500      0      2]
		 [ 17000      0      1] ...
	"""

	w_size_tick = int(sample_Hz * w_size_sec)
	w_stride_tick = int(sample_Hz * w_stride_sec)

	for fn in fns:
		process_one_fif(fn, events, w_size_tick, w_stride_tick)







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
		w_size_sec: sliding window 의 크기 (초)
		w_stride_sec: sliding window 의 stride (초)

	"""
	dir_fif = "crop_raw_fif"
	sample_Hz = 500
	events_npy = "answer_sheet.npy"
	w_size_sec = 1
	w_stride_sec = 0.5

	# run epoch_sliding_window
	epoch_sliding_window(dir_fif, sample_Hz, events_npy, w_size_sec, w_stride_sec)













if __name__ == '__main__':
	main()


