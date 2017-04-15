import numpy as np

root_postion = {		'A':	[[57,61,64]],
						'Am':	[[57,60,64]],
						'Bb':	[[58,62,65]],
						'Bbm':	[[58,61,65]],
						'Bm':	[[59,62,66]],
						'B':	[[59,63,66]],
						'Bb':	[[59,62,66]],
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
						'F#':	[[66,70,73]],
						'F#m':	[[66,69,73]],
						'G':	[[67,71,74]],
						'Gm':	[[67,70,74]],
						'Ab':	[[68,72,75]],
						'Abm':	[[68,69,75]]}

closed_chord_list = {	'A':	[[40,45,49],[45,49,52],[52,57,61]],
						'Am':	[[40,45,48],[45,48,52],[52,57,60]],
						'Bb':	[[38,41,46],[46,50,53],[53,58,62]],
						'Bbm':	[[37,41,46],[46,49,53],[53,58,61]],
						'B':	[[39,42,47],[47,51,54],[54,59,63]],
						'Bm':	[[38,42,47],[47,50,54],[54,59,62]],
						'C':	[[36,40,43],[43,48,52],[48,52,55]],
						'Cm':	[[36,39,43],[43,48,51],[48,51,55]],
						'C#':	[[37,41,44],[44,49,53],[49,53,56]],
						'Dbm':	[[37,40,44],[44,49,52],[49,52,56]],
						'D':	[[38,42,45],[45,50,54],[50,54,57]],
						'Dm':	[[38,41,45],[45,50,53],[50,53,57]],
						'Eb':	[[34,39,43],[43,46,51],[51,55,58]],
						'Ebm':	[[34,39,42],[46,51,54],[51,54,58]],
						'E':	[[35,40,44],[44,47,52],[47,52,56]],
						'Em':	[[35,40,43],[43,47,52],[47,52,57]],
						'F':	[[36,41,45],[48,53,57],[48,53,57]],
						'Fm':	[[36,41,44],[48,53,56],[48,53,56]],
						'F#':	[[37,42,46],[46,49,54],[49,54,58]],
						'F#m':	[[37,42,45],[45,49,54],[49,54,57]],
						'G':	[[38,43,47],[43,47,50],[50,55,59]],
						'Gm':	[[38,43,46],[43,46,50],[50,55,58]],
						'Ab':	[[39,44,48],[44,48,51],[51,56,60]],
						'Abm':	[[39,44,47],[44,47,51],[51,56,59]]}

open_chord_list = {		'A':	[[25,33,40],[33,40,49],[37,45,52]],
						'Am':	[[24,33,40],[33,40,48],[37,45,51]],
						'Bb':	[[26,34,41],[29,38,46],[34,41,50]],
						'Bbm':	[[25,34,41],[29,37,46],[34,41,49]],
						'B':	[[27,35,42],[30,39,47],[35,42,51]],
						'Bm':	[[26,35,42],[30,38,47],[35,42,50]],
						'C':	[[24,31,40],[31,40,48],[36,43,52]],
						'Cm':	[[24,31,39],[31,39,48],[36,43,51]],
						'C#':	[[25,32,41],[29,37,44],[37,44,53]],
						'Dbm':	[[25,32,40],[32,40,49],[37,44,52]],
						'D':	[[26,33,42],[30,38,45],[38,45,54]],
						'Dm':	[[26,33,41],[29,38,45],[38,45,53]],
						'Eb':	[[27,34,43],[31,39,46],[34,43,51]],
						'Ebm':	[[27,34,42],[30,39,46],[34,42,51]],
						'E':	[[28,35,44],[32,40,47],[35,44,52]],
						'Em':	[[28,35,43],[31,40,47],[35,43,52]],
						'F':	[[24,33,41],[29,36,45],[36,45,53]],
						'Fm':	[[24,32,41],[29,36,44],[36,44,53]],
						'F#':	[[25,34,42],[30,37,46],[34,42,49]],
						'F#m':	[[25,33,42],[30,37,45],[37,45,54]],
						'G':	[[26,35,43],[31,38,47],[35,43,50]],
						'Gm':	[[26,34,43],[31,38,46],[34,43,50]],
						'Ab':	[[24,32,39],[32,39,48],[36,44,51]],
						'Abm':	[[27,35,44],[32,39,47],[35,44,51]]}

beat_list44 = {			0:[[42,35],[42],[42,38],[42]], #basic 2-beat
						1:[[42,35],[42],[42,38],[42],[42,35],[42,35],[42,38],[42]], #basic rock beat 1
						2:[[42,35],[42],[42,38],[42,35],[42,35],[42],[42,38],[42]], #basic rock beat 2
						3:[[42,35],[42],[42,38],[42],[42,35],[42,35],[42,38],[42,35],[42],[42,35],[42,38],[42],[42,35],[42,35],[42,38],[42]], #basic rock beat 3
						4:[[42,35],[0],[38],[0],[42,35],[35],[42,38],[0]], #basic punk beat 1
						5:[[0],[0],[42],[42],[37],[0],[42],[42],[35],[0],[42],[42],[37],[0],[42],[42]], #basic reggae - but this relies on the empty brackets being interpreted as rests by the system. Will it work that way? I need to hear it in action as well, but this pattern may need to be at double speed compared to the others
}

beat_list34 = {			0:[[42,35],[42],[42,38]],
						1:[[42,35],[42,38],[42,38]],
						2:[[42,35],[42],[42,38],[42,35],[42,35],[42,38]],
						3:[[42,35],[42],[42],[42,35],[42,38],[42,35],[42,35],[42],[42,35],[42],[42,38],[42]],
						4:[[42,35],[42],[42],[42,35],[42,38],[42],[42,35],[42],[42,35],[42],[42,38],[42]],
						5:[[42,35],[42],[42],[42,38],[42],[42],[42,35],[42],[42,35],[42,38],[42],[42,35]]
}

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
		if (style == 0):
			midi_chords.append(closed_chord_list[chords[i]][(int(reg[i]))%len(closed_chord_list[chords[i]])])
		else:
			midi_chords.append(open_chord_list[chords[i]][(int(reg[i]))%len(closed_chord_list[chords[i]])])
	return midi_chords

def convert_beat_to_midi(beats, pattern, time_sig, inst, reg, speed):
	print "...Converting beats to MIDI values"
	midi_beats = [[0]]
	if (inst == 128):
		for i in range(int(len(beats)*speed)-int(speed)):
			if (time_sig == 4):
				midi_beats.append(beat_list44[pattern][i%len(beat_list44[int(pattern)])])
			else:
				midi_beats.append(beat_list34[pattern][i%len(beat_list34[int(pattern)])])
		midi_beats.append([49,51]) # the last drum hit is crash and ride
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
