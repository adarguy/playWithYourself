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

def track_beats(y, sr, UI_onset, UI_dynamic):
	print "...Tracking onsets"
	onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median);
	onsets = librosa.util.normalize(onset_env)
	
	beats = []
	for i in range(1, len(onsets)-1):
		if ((onsets[i] > onsets[i-1] and onsets[i] > onsets[i+1]) and onsets[i] > UI_onset):
			beats.append(i)
	beat_times = librosa.frames_to_time(beats, sr=sr);
	
	#i want to try and find cleaner way to do this...
	t = 0
	for i in range(1, len(beat_times)):
		beat_length = beat_times[i]-beat_times[i-1]
		if(beat_length < 0.1):
			t += 1;
	
	for i in range(1, len(beat_times)-t):
		beat_length = beat_times[i]-beat_times[i-1]
		#print str(i)+") "+str(beat_times[i] - beat_times[i-1])
		if(beat_length < 0.1):
			if(beat_times[i] > beat_times[i-1]): del beats[i-1]
			else: del beats[i]
			beat_times = np.delete(beat_times, i)
			beat_times[i-1] += beat_length

	volume = onsets[beats]*UI_dynamic*127
	return onsets, beats, volume

	