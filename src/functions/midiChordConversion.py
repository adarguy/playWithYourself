import numpy as np

chord_list = {	'A':[57,61,64],
				'Am':[57,60,64],
				'Bb':[58,62,65],
				'Bbm':[58,61,65],
				'Bm':[59,62,66],
				'B':[59,63,66],
				'Bb':[59,62,66],
				'C':[60,64,67],
				'Cm':[60,63,67],
				'C#':[61,65,68],
				'Dbm':[61,64,68],
				'D':[62,66,69],
				'Dm':[62,65,69],
				'Eb':[63,67,70],
				'Ebm':[63,66,70],
				'E':[64,68,71],
				'Em':[64,67,71],
				'F':[65,69,72],
				'Fm':[65,68,72],
				'F#':[66,70,73],
				'F#m':[66,69,73],
				'F#':[66,70,73],
				'F#m':[66,69,73],
				'G':[67,71,74],
				'Gm':[67,70,74],
				'Ab':[68,72,75],
				'Abm':[68,69,75],
				}
""" I'm unsure how the chord list is being used.
Does the system recognize equivalence between F# and Gb?
Or do we need to account for that in the chord list.
Does it matter what range we are in?
The 50's to 70's are relatively high on the keyboard.
"""

def convert_chord_to_midi(chords):
	print "...Converting chord notes to MIDI values"
	midi_notes = [[0,0,0]]
	for i in range(len(chords)):
		midi_notes.append(chord_list[chords[i]])

	return midi_notes

def determine_durations(chords, startTimes, endTimes, frameIndex, volume):
	i = 0; j = 0;
	while (i < len(chords)-2):
		j = i + 1
		while (chords[j] == chords[i]):
			endTimes[i] = endTimes[j]
			chords =  np.delete(chords, j)
			startTimes =  np.delete(startTimes, j)
			endTimes =  np.delete(endTimes, j)
			if (volume[j] > volume[i]):
				volume[i] = volume[j]
			volume = np.delete(volume, j)
			frameIndex -= 1
		i += 1

	return chords, startTimes, endTimes, frameIndex, volume





