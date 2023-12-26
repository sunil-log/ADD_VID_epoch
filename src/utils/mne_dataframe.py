
import pandas as pd
from util_sac.time_series.plot_series import plot_multi_time_series


def concat_raw_annot_in_df(raw):
	"""
	concat raw and annot in dataframe

		0. Assume annot is already applied in raw
		1. make raw df_raw
		2. make annot df_annot
		3. resample df_annot by one second
		4. concat df_raw and df_annot
	"""

	# check if annot is applied in raw
	if not raw.annotations:
		raise Exception('> Annotation is not applied in raw')

	# make raw df
	df_raw = raw.to_data_frame()

	# make annot df
	annot = raw.annotations
	df_annot = pd.DataFrame([annot.onset, annot.description], index=['onset', 'description']).T

	# convert time to tick (int)
	df_raw['tick'] = df_raw['time'].apply(lambda x: int(x*raw.info['sfreq']))
	df_annot['tick'] = df_annot['onset'].apply(lambda x: int(x*raw.info['sfreq']))

	# merge two dfs on tick with left join
	df_merge = pd.merge(df_raw, df_annot, on='tick', how='left')

	# fill na with ffill
	df_merge = df_merge.fillna(method='ffill')

	# fill na with -1
	df_merge = df_merge.fillna(-1)

	"""
	make 'description' as integer code
	
		1. find all unique elements in description
		2. make dictionary with key as unique element and value as integer code
		3. replace description with integer code
	"""
	unique_desc = df_merge['description'].unique()
	desc_dict = {}
	for i, desc in enumerate(unique_desc):
		desc_dict[desc] = i
	df_merge['description_code'] = df_merge['description'].apply(lambda x: desc_dict[x])


	# remove columns
	df_merge = df_merge.drop(['description', 'onset', 'tick'], axis=1)

	return df_merge


def plot_eeg_as_df_all_channel(df):
	"""
	plot given df containing time series
		it is assumed the df is already filtered

	Data Example is as follows
		time  EEG Fpz-Cz  EEG Pz-Oz  EOG horizontal  Resp oro-nasal  EMG submental  Temp rectal  Event marker
		0.00    5.016850  -2.467399       16.508669   -4.820000e+08       3.552000    37.206452         920.0
		0.01   -2.578755   1.467399       16.015873   -4.775133e+08       3.553560    37.206154         920.0
		0.02    1.359707  -4.098901        9.609524   -4.727921e+08       3.555095    37.205865         920.0
	"""

	# extract data
	t = df['time'].values
	data_df = df.drop(['time'], axis=1)
	columns = data_df.columns
	data = data_df.values.T

	# plot
	plt2 = plot_multi_time_series(t, data, columns)
	return plt2



def plot_all_channel_time_series(raw, start=60, duration=60):
	"""
	Plot all channels time series
	"""

	# convert raw to dataframe
	df = raw.to_data_frame()


	"""
	time  EEG Fpz-Cz  EEG Pz-Oz  EOG horizontal  Resp oro-nasal  EMG submental  Temp rectal  Event marker
	0.00    5.016850  -2.467399       16.508669   -4.820000e+08       3.552000    37.206452         920.0
	0.01   -2.578755   1.467399       16.015873   -4.775133e+08       3.553560    37.206154         920.0
	0.02    1.359707  -4.098901        9.609524   -4.727921e+08       3.555095    37.205865         920.0	
	"""

	# filter time	(not including end_time)
	end_time = start + duration
	df = df[df['time'] >= start]
	df = df[df['time'] < end_time]

	# return plot
	return plot_eeg_as_df_all_channel(df)


def channel_name_and_type(raw):
	"""
	return dataframe contains channel name and type in raw object
	"""

	# collect channel names and types
	res = []
	for i in range(raw.info['nchan']):
		ch_name = raw.info['ch_names'][i]
		ch_type = raw.info['chs'][i]['kind']
		res.append( {'idx': i, 'ch_name': ch_name, 'ch_type': ch_type.__str__()} )

	# make dataframe
	df = pd.DataFrame(res)
	return df


