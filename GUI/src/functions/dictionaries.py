def instToPrgNum(inst):
	midi_programs = dict((b.lower(), a) for a,b in midi_inst.iteritems())
	return midi_programs[inst.lower()]

def prgNumToInst(num, p):
	if ((p==1 and num==35) or (p==2 and num==0) or (p==3 and num==128)):
		return midi_inst[num]+' (default)'
	return midi_inst[num]

def genreToPrgNum(genre):
	genres_list = dict((b.lower(), a) for a,b in genres_programs.iteritems())
	return genres_list[genre.lower()]

def prgNumToGenre(num):
	if (num==0):
		return genres_programs[num]+' (default)'
	return genres_programs[num]

def styleToPrgNum(style):
	style_programs = dict((b.lower(), a) for a,b in style_list.iteritems())
	return style_programs[style.lower()]

def getBusy(num):
	return busy_list[num]

def getDyn(num):
	return dyn_list[num]

def getWindow(num):
	return window_list[num]

def getStyle(num, p):
	if (num==0 and p==0):
		return style_list[num][p]+' (default)'
	return style_list[num][p]

def getTimeSig(num):
	if (num==4):
		return timesig_list[num]+' (default)'
	return timesig_list[num]

def getInstruments():
	return midi_inst

def getGenres():
	return genres_list

def speedToPrgNum(speed):
	return scale_tempo[speed.lower()]

style_list = {			0:'closed',
						1:'open'
}

timesig_list = {		3:'-triple-',
						4:'-quadruple-'
}

scale_tempo = {
						'half':0.5,
						'regular':1.0, 
						'double':2.0,
						'quadruple':3.0,
}

genres_programs = {
						0:'2-beat',
						1:'rock 1',
						2:'rock 2',
						3:'rock 3',
						4:'punk',
						5:'reggae'
}

busy_list = {			1:'-the busiest!-',
						2:'-damn busy-',
						3:'-officially busy-',
						4:'-gettin\' busy-',
						5:'-in the middle-',
						6:'-chillin out-',
						7:'-gettin\' lazy-',
						8:'-probably missed a few-',
						9:'-so NOT busy!-'
}

dyn_list = {			1:'-completely flat!-',
						2:'-almost gone-',
						3:'-gettin\' flat-',
						4:'-a lot of compression-',
						5:'-in the middle-',
						6:'-good compression-',
						7:'-balanced compression-',
						8:'-a bit of compression-',
						9:'-the slightest compression-',
						10:'-full dynamic range-'
}

window_list = {			1:'-the tiniest!-',
						2:'-very small-',
						3:'-small-',
						4:'-medium/small-',
						5:'-medium-',
						6:'-medium/large-',
						7:'-large-',
						8:'-very large-',
						9:'-so huge!-'
}

midi_inst = {			0:'Acoustic Grand Piano',
					    1:'Bright Acoustic Piano',
					    2:'Electric Grand Piano',
					    3:'Honky-tonk Piano',
					    4:'Electric Piano 1',
					    5:'Electric Piano 2',
					    6:'Harpsichord',
					    7:'Clavinet',
					    8:'Celesta',
					    9:'Glockenspiel',
					    10:'Music Box',
					    11:'Vibraphone',
					    12:'Marimba',
					    13:'Xylophone',
					    14:'Tubular Bells',
					    15:'Dulcimer',
					    16:'Drawbar Organ',
					    17:'Percussive Organ',
					    18:'Rock Organ',
					    19:'Church Organ',
					    20:'Reed Organ',
					    21:'Accordion',
					    22:'Harmonica',
					    23:'Tango Accordion',
					    24:'Acoustic Guitar (nylon)',
					    25:'Acoustic Guitar (steel)',
					    26:'Electric Guitar (jazz)',
					    27:'Electric Guitar (clean)',
					    28:'Electric Guitar (muted)',
					    29:'Overdriven Guitar',
					    30:'Distortion Guitar',
					    31:'Guitar Harmonics',
					    32:'Acoustic Bass',
					    33:'Electric Bass (finger)',
					    34:'Electric Bass (pick)',
					    35:'Fretless Bass',
					    36:'Slap Bass 1',
					    37:'Slap Bass 2',
					    38:'Synth Bass 1',
					    39:'Synth Bass 2',
					    40:'Violin',
					    41:'Viola',
					    42:'Cello',
					    43:'Contrabass',
					    44:'Tremolo Strings',
					    45:'Pizzicato Strings',
					    46:'Orchestral Harp',
					    47:'Timpani',
					    48:'String Ensemble 1',
					    49:'String Ensemble 2',
					    50:'Synth Strings 1',
					    51:'Synth Strings 2',
					    52:'Choir Aahs',
					    53:'Voice Oohs',
					    54:'Synth Choir',
					    55:'Orchestra Hit',
					    56:'Trumpet',
					    57:'Trombone',
					    58:'Tuba',
					    59:'Muted Trumpet',
					    60:'French Horn',
					    61:'Brass Section',
					    62:'Synth Brass 1',
					    63:'Synth Brass 2',
					    64:'Soprano Sax',
					    65:'Alto Sax',
					    66:'Tenor Sax',
					    67:'Baritone Sax',
					    68:'Oboe',
					    69:'English Horn',
					    70:'Bassoon',
					    71:'Clarinet',
					    72:'Piccolo',
					    73:'Flute',
					    74:'Recorder',
					    75:'Pan Flute',
					    76:'Blown bottle',
					    77:'Shakuhachi',
					    78:'Whistle',
					    79:'Ocarina',
					    80:'Lead 1 (square)',
					    81:'Lead 2 (sawtooth)',
					    82:'Lead 3 (calliope)',
					    83:'Lead 4 (chiff)',
					    84:'Lead 5 (charang)',
					    85:'Lead 6 (voice)',
					    86:'Lead 7 (fifths)',
					    87:'Lead 8 (bass + lead)',
					    88:'Pad 1 (new age)',
					    89:'Pad 2 (warm)',
					    90:'Pad 3 (polysynth)',
					    91:'Pad 4 (choir)',
					    92:'Pad 5 (bowed)',
					    93:'Pad 6 (metallic)',
					    94:'Pad 7 (halo)',
					    95:'Pad 8 (sweep)',
					    96:'FX 1 (rain)',
					    97:'FX 2 (soundtrack)',
					    98:'FX 3 (crystal)',
					    99:'FX 4 (atmosphere)',
					    100:'FX 5 (brightness)',
					    101:'FX 6 (goblins)',
					    102:'FX 7 (echoes)',
					    103:'FX 8 (sci-fi)',
					    104:'Sitar',
					    105:'Banjo',
					    106:'Shamisen',
					    107:'Koto',
					    108:'Kalimba',
					    109:'Bagpipe',
					    110:'Fiddle',
					    111:'Shanai',
					    112:'Tinkle Bell',
					    113:'Agogo',
					    114:'Steel Drums',
					    115:'Woodblock',
					    116:'Taiko Drum',
					    117:'Melodic Tom',
					    118:'Synth Drum',
					    119:'Reverse Cymbal',
					    120:'Guitar Fret Noise',
					    121:'Breath Noise',
					    122:'Seashore',
					    123:'Bird Tweet',
					    124:'Telephone Ring',
					    125:'Helicopter',
					    126:'Applause',
					    127:'Gunshot',
					    128:'Drum Set'
}

'''
    
            'Piano\n'
                '\tAcoustic Grand Piano\n'
                '\tBright Acoustic Piano\n'
                '\tElectric Grand Piano\n'
                '\tHonky-tonk Piano\n'
                '\tElectric Piano 1\n'
                '\tElectric Piano 2\n'
                '\tHarpsichord\n'
                '\tClavinet\n'
            'Chromatic Percussion\n'
                '\tCelesta\n'
                '\tGlockenspiel\n'
                '\tMusic Box\n'
                '\tVibraphone\n'
                '\tMarimba\n'
                '\tXylophone\n'
                '\tTubular Bells\n'
                '\tDulcimer\n'
            'Organ\n'
                '\tDrawbar Organ\n'
                '\tPercussive Organ\n'
                '\tRock Organ\n'
                '\tChurch Organ\n'
                '\tReed Organ\n'
                '\tAccordion\n'
                '\tHarmonica\n'
                '\tTango Accordion\n'
            'Guitar\n'
                '\tAcoustic Guitar (nylon)\n'
                '\tAcoustic Guitar (steel)\n'
                '\tElectric Guitar (jazz)\n'
                '\tElectric Guitar (clean)\n'
                '\tElectric Guitar (muted)\n'
                '\tOverdriven Guitar\n'
                '\tDistortion Guitar\n'
                '\tGuitar Harmonics\n'
            'Bass\n'
                '\tAcoustic Bass\n'
                '\tElectric Bass (finger)\n'
                '\tElectric Bass (pick)\n'
                '\tFretless Bass\n'
                '\tSlap Bass 1\n'
                '\tSlap Bass 2\n'
                '\tSynth Bass 1\n'
                '\tSynth Bass 2\n'
            'Strings\n'
                '\tViolin\n'
                '\tViola\n'
                '\tCello\n'
                '\tContrabass\n'
                '\tTremolo Strings\n'
                '\tPizzicato Strings\n'
                '\tOrchestral Harp\n'
                '\tTimpani\n'
            'Ensemble\n'
                '\tString Ensemble 1\n'
                '\tString Ensemble 2\n'
                '\tSynth Strings 1\n'
                '\tSynth Strings 2\n'
                '\tChoir Aahs\n'
                '\tVoice Oohs\n'
                '\tSynth Choir\n'
                '\tOrchestra Hit\n'
            'Brass\n'
                '\tTrumpet\n'
                '\tTrombone\n'
                '\tTuba\n'
                '\tMuted Trumpet\n'
                '\tFrench Horn\n'
                '\tBrass Section\n'
                '\tSynth Brass 1\n'
                '\tSynth Brass 2\n'
            'Reed\n'
                '\tSoprano Sax\n'
                '\tAlto Sax\n'
                '\tTenor Sax\n'
                '\tBaritone Sax\n'
                '\tOboe\n'
                '\tEnglish Horn\n'
                '\tBassoon\n'
                '\tClarinet\n'
            'Pipe\n'
                '\tPiccolo\n'
                '\tFlute\n'
                '\tRecorder\n'
                '\tPan Flute\n'
                '\tBlown bottle\n'
                '\tShakuhachi\n'
                '\tWhistle\n'
                '\tOcarina\n'
            'Synth Lead\n'
                '\tLead 1 (square)\n'
                '\tLead 2 (sawtooth)\n'
                '\tLead 3 (calliope)\n'
                '\tLead 4 (chiff)\n'
                '\tLead 5 (charang)\n'
                '\tLead 6 (voice)\n'
                '\tLead 7 (fifths)\n'
                '\tLead 8 (bass + lead)\n'
            'Synth Pad\n'
                '\tPad 1 (new age)\n'
                '\tPad 2 (warm[disambiguation needed])\n'
                '\tPad 3 (polysynth)\n'
                '\tPad 4 (choir)\n'
                '\tPad 5 (bowed)\n'
                '\tPad 6 (metallic)\n'
                '\tPad 7 (halo)\n'
                '\tPad 8 (sweep)\n'
            'Synth Effects\n'
                '\tFX 1 (rain)\n'
                '\tFX 2 (soundtrack)\n'
                '\tFX 3 (crystal)\n'
                '\tFX 4 (atmosphere)\n'
                '\tFX 5 (brightness)\n'
                '\tFX 6 (goblins)\n'
                '\tFX 7 (echoes)\n'
                '\tFX 8 (sci-fi)\n'
            'Ethnic\n'
                '\tSitar\n'
                '\tBanjo\n'
                '\tShamisen\n'
                '\tKoto\n'
                '\tKalimba\n'
                '\tBagpipe\n'
                '\tFiddle\n'
                '\tShanai\n'
            'Sound Effects\n'
                '\tGuitar Fret Noise\n'
                '\tBreath Noise\n'
                '\tSeashore\n'
                '\tBird Tweet\n'
                '\tTelephone Ring\n'
                '\tHelicopter\n'
                '\tApplause\n'
                '\tGunshot\n')
    
    print ("\nThe valid MIDI PERCUSSION INSTRUMENTS are:\n"
            'Drum-set\n'
            'Tinkle Bell\n'
            'Agogo\n'
            'Steel Drums\n'
            'Woodblock\n'
            'Taiko Drum\n'
            'Melodic Tom\n'
            'Synth Drum\n'
            'Reverse Cymbal\n')
'''
