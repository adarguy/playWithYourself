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
	chords, startTimes, endTimes, frameIndex = midiChordConversion.determine_durations(chords, startTimes, endTimes, frameIndex)
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
	start_duration = (times[-1]-endTimes[-1])/(60/tempo[0])
									
	chord_duration = [start_duration]			#chord Parameters
	chord_volume = [0]
	for i in range(len(midi_tracks[0])-1):
		chord_duration.append(round((endTimes[i] - startTimes[i])/(60/tempo[0]), 1))
		chord_volume.append(100)
												
	#beat_duration = [start_duration]			#beat Parameters
	#beat_volume = [0]
	#for i in range(len(midi_tracks[0])-1):
	#	beat_duration.append(round((endTimes[i] - startTimes[i])/(60/tempo[0]), 1))
	#	beat_volume.append(100)

	duration = [chord_duration, chord_duration]
	volume = [chord_volume, chord_volume]


	print midiFileCreation.write_midi_file(p['input_file'], midi_notes, track_num, channel_num, time, duration, tempo[0], volume)















main()