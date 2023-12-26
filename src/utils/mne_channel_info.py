
import mne

def check_channel_exist(raw, channel_name):
	"""
	채널의 존재 여부를 확인하는 함수
	"""
	return channel_name in raw.ch_names
	
	
	
	
def extract_ch_name_type(raw):
	"""
	원래 raw 객체에서 채널 정보를 추출
	"""
	ch_names = raw.ch_names
	ch_types = [channel['kind'] for channel in raw.info['chs']]

	# 채널 유형이 정수로 되어 있다면, 이를 문자열로 변환
	# MNE-Python에서는 일반적으로 채널 유형을 문자열로 사용합니다.
	ch_types = [mne.io.pick.channel_type(raw.info, i) for i in range(raw.info['nchan'])]

	return ch_names, ch_types




def print_channel_info(raw):
	"""
	print channel name and type
	"""
	ch_names, ch_types = extract_ch_name_type(raw)
	for ch_name, ch_type in zip(ch_names, ch_types):
		print(f"Name: {ch_name}, Type: {ch_type}")




