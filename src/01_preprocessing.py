
from pathlib import Path

import mne
from scipy.signal import detrend
import numpy as np


from utils.dir_manage import recreate_directory
from utils.mne_plot_raw import plot_raw
from utils.mne_channel_info import print_channel_info, check_channel_exist, extract_ch_name_type
from utils.mne_modify_raw import rebuild_raw, tail_padding



def crop_haed_and_tail(raw):
	"""
	첫번째 event 에서 1초 전에서 시작하여 마지막 event 의 16초 뒤까지 자르고,
	data 를 추출하여 새로운 raw 를 만들어 반환 (이렇게 하지 않으면 crop 이전 timestamp 가 유지됨)
	"""

	# 혹시 몰라서 tail 에 10초 padding
	raw = tail_padding(raw)

	# 첫번쨰 event 와 마지막 event+15초 사이의 데이터만 추출
	events = mne.find_events(raw, stim_channel='stim')
	sfreq = raw.info['sfreq']
	"""
	[[  4178      0      2]
	 [ 14178      0      2]
	 [ 23285      0      2] ...
	"""
	t_start = events[0][0] - 1 * sfreq
	t_end = events[-1][0] + 16 * sfreq
	raw.crop(tmin=t_start/sfreq, tmax=t_end/sfreq)

	# rebulid raw
	data = raw.get_data()
	ch_names, ch_types = extract_ch_name_type(raw)
	raw = rebuild_raw(data, sfreq, ch_names, ch_types)

	return raw



def pre_processing(fn, target_dir, low_Hz, high_Hz):

	# load raw data
	raw = mne.io.read_raw_egi(fn, preload=True)
	sfreq = raw.info['sfreq']       # 500Hz
	"""
	print_channel_info(raw)
	Name: E1, Type: eeg
	...
	Name: E64, Type: eeg
	Name: VREF, Type: eeg
	Name: STRT, Type: stim
	Name: stim, Type: stim
	Name: STI 014, Type: stim
	"""

	# stim 채널이 있는지 확인하고, 없으면 exit
	if not check_channel_exist(raw, 'stim'):
		print(f"stim 채널이 없습니다. {fn} 파일을 확인해주세요.")
		print_channel_info(raw)
		new_fn = f"{target_dir}/{Path(fn).stem}_raw_BAD.png"
		plot_raw(raw, new_fn)
		return None

	"""
	Pre-Processing
	"""
	# event 기반으로 앞뒤를 자름
	raw = crop_haed_and_tail(raw)

	# de-trend (apply 는 채널 하나씩 수행된다)
	raw.apply_function(detrend, picks='eeg', verbose=True)

	# band-pass filter
	raw.filter(l_freq=low_Hz, h_freq=high_Hz, picks='eeg')

	# re-reference by average
	raw.set_eeg_reference('average', projection=True)
	raw.apply_proj()



	"""
	event 마다 15초씩 잘라서 이어붙이기
	"""
	events = mne.find_events(raw, stim_channel='stim')
	data = []
	for event in events:
		start = event[0]
		end = int(start + 15 * sfreq)
		data.append(raw.get_data(start=start, stop=end))  # shape = (68, 7500)
	# concat data
	data = np.concatenate(data, axis=1)
	"""
	data.shape = (68, 240000) = (68 channels, 15secs * 500Hz * 32 trials)
	"""

	# make data raw
	ch_names, ch_types = extract_ch_name_type(raw)
	raw = rebuild_raw(data, sfreq, ch_names, ch_types)

	# plot before channel selection
	new_fn = f"{target_dir}/{Path(fn).stem}_raw.png"
	plot_raw(raw, new_fn)

	# extract only [E1, E2, ..., E64, VREF]
	raw.pick_types(eeg=True)

	# new name
	new_fn = f"{target_dir}/{Path(fn).stem}_raw.fif"
	raw.save(new_fn, overwrite=True)




def main():

	"""
	1. EEG data 에 linear detrend 및 band-pass filter 를 적용합니다.
	2. Average reference 를 적용합니다.
	3. event 기반으로 앞뒤를 자르고, 15초씩 잘라서 이어붙입니다.
		이렇게 하여 동영상을 시청하는 동안의 데이터만 추출하여 이어 붙입니다.
	4. E1 ~ E64, VREF 채널만 추출합니다. (STRT, stim, STI 014 는 제거)
	5. 결과물을 fif 형태로 저장합니다.

	raw_dir: mff 가 있는 위치
	target_dir: fif 가 저장될 위치
	low_Hz: band-pass filter 의 하한
	high_Hz: band-pass filter 의 상한
	"""

	# Parameters
	raw_dir = Path('../../')
	# run `ls`
	import os
	print(os.system('ls ../../'))
	exit()




	target_dir = Path('crop_raw_fif')
	low_Hz = 1
	high_Hz = 40

	# Create target directory
	recreate_directory(target_dir)

	# Get raw file list
	raw_list = sorted(list(raw_dir.glob('*.mff')))

	# pre-processing
	for fn in raw_list:
		pre_processing(fn, target_dir, low_Hz, high_Hz)






if __name__ == '__main__':
	main()