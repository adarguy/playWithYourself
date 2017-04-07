# IMPORT PYTHON LIBRARIES
import sys


# IMPORT MIR LIBRARIES
sys.path.append('../lib')
import librosa
import pymir
import midiutil


# IMPORT OUR MIR FUNCTIONS
sys.path.append('functions')
import utils
import beatDetection
import chordPrediction
import midiConversion
import midiFileCreation


show_diagnostics = False;

while(True):
	# OPEN FILE
	args = utils.process_arguments(sys.argv[1:], show_diagnostics);
	UI_instrument_notes = float(args['Instrument1']); UI_onset_threshold = float(args['Busyness']);
	UI_instrument_chords = float(args['Instrument2']); UI_dynamic_threshold = float(args['Dynamics']);
	UI_instrument_beats = float(args['Instrument3']); UI_beat_windowSize = float(args['Window']); #300 msec
	UI_beat_pattern = float(args['Pattern']);
	y, sr = librosa.load(args['Filename'])




	# TRACK BEATS
	onsets, beats, volume_notes, times, tempo, msec_tempo = beatDetection.track_beats(y, sr, UI_onset_threshold, UI_dynamic_threshold, UI_beat_windowSize)
	beatDetection.plot_beats_and_onsets(onsets, beats, times, show_diagnostics)




	# PREDICT CHORDS
	notes, reg_notes, startTimes_notes, endTimes_notes, frameIndex_notes = chordPrediction.get_chords(args['Filename'], times[beats], times)
	chords, reg_chords, startTimes_chords, endTimes_chords, frameIndex_chords, volume_chords = midiConversion.determine_durations(list(notes), list(reg_notes), list(startTimes_notes), list(endTimes_notes), frameIndex_notes, list(volume_notes))
	chordPrediction.print_chords_and_times(chords, startTimes_chords, endTimes_chords, frameIndex_chords, times, show_diagnostics)
	startTimes_beats, endTimes_beats = beatDetection.alter_beats(startTimes_notes, endTimes_notes, msec_tempo, UI_beat_windowSize)
	


	
	# NOTES TO MIDI
	midi_notes = midiConversion.convert_note_to_midi(notes, reg_notes)
	midi_chords = midiConversion.convert_chord_to_midi(chords, reg_chords)
	midi_beats = midiConversion.convert_beat_to_midi(endTimes_beats, UI_beat_pattern)

	


	# WRITE MIDI
	midi_tracks = [midi_notes, midi_chords, midi_beats]
	startTimes = [startTimes_notes, startTimes_chords, startTimes_beats]
	endTimes = [endTimes_notes, endTimes_chords, endTimes_beats]
	UI_instrument = [UI_instrument_notes, UI_instrument_chords, UI_instrument_beats]
	volumes = [volume_notes, volume_chords, volume_notes]
	duration = [0]*len(midi_tracks); program = [0]*len(midi_tracks); volume = [0]*len(midi_tracks);
	for i in range(len(midi_tracks)):
		duration[i], program[i], volume[i] = midiFileCreation.build_track(UI_instrument[i], midi_tracks[i], startTimes[i], endTimes[i], volumes[i],msec_tempo, UI_dynamic_threshold)
	midiFileCreation.write_midi_file(args['Filename'], midi_tracks, program, duration, tempo[0], volume)




	# PREVIEW
	happy = utils.preview(args['Filename'])

	if (happy):
		utils.clean(args['Filename'])
		break;









