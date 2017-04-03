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
import midiConversion
import midiFileCreation


def main():
	# OPEN FILE
	show_diagnostics = False;
	UI_instrument_notes = 32; UI_onset_threshold = 0.1;
	UI_instrument_chords = 0; UI_dynamic_threshold = 0.7;
	UI_instrument_beats = 10; UI_beat_windowSize = 0.3; #100 msec
	
	args = utils.process_arguments(sys.argv[1:], show_diagnostics);
	y, sr = librosa.load(args['input_file'])




	# TRACK BEATS
	onsets, beats, volume_notes, times, tempo, msec_tempo = beatDetection.track_beats(y, sr, UI_onset_threshold, UI_dynamic_threshold, UI_beat_windowSize)
	beatDetection.plot_beats_and_onsets(onsets, beats, times, show_diagnostics)




	# PREDICT CHORDS
	notes, startTimes_notes, endTimes_notes, frameIndex_notes = chordPrediction.get_chords(args['input_file'], times[beats], times)
	chords, startTimes_chords, endTimes_chords, frameIndex_chords, volume_chords = midiConversion.determine_durations(list(notes), list(startTimes_notes), list(endTimes_notes), frameIndex_notes, list(volume_notes))
	chordPrediction.print_chords_and_times(chords, startTimes_chords, endTimes_chords, frameIndex_chords, times, show_diagnostics)
	startTimes_beats, endTimes_beats = beatDetection.alter_beats(startTimes_notes, endTimes_notes, msec_tempo, UI_beat_windowSize)
	


	
	# NOTES TO MIDI
	midi_notes = midiConversion.convert_note_to_midi(notes)
	midi_chords = midiConversion.convert_chord_to_midi(chords)
	midi_beats = midiConversion.convert_beat_to_midi(endTimes_beats)

	


	# WRITE MIDI
	midi_tracks = [midi_notes, midi_chords, midi_beats]
	startTimes = [startTimes_notes, startTimes_chords, startTimes_beats]
	endTimes = [endTimes_notes, endTimes_chords, endTimes_beats]
	UI_instrument = [UI_instrument_notes, UI_instrument_chords, UI_instrument_beats]
	volumes = [volume_notes, volume_chords, volume_notes]
	duration = [0]*len(midi_tracks); program = [0]*len(midi_tracks); volume = [0]*len(midi_tracks);
	for i in range(len(midi_tracks)):
		duration[i], program[i], volume[i] = midiFileCreation.build_track(UI_instrument[i], midi_tracks[i], startTimes[i], endTimes[i], volumes[i],msec_tempo, UI_dynamic_threshold)
	midiFileCreation.write_midi_file(args['input_file'], midi_tracks, program, duration, tempo[0], volume)




main()