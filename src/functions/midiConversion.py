import numpy as np

root_postion = {		'A':	[[57,61,64]],
						'Am':	[[57,60,64]],
						'Bb':	[[58,62,65]],
						'Bbm':	[[58,61,65]],
						'Bm':	[[59,62,66]],
						'B':	[[59,63,66]],
						'C':	[[60,64,67]],
						'Cm':	[[60,63,67]],
						'C#':	[[61,65,68]],
						'Dbm':	[[61,64,68]],
						'D':	[[62,66,69]],
						'Dm':	[[62,65,69]],
						'Eb':	[[63,67,70]],
						'Ebm':	[[63,66,70]],
						'E':	[[64,68,71]],
						'Em':	[[64,67,71]],
						'F':	[[65,69,72]],
						'Fm':	[[65,68,72]],
						'F#':	[[66,70,73]],
						'F#m':	[[66,69,73]],
						'G':	[[67,71,74]],
						'Gm':	[[67,70,74]],
						'Ab':	[[68,72,75]],
						'Abm':	[[68,69,75]]}

closed_chord_list = {	'A':	[[25,33,40],[40,45,49],[45,49,52],[52,57,61],[57,61,64]],
						'Am':	[[24,33,40],[40,45,48],[45,48,52],[52,57,60],[57,60,64]],
						'Bb':	[[26,34,41],[38,41,46],[46,50,53],[53,58,62],[58,62,65]],
						'Bbm':	[[25,34,41],[37,41,46],[46,49,53],[53,58,61],[58,61,65]],
						'B':	[[27,35,42],[39,42,47],[47,51,54],[54,59,63],[59,63,66]],
						'Bm':	[[26,35,42],[38,42,47],[47,50,54],[54,59,62],[59,62,66]],
						'C':	[[24,31,40],[36,40,43],[43,48,52],[48,52,55],[60,64,67]],
						'Cm':	[[24,31,39],[36,39,43],[43,48,51],[48,51,55],[60,63,67]],
						'C#':	[[25,32,41],[37,41,44],[44,49,53],[49,53,56],[61,65,68]],
						'Dbm':	[[25,32,40],[37,40,44],[44,49,52],[49,52,56],[61,64,68]],
						'D':	[[26,33,42],[38,42,45],[45,50,54],[50,54,57],[62,66,69]],
						'Dm':	[[26,33,41],[38,41,45],[45,50,53],[50,53,57],[62,65,69]],
						'Eb':	[[27,34,43],[34,39,43],[43,46,51],[51,55,58],[63,67,70]],
						'Ebm':	[[27,34,42],[34,39,42],[46,51,54],[51,54,58],[63,66,70]],
						'E':	[[28,35,44],[35,40,44],[44,47,52],[47,52,56],[64,68,71]],
						'Em':	[[28,35,43],[35,40,43],[43,47,52],[47,52,57],[64,67,71]],
						'F':	[[24,33,41],[36,41,45],[48,53,57],[48,53,57],[65,69,72]],
						'Fm':	[[24,32,41],[36,41,44],[48,53,56],[48,53,56],[24,32,41]],
						'F#':	[[25,34,42],[37,42,46],[46,49,54],[49,54,58],[66,70,73]],
						'F#m':	[[25,33,42],[37,42,45],[45,49,54],[49,54,57],[66,69,73]],
						'G':	[[26,35,43],[38,43,47],[43,47,50],[50,55,59],[67,71,74]],
						'Gm':	[[26,34,43],[38,43,46],[43,46,50],[50,55,58],[67,70,74]],
						'Ab':	[[24,32,39],[39,44,48],[44,48,51],[51,56,60],[68,72,75]],
						'Abm':	[[27,35,44],[39,44,47],[44,47,51],[51,56,59],[68,69,75]]}

beat_list44 = {			0:[[42,35],[42],[42,38],[42]],
						1:[[42,35],[42],[42,38],[42]]}

beat_list34 = {			0:[[42,35],[42],[42,38]],
						1:[[42,35],[42],[42,38]]}

def convert_note_to_midi(notes, reg):
	print "...Converting notes to MIDI values"
	midi_notes = [[0]]
	for i in range(len(notes)):
		midi_notes.append([closed_chord_list[notes[i]][(int(reg[i]))%len(closed_chord_list[notes[i]])][0]])

	return midi_notes

def convert_chord_to_midi(chords, reg, style):
	print "...Converting chords to MIDI values"
	midi_chords = [[0,0,0]]
	for i in range(len(chords)):
		if (style == 0.0):
			midi_chords.append(closed_chord_list[chords[i]][(int(reg[i]))%len(closed_chord_list[chords[i]])])
		else:
			midi_chords.append(root_postion[chords[i]])
	return midi_chords

def convert_beat_to_midi(beats, pattern, time_sig, inst, reg):
	print "...Converting beats to MIDI values"
	midi_beats = [[0]]
	if (inst == 128):
		for i in range(len(beats)):
			if (time_sig == 4):
				midi_beats.append(beat_list44[pattern][i%len(beat_list44[int(pattern)])])
			else:
				midi_beats.append(beat_list34[pattern][i%len(beat_list34[int(pattern)])])
	else:
		midi_beats = convert_note_to_midi(beats, reg)
	return midi_beats

def determine_durations(chords, reg, startTimes, endTimes, frameIndex, volume):
	i = 1; j = 0;
	while (i < len(chords)):
		if (chords[i] == chords[j]):
			if (volume[i] > volume[j]):
				volume = np.delete(volume, j)
			else:
				volume = np.delete(volume, i)
			chords = np.delete(chords, i)
			reg = np.delete(reg, i)
			startTimes = np.delete(startTimes, i)
			endTimes = np.delete(endTimes, j)
			frameIndex -= 1
			i -= 1; j -= 1
		i += 1; j += 1

	return chords, reg, startTimes, endTimes, frameIndex, volume
