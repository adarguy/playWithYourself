import midiutil

def write_midi_file(filename, midi_tracks, channel, program, time, duration, tempo, volume):
	print "...Writing MIDI file"
	MyMIDI = midiutil.MIDIFile(len(midi_tracks))  # number of tracks

	for i in range(len(midi_tracks)):
		MyMIDI.addTempo(track=i+1, time=time, tempo=tempo)
		MyMIDI.addProgramChange(track=i+1, channel=channel-1, time=time, program=program[i])
		d = duration[i]; v = volume[i]
		for j, midi_note in enumerate(midi_tracks[i]):
			for k in range(len(midi_note)):
				MyMIDI.addNote(i, channel-1, midi_note[k], time, d[j], v[j])
			time = sum(d[:j+1])
		time = 0

	with open(filename[:-4]+"_accompaniment.mid", "wb") as output_file:
		MyMIDI.writeFile(output_file)

	return "...Accompaniment Completed"