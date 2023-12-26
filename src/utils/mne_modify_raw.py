
import mne
from utils.mne_channel_info import extract_ch_name_type
import numpy as np

def tail_padding(raw):
	"""
	맨 뒤에 0 으로 10초 padding
	"""

	# padding data
	sfreq = raw.info['sfreq']
	duration = int(sfreq * 10)
	padding_data = np.zeros((len(raw.ch_names), duration))

	# raw data
	raw_data = raw.get_data()

	# concat
	data = np.concatenate((raw_data, padding_data), axis=1)

	# rebuild raw
	ch_names, ch_types = extract_ch_name_type(raw)
	raw = rebuild_raw(data, sfreq, ch_names, ch_types)

	return raw
	
	
	
def rebuild_raw(data, sfreq, ch_names, ch_types):
	"""
	data 와 info 를 받아서 raw 를 재 조립한다.
		raw 의 변화가 view 만 생성되었을 가능성을 없애기 위해서
	"""
	info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
	raw = mne.io.RawArray(data, info)
	return raw

