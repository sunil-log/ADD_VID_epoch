import numpy as np

from pathlib import Path
import mne

import pandas as pd


def find_event_value_pandas(df, idx_start, idx_end):
	"""
	events: 이벤트 정보를 담고 있는 pandas DataFrame, columns = ['time', 'col1', 'col2']
	idx_start: 검색 시작 인덱스
	idx_end: 검색 종료 인덱스
	반환값: 조건을 만족하는 이벤트의 세 번째 열 값, 없으면 None
	"""

	"""
	df = 
	      tick  zero  event_id
	0     5000     0         1
	1     8500     0         2
	...
	34  234866     0         1
	35  237000     0         2
	"""

	filtered = df[(df['tick'] >= idx_start) & (df['tick'] < idx_end)]
	if not filtered.empty:
		return filtered['event_id'].iloc[0]
	return 0


def extract_windows(x, events_df, w_size, w_stride):
	"""
	x: 입력 배열, shape = (channels, ts)
	w_size: 추출할 윈도우의 크기
	w_stride: 윈도우의 이동 간격
	반환값: 추출된 윈도우들의 배열
	"""
	n_channels, ts_length = x.shape
	n_windows = 1 + (ts_length - w_size) // w_stride
	windows = np.empty((n_windows, n_channels, w_size))
	max_start_idx = ts_length - w_size
	min_start_idx = 0

	label_list = []
	for i in range(n_windows):

		# add start to jitter
		start_idx = i * w_stride + np.random.randint(-w_stride // 2, w_stride // 2)
		if start_idx > max_start_idx:
			start_idx = max_start_idx
		elif start_idx < min_start_idx:
			start_idx = min_start_idx

		# specify end
		end_idx = start_idx + w_size
		print(start_idx, end_idx)
		windows[i] = x[:, start_idx:end_idx]

		# event label
		event_label = find_event_value_pandas(events_df, start_idx, end_idx)
		label_list.append(event_label)

	return windows, np.array(label_list)


def process_one_fif(fn_fif, events_df, w_size_tick, w_stride_tick, scale_factor):

	# load fif
	raw = mne.io.read_raw_fif(fn_fif, preload=True)

	# make it numpy
	raw_data = raw.get_data().astype(np.float32)  # shape = (65, 240000)
	raw_data = raw_data * scale_factor

	# for each sliding window -> (n_windows, n_channels, w_size)
	epoch_data, label_data = extract_windows(raw_data, events_df, w_size_tick, w_stride_tick)
	"""
	epoch_data.shape = (n_windows, n_channels, w_size)
	label_data.shape = (n_windows,)
	label \in {0, 1, 2}; 0: no event, 1: 군인, 2: 멧되지
	"""

	# save epoch_data, label_data as npz
	new_fn = f"{Path(fn_fif).parent}/{Path(fn_fif).stem}.npz"
	np.savez(new_fn, X=epoch_data, y=label_data)



def epoch_sliding_window(dir_fif, sample_Hz, events_npy, w_size_sec, w_stride_sec, scale_factor):

	# data_dir
	data_dir = Path(dir_fif)
	fns = sorted(list(data_dir.glob('*.fif')))

	# load events
	events = np.load(events_npy)
	events_df = pd.DataFrame(events, columns=['tick', 'zero', 'event_id'])
	"""
	events_df = 
	      tick  zero  event_id
	0     5000     0         1
	1     8500     0         2
	...
	34  234866     0         1
	35  237000     0         2
	"""

	w_size_tick = int(sample_Hz * w_size_sec)
	w_stride_tick = int(sample_Hz * w_stride_sec)

	for fn in fns:
		process_one_fif(fn, events_df, w_size_tick, w_stride_tick, scale_factor)




def main():

	"""
	각 subject (fif 파일을) numpy array 로 load 한다.
	시간축에 따라 sliding_window_size_sec 의 크기의 epoch 을 extract 하고,
	sliding_window_stride_sec 만큼씩 window 를 이동시킨다.
	window 안에 event 가 존재하면 해당 event 의 label 을 저장한다.
		0: no event, 1: 군인, 2: 멧돼지
	그러한 epoch 과 label 을 npz 파일로 저장한다 (X, y).

	Parameters
		dir_fif: raw fif 파일이 있는 디렉토리
		sample_Hz: EEG 의 sampling rate
		events_npy: 동영상의 event sheet 정보가 담긴 npy 파일
		w_size_sec: sliding window 의 크기 (초)
		w_stride_sec: sliding window 의 stride (초)
		scale_factor: EEG 의 voltage 에 곱해줄 스케일링 factor

	"""
	dir_fif = "crop_raw_fif"
	sample_Hz = 500
	events_npy = "answer_sheet.npy"
	w_size_sec = 1.0
	w_stride_sec = 0.5
	scale_factor = 1e5

	# run epoch_sliding_window
	epoch_sliding_window(dir_fif, sample_Hz, events_npy, w_size_sec, w_stride_sec, scale_factor)













if __name__ == '__main__':
	main()


