# IMPORT PYTHON LIBRARIES
import sys

# IMPORT MIR LIBRARIES
sys.path.append('../lib')
import pymir
import librosa

# IMPORT OUR MIR FUNCTIONS
sys.path.append('functions')
import utils
import chordPrediction
import beatDetection

def main():
	# OPEN FILE
	p = utils.process_arguments(sys.argv[1:]);
	print "Opening File: " + p['input_file']
	y, sr = librosa.load(p['input_file'])

	# TRACK BEATS
	onsets, beats, beat_times = beatDetection.track_beats(y, sr)
	times = beatDetection.plot_beats_and_onsets(onsets, beats)

	# PREDICT CHORDS	
	chords, startTimes, endTimes, frameIndex = chordPrediction.get_chords(p['input_file'], beat_times, times);
	chordPrediction.print_chords_and_times(chords, startTimes, endTimes, frameIndex, times)
	

	#NEXT STEPS: compare the beat times and onset times with the chord times, (IN SECONDS) and so we will know
				 #when to insert a new note for the Accompaniment we are creating.
	
















main()