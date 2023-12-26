import mne
import matplotlib.pyplot as plt
from utils.image_processing import reduce_palette_from_matplotlib_image

def plot_raw(raw, new_fn):

	# plot raw using plt
	plt.close('all')
	fig, ax = plt.subplots(len(raw.info['ch_names']), 1, figsize=(30, 50), sharex=True)
	raw_data = raw.get_data()   # (channel, ts)

	raw_data = raw_data[:, ]
	for i, ch in enumerate(raw.info['ch_names']):
		ax[i].plot(raw.times, raw_data[i])
		ax[i].set_title(ch)

	img = reduce_palette_from_matplotlib_image(fig, 16)
	img.save(new_fn)
	# plt.savefig('raw.png', dpi=300, bbox_inches='tight')


