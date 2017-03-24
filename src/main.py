# IMPORT PYTHON LIBRARIES
import sys

# IMPORT MIR LIBRARIES
sys.path.append('../lib')
import librosa
import pymir
import midiutil


# IMPORT OUR MIR FUNCTIONS
sys.path.append('functions')
import beatDetection
import utils
import chordPrediction
import midiChordConversion
import midiFileCreation


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
	

	# CHORDS TO MIDI
	midi_notes = midiChordConversion.convert_chord_to_midi(chords)
	#get the drum samples or whatever we will use
	midi_tracks = [midi_notes, midi_notes] 		# second will be changed to drum accompaniment
	

	# WRITE MIDI

	track_num = len(midi_tracks)
	channel_num = 1 							#mono channel as default
	time = 0; 									#unless signal starts after 0?
	tempo = librosa.beat.beat_track(y=y, sr=sr);

	chord_duration = [1]*len(midi_tracks[0])	#make variable
	beat_duration = [1]*len(midi_tracks[1])		#make variable
	duration = [chord_duration, beat_duration] 	#second will be changed to beat_duration
	
	chord_volume = [100]*len(midi_tracks[0]) 	#make variable
	beat_volume = [100]*len(midi_tracks[1])		#make variable
	volume = [chord_volume, beat_volume]
	print tempo
	""" #FOR TESTING
		midi_chords  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
		midi_tracks = [midi_chords, midi_chords]
		track_num    = 2
		channel_num  = 1
		time 	 = 0
		duration = [[1, 3, 2, 2, 1, 1, 1, 1], [1, 3, 2, 2, 1, 1, 1, 1]]   # In beats
		tempo    = 60   # In BPM
		volume   = [100, 100]  # 0-127, as per the MIDI standard
	"""
	
	print midiFileCreation.write_midi_file(p['input_file'], midi_notes, track_num, channel_num, time, duration, tempo[0], volume)















main()