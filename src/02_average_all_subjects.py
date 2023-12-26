import numpy as np

from pathlib import Path
import mne
import matplotlib.pyplot as plt

from utils.mne_plot_raw import plot_raw
from utils.mne_modify_raw import rebuild_raw
from utils.mne_channel_info import extract_ch_name_type

def main():
	"""
	각 event 에 대핸 eeg epoch 의 average 를 plot 한다.

	1. 모든 피험자에 대해서 average 한다.
	2. event file ('answer_sheet.npy') 을 읽어서,
		특정 event (i.g. 군인, 멧돼지, 없음) 에 대해서 average 한다.
	"""

	# Parameters
	data_dir = Path('crop_raw_fif')
	fns = sorted(list(data_dir.glob('*.fif')))

	# read raw, extract data, calculate average
	data = []
	for fn in fns:
		raw = mne.io.read_raw_fif(fn, preload=True)
		raw_data = raw.get_data().astype(np.float32)  # shape = (68, 240000)
		data.append(raw_data)
	data = np.array(data)       # (15, 65, 240000)

	# average over subjects
	average = np.mean(data, axis=0)  # (65, 240000)

	# rebuild raw
	ch_names, ch_types = extract_ch_name_type(raw)
	raw = rebuild_raw(average, raw.info['sfreq'], ch_names, ch_types)

	# plot raw
	# new_fn = f"average_raw.png"
	# plot_raw(raw, new_fn)

	# load events
	events = np.load('answer_sheet.npy')
	"""
	events = 
		[[  5000      0      1]
		 [  8500      0      2]
		 [ 17000      0      1] ...
	"""

	max_tick = events[-1, 0] - 1000
	data_raw = raw.get_data()
	line_color_map = {1: 'r', 2: 'b', 0: 'gray'}
	channel_idx = -1

	list_ts = []
	list_id = []
	for event in events:
		tick, _, event_id = event

		data = data_raw[channel_idx, tick-1000:tick+1000]
		list_ts.append(data)
		list_id.append(event_id)

		random_tick = np.random.randint(1000, max_tick)
		data2 = data_raw[channel_idx, random_tick-1000:random_tick+1000]
		list_ts.append(data2)
		list_id.append(0)

	list_ts = np.array(list_ts)
	list_id = np.array(list_id)
	"""
	list_ts = (72, 2000)
	list_id = (72,)
	"""

	# average over id
	list_ts_1 = list_ts[list_id == 1]
	list_ts_2 = list_ts[list_id == 2]
	list_ts_0 = list_ts[list_id == 0]
	"""
	list_ts_1.shape = (21, 2000)
	list_ts_2.shape = (15, 2000)
	list_ts_0.shape = (36, 2000)
	"""

	average_1 = np.mean(list_ts_1, axis=0)
	average_2 = np.mean(list_ts_2, axis=0)
	average_0 = np.mean(list_ts_0[:15], axis=0)

	# plot
	plt.close("all")
	fig, ax = plt.subplots(1, 1, figsize=(20, 7))
	ax.plot(average_1, label='1', alpha=0.5, c='r')
	ax.plot(average_2, label='2', alpha=0.5, c='b')
	ax.plot(average_0, label='0', alpha=0.5, c='gray')

	plt.savefig('average_raw_epochs.png', bbox_inches='tight')






if __name__ == '__main__':
	main()