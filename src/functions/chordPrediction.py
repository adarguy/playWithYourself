from __future__ import division 
import sys
import numpy as np

sys.path.append('../lib')
import pymir

def print_chords_and_times(chords, startTimes, endTimes, frameIndex, times):
	first_onset_time = times[-1]-endTimes[-1]
	for i in range (frameIndex):
		print('frame : %6d | chord : %6s | startTime : %8.5f | endTime : %8.5f | length : %7.5f' % (i+1,chords[i],startTimes[i]+first_onset_time,endTimes[i]+first_onset_time, endTimes[i]-startTimes[i]))
	
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
	
	return chords, startTimes, endTimes, frameIndex