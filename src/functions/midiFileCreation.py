import midiutil

def write_midi_file(filename, midi_tracks, track_num, channel_num, time, duration, tempo, volume):
	print "...Writing MIDI file"
	MyMIDI = midiutil.MIDIFile(track_num)  # number of tracks

	for i in range(track_num):
		MyMIDI.addTempo(track=i, time=time, tempo=tempo)
		d = duration[i]; v = volume[i]
		for j, midi_note in enumerate(midi_tracks):
			for k in range(len(midi_note)):
				MyMIDI.addNote(i, channel_num-1, midi_note[k], time, d[j], v[j])
			time = sum(d[:j+1])
		time = 0

	with open(filename[:-4]+"_accompaniment.mid", "wb") as output_file:
		MyMIDI.writeFile(output_file)

	return "...Accompaniment Completed"