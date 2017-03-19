chord_list = {	'A':[60,61,66],
				'Bm':[60,61,66],
				'C#':[60,61,66],
				'D':[60,61,66],
				'Em':[60,61,66],
				'F#':[60,61,66],
				'Ab':[60,61,66],}

def convert_chord_to_midi(chords):
	print "...Converting chord notes to MIDI values"
	midi_notes = []
	for i in range(len(chords)):
		midi_notes.append(chord_list[chords[i]])

	return midi_notes