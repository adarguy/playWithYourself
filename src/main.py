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
	UI_onset_threshold = 0.4; UI_dynamic_threshold = 1
	UI_instrument_harm = 10; UI_instrument_perc = 10

	# TRACK BEATS
	onsets, beats, v = beatDetection.track_beats(y, sr, UI_onset_threshold, UI_dynamic_threshold)
	times = beatDetection.plot_beats_and_onsets(onsets, beats)

	# PREDICT CHORDS	
	c, s, e, f = chordPrediction.get_chords(p['input_file'], times[beats], times);
	chords, startTimes, endTimes, frameIndex, volume = midiChordConversion.determine_durations(c, s, e, f, v)
	chordPrediction.print_chords_and_times(chords, startTimes, endTimes, frameIndex, times)


	# CHORDS TO MIDI
	midi_notes = midiChordConversion.convert_chord_to_midi(chords)
	pattern = [[42,35],[42],[42,38],[42]]

	midi_beats = [[0]]
	for i in range(len(beats)):
		midi_beats.append(pattern[i%4])
	midi_tracks = [midi_notes, midi_beats] 		# second will be changed to drum accompaniment
	

	# WRITE MIDI
	track = 1
	channel = 1 								#mono channel as default
	time = 0; 									#unless signal starts after 0?
	tempo = librosa.beat.beat_track(y=y, sr=sr);
	start_duration = (times[-1]-endTimes[-1])/(60/tempo[0])
									
	chord_duration = [start_duration]			#chord Parameters
	chord_volume = [0]
	chord_program = UI_instrument_harm
	for i in range(len(midi_tracks[0])-1):
		chord_duration.append(round((endTimes[i] - startTimes[i])/(60/tempo[0]), 1))
		chord_volume.append(int(round(127-(UI_dynamic_threshold*127))+round(volume[i])))
								
	beat_duration = [start_duration]			#beat Parameters
	beat_volume = [0]
	beat_program = UI_instrument_perc
	for i in range(len(beats)):
		beat_duration.append(round((e[i] - s[i])/(60/tempo[0]), 1))
		beat_volume.append(int(round(127-(UI_dynamic_threshold*127))+round(v[i])))

	duration = [chord_duration, beat_duration]
	volume = [chord_volume, beat_volume]
	program = [chord_program, beat_program]

	print midiFileCreation.write_midi_file(p['input_file'], midi_tracks, channel, program, time, duration, tempo[0], volume)















main()