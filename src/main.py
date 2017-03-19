#IMPORT PYTHON LIBRARIES
from __future__ import division 
import sys, argparse
import matplotlib.pyplot as plt
import numpy as np

#IMPORT MIR LIBRARIES
import librosa
sys.path.append('../lib')
import pymir

def process_arguments(args):
    parser = argparse.ArgumentParser(description='Beat tracking example')
    parser.add_argument('input_file',
                        action='store',
                        help='path to the input file (wav, mp3, etc)')
    return vars(parser.parse_args(args))

def track_beats(y, sr):
	print "...Tracking onsets"
	onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median);
	onsets = librosa.util.normalize(onset_env)	
	beats =[]
	for i in range(len(onsets)):
		if (onsets[i] > 0.4):
			beats.append(i)
	beat_times = librosa.frames_to_time(beats, sr=sr);
	times = plot_beats_and_onsets(onset_env, onsets, beats)
	
	return beats, beat_times, times;

def plot_beats_and_onsets(onset_env, onsets, beats):
	print "...Plotting beats and onsets"
	plt.figure(figsize=(8, 4));
	times = librosa.frames_to_time(np.arange(len(onset_env)));

	plt.plot(times, onsets,label='Onset strength');
	plt.vlines(times[beats], 0, 1, alpha=0.5, color='r',linestyle='--', label='Beats');
	plt.legend(frameon=True, framealpha=0.75);
	plt.xlim(0, times[-1]);
	plt.show();
	return times

def get_chords(input_file, beat_times, times):
	print "...Predicting chords"	
	audiofile = pymir.AudioFile.open(input_file);
	t = len(audiofile)/times[-1]
	beat_times = [int(round(x*t)) for x in beat_times]
	frames = audiofile.framesFromOnsets(beat_times)
	
	chords = []; startTimes = []; endTimes = []; numFrames = 0;
	frameIndex = 0; startIndex = 0;

	for frame in frames:	
		spectrum = frame.spectrum();
		chroma = spectrum.chroma();
		
		chord, score = pymir.Pitch.getChord(chroma);	
		chords = np.append(chords, chord);

		endIndex = startIndex + len(frame);
		startTime = startIndex / frame.sampleRate; 
		startTimes = np.append(startTimes, startTime);
		
		endTime = endIndex / frame.sampleRate;
		endTimes = np.append(endTimes, endTime);
		
		frameIndex = frameIndex + 1
		startIndex = startIndex + len(frame)
	
	first_onset_time = times[-1]-endTimes[-1]
	for i in range (frameIndex):
		print('frame : %6d | chord : %6s | startTime : %8.5f | endTime : %7.5f ' % (i+1,chords[i],startTimes[i]+first_onset_time,endTimes[i]+first_onset_time))
	
	return chords, startTimes, endTimes, frameIndex;

def main():
	# OPEN FILE
	p = process_arguments(sys.argv[1:]);
	print "Opening File: " + p['input_file']
	y, sr = librosa.load(p['input_file'])
	#plt.plot(y)
	#plt.show()
	

	# TRACK BEATS
	beats, beat_times, times = track_beats(y, sr)
	#print beats
	#print beat_times

	# PREDICT CHORDS	
	chords = [];
	startTimes = [];
	endTimes = [];
	numFrames = 0;

	chords, startTimes, endTimes, numFrames = get_chords(p['input_file'], beat_times, times);
	
	#print chords;     #letter name of chords predicted.
	#print startTimes; #time in seconds that chord starts 
	#print endTimes;   #time in seconds chord ends
	#print numFrames;  #total number of chords predicted 
	

	#NEXT STEPS: compare the beat times and onset times with the chord times, (IN SECONDS) and so we will know
				 #when to insert a new note for the Accompaniment we are creating.
	
















main()