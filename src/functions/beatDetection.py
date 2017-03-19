import librosa
import numpy as np
import matplotlib.pyplot as plt

def plot_beats_and_onsets(onsets, beats):
	print "...Plotting beats and onsets"
	plt.figure(figsize=(8, 4));
	times = librosa.frames_to_time(np.arange(len(onsets)));

	plt.plot(times, onsets,label='Onset strength');
	plt.vlines(times[beats], 0, 1, alpha=0.5, color='r',linestyle='--', label='Beats');
	plt.legend(frameon=True, framealpha=0.75);
	plt.xlim(0, times[-1]);
	plt.show();
	return times

def track_beats(y, sr):
	print "...Tracking onsets"
	onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median);
	onsets = librosa.util.normalize(onset_env)	
	beats =[]
	for i in range(len(onsets)):
		if (onsets[i] > 0.4):
			beats.append(i)
	beat_times = librosa.frames_to_time(beats, sr=sr);
	return onsets, beats, beat_times;

	