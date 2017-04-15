import midiutil

def build_track(UI_instrument, midi_tracks,startTimes, endTimes, volume, msec_tempo, UI_dynamic_threshold):
	note_volume = [0]; 
	note_program = UI_instrument; 
	note_duration = [round(startTimes[0]/msec_tempo, 1)]
	for i in range(len(midi_tracks)-1):
		note_duration.append(round((endTimes[i] - startTimes[i])/msec_tempo, 1))
		note_volume.append(int(round(127-(UI_dynamic_threshold*127))+round(volume[i])))

	return note_duration, note_program, note_volume

def write_midi_file(filename, midi_tracks, program, duration, tempo, volume):
	print "...Writing MIDI file"
	MyMIDI = midiutil.MIDIFile(len(midi_tracks))
	time = 0;
	channel = 1
	for i in range(len(midi_tracks)):	
		if (program[i]==128):
			channel = 10; program[i] = 0
		MyMIDI.addTempo(track=i+1, time=time, tempo=tempo)
		MyMIDI.addProgramChange(track=i+1, channel=channel-1, time=time, program=program[i])
		d = duration[i]; v = volume[i]
		for j, midi_note in enumerate(midi_tracks[i]):
			for k in range(len(midi_note)):
				MyMIDI.addNote(i, channel-1, midi_note[k], time, d[j], v[j])
			time = sum(d[:j+1])
		time = 0

	with open(filename[:-4]+".mid", "wb") as output_file:
		MyMIDI.writeFile(output_file)