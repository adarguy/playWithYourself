import numpy as np

midi_programs = { 		'bass':35,
						'piano':0,
						'drums':0}	

genres_list = {			'rock':0,
						'reggae':1,
						'r&b':2}

root_postion = {		'A':[[57,61,64]],
						'Am':[[57,60,64]],
						'Bb':[[58,62,65]],
						'Bbm':[[58,61,65]],
						'Bm':[[59,62,66]],
						'B':[[59,63,66]],
						'Bb':[[59,62,66]],
						'C':[[60,64,67]],
						'Cm':[[60,63,67]],
						'C#':[[61,65,68]],
						'Dbm':[[61,64,68]],
						'D':[[62,66,69]],
						'Dm':[[62,65,69]],
						'Eb':[[63,67,70]],
						'Ebm':[[63,66,70]],
						'E':[[64,68,71]],
						'Em':[[64,67,71]],
						'F':[[65,69,72]],
						'Fm':[[65,68,72]],
						'F#':[[66,70,73]],
						'F#m':[[66,69,73]],
						'F#':[[66,70,73]],
						'F#m':[[66,69,73]],
						'G':[[67,71,74]],
						'Gm':[[67,70,74]],
						'Ab':[[68,72,75]],
						'Abm':[[68,69,75]]}

closed_chord_list = {	'A':[[40,45,49],[45,49,52], [52,57,61],[25,33,40],[33,40,49],[37,45,52]],
						'Am':[[40,45,48], [45,48,52], [52,57,60],[24,33,40],[33,40,48],[37,45,51]],
						'Bb':[[38,41,46], [46,50,53], [53,58,62],[26,34,41]],[29,38,46],[34,41,50]],
						'Bbm':[[37,41,46], [46,49,53], [53,58,61],[25,34,41],[29,37,46],[34,41,49]],
						'B':[[39,42,47], [47,51,54], [54,59,63],[27,35,42],[30,39,47],[35,42,51]],
						'Bm':[[38,42,47], [47,50,54], [54,59,62],[26,35,42],[30,38,47],[35,42,50]],
						'C':[[36,40,43], [43,48,52], [48,52,55],[24,31,40],[31,40,48],[36,43,52]],
						'Cm':[[36,39,43], [43,48,51], [48,51,55],[24,31,39],[31,39,48],[36,43,51]],
						'C#':[[37,41,44], [44,49,53], [49,53,56],[25,32,41],[29,37,44],[37,44,53]],
						'Dbm':[[37,40,44], [44,49,52], [49,52,56],[25,32,40],[32,40,49],[37,44,52]],
						'D':[[38,42,45], [45,50,54], [50,54,57],[26,33,42],[30,38,45],[38,45,54]],
						'Dm':[[38,41,45], [45,50,53], [50,53,57],[26,33,41],[29,38,45],[38,45,53]],
						'Eb':[[34,39,43], [43,46,51], [51,55,58],[27,34,43],[31,39,46],[34,43,51]],
						'Ebm':[[34,39,42], [46,51,54], [51,54,58],[27,34,42],[30,39,46],[34,42,51]],
						'E':[[35,40,44], [44,47,52], [47,52,56],[28,35,44],[32,40,47],[35,44,52]],
						'Em':[[35,40,43], [43,47,52], [47,52,57],[28,35,43],[31,40,47],[35,43,52]],
						'F':[[36,41,45], [48,53,57], [48,53,57],[24,33,41],[29,36,45],[36,45,53]],
						'Fm':[[36,41,44], [48,53,56], [48,53,56],[24,32,41],[29,36,44],[36,44,53]],
						'F#':[[37,42,46], [46,49,54], [49,54,58],[25,34,42],[30,37,46],[34,42,49]],
						'F#m':[[37,42,45], [45,49,54], [49,54,57],[25,33,42],[30,37,45],[37,45,54]],
						'G':[[38,43,47], [43,47,50], [50,55,59],[26,35,43],[31,38,47],[35,43,50]],
						'Gm':[[38,43,46], [43,46,50], [50,55,58],[26,34,43],[31,38,46],[34,43,50]],
						'Ab':[[39,44,48], [44,48,51], [51,56,60],[24,32,39],[32,39,48],[36,44,51]],
						'Abm':[[39,44,47], [44,47,51], [51,56,59],[27,35,44],[32,39,47],[35,44,51]]}
"""
Should no longer be called "closed_chord_list" since it includes open chord shapes as well for items 4-6.
Should probably just be labeled "chord_list" now,
but I don't want to change the name without knowing all of the places it's being called.
"""

beat_list44 = {			0:[[42,35],[42],[42,38],[42]],
						1:[[42,35],[42],[42,38],[42]]}

beat_list34 = {			0:[[42,35],[42],[42,38]],
						1:[[42,35],[42],[42,38]]}

def convert_note_to_midi(notes, reg):
	print "...Converting notes to MIDI values"
	midi_notes = [[0]]
	for i in range(len(notes)):
		midi_notes.append([closed_chord_list[notes[i]][(int(reg[i])/2)%len(closed_chord_list[notes[i]])][0]])

	return midi_notes

def convert_chord_to_midi(chords, reg, style):
	print "...Converting chords to MIDI values"
	midi_chords = [[0,0,0]]
	for i in range(len(chords)):
		if (style == 0.0):
			midi_chords.append(closed_chord_list[chords[i]][(int(reg[i])/2)%len(closed_chord_list[chords[i]])])
		else:
			midi_chords.append(root_postion[chords[i]])
	return midi_chords

def convert_beat_to_midi(beats, pattern, time_sig):
	print "...Converting beats to MIDI values"
	midi_beats = [[0]]
	for i in range(len(beats)):
		if (time_sig == 4.0):
			midi_beats.append(beat_list44[int(pattern)][i%len(beat_list44[int(pattern)])])
		else:
			midi_beats.append(beat_list34[int(pattern)][i%len(beat_list34[int(pattern)])])
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
