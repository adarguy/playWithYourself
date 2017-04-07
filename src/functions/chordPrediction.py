from __future__ import division 

import pymir
import numpy as np
import sys

def print_chords_and_times(chords, startTimes, endTimes, frameIndex, times, show):
	if (not show): return
	for i in range (frameIndex):
		print('frame : %6d | chord : %6s | startTime : %8.5f | endTime : %8.5f | length : %7.5f' % (i+1,chords[i],startTimes[i],endTimes[i], endTimes[i]-startTimes[i]))
	
def get_chords(input_file, beat_times, times):
	print "...Predicting chords"	
	audiofile = pymir.AudioFile.open(input_file);
	t = len(audiofile)/times[-1]
	bt = [int(round(x*t, 3)) for x in beat_times]
	frames = audiofile.framesFromOnsets(bt)
	
	chords = []; regs = []; startTimes = []; endTimes = []; numFrames = 0;
	frameIndex = 0; startIndex = 0;
	for frame in frames:	
		spectrum = frame.spectrum();
		chroma = spectrum.chroma();
		
		reg = pymir.Pitch.naivePitch(spectrum)
		regs = np.append(regs, reg[1])

		chord, score = pymir.Pitch.getChord(chroma);
		chords = np.append(chords, chord);

		endIndex = startIndex + len(frame);
		
		startTimes = np.append(startTimes, beat_times[frameIndex]);

		if ((frameIndex+1)==len(beat_times)):
			endTimes = np.append(endTimes, times[-1]);
		else:
			endTimes = np.append(endTimes, beat_times[frameIndex+1]);

		frameIndex = frameIndex + 1
		startIndex = startIndex + len(frame)
	
	return chords, regs, startTimes, endTimes, frameIndex

