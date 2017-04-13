import argparse, warnings, logging, subprocess, sys, os, ntpath
import scikits.audiolab as audiolab
import numpy as np
import midiConversion

def help():
    print ("\nWelcome to Play With Yourself!\n" #App Description
    "An Accompaniment tool for the modern musician\n\n"
    "Play With Yourself is an accompaniment tool that allows users to\n"
    "create automatic accompaniments to their working songs and projects.\n"
    "This has been developed in part for a university class on music\n"
    "information retrieval hosted at the University of Victoria, BC Canada.\n"
    "Contact the administrator with any inquiries at adarguy10@gmail.com\n")
    
    print ("\nThe valid COMMANDS are:\n" #Command Description
    "load <filename>            -- to read in a wav audio file\n"
    "save <filename> <path>     -- to save accompaniment to specified location\n"
    "diagnostics <toggle>       -- to report diagnostics on the input audio file during processing (specify before loading file)\n"
    "savesettings               -- to save back to a different file\n"
    "printcontrols              -- print user/default settings for accompaniment <n>\n"
    "help                       -- to display this help message\n"
    "quit                       -- to exit the program\n")
    
    print ("\nThe valid USER INPUTS are:\n" #Parameter Description
    "Busyness <num>             -- Onset (beat) threshold\n"
    "Dynamics <num>             -- Dynamics threshold\n"
    "Window <size>              -- Beat Correction Window Size\n"
    "Instrument 1 <name>        -- Instrument for Melodic Accompaniment\n"
    "Instrument 2 <name>        -- Instrument for Harmonic Accompaniment\n"
    "Instrument 3 <name>        -- Instrument for Percussive Accompaniment\n"
    "Pattern <genre>            -- Pattern for Percussive Accompaniment\n"
    "Chord Style <style>        -- Closed or Open Chords for Harmonic Accompaniment\n"
    "Time Signature <num>       -- Chosen Time Signature (3/4 or 4/4 only)\n")

    print ("\nThe valid INSTRUMENT INPUTS are:\n" #Parameter Description
    "Piano                      -- General MIDI Acoustic Piano\n"
    "EBass                      -- General MIDI Electric Bass\n"
    "Drum-set                   -- General MIDI Drum-set\n")

def convert_settings(s):
    final = {}
    try:
        y, sr = librosa.load(settings[0])
        final['filename'] = settings[0]
        final['y'] = y
        final['sr'] = sr
    except:
        print "File does not exist or is corrupt"
        return 0

    final['busy'] = float(settings[1])/10
    final['dyn'] = float(settings[2])/10
    try:
        final['window'] = float(settings[3])/10
    except:
        if (settings[3] == 'xs'):
            final['window'] = 0.1
        elif (settings[3] == 's'):
            final['window'] = 0.3
        elif (settings[3] == 'm'):
            final['window'] = 0.5
        elif (settings[3] == 'l'):
            final['window'] = 0.7
        elif (settings[3] == 'xl'):
            final['window'] = 0.9
        else:
            print "Invalid user input. Try Again"
            return 0

        UI_instrument_notes = float(settings[4]);   UI_onset_threshold = float(settings[1]);
        UI_instrument_chords = float(settings[5]);  UI_dynamic_threshold = float(settings[2]);
        UI_instrument_beats = float(settings[6]);   UI_beat_windowSize = float(settings[3]); #300 msec
        UI_beat_pattern = float(settings[7]);       UI_chord_style = float(settings[8]);
        UI_time_signature = float(settings[9]);     

def get_arguments(f, dic):
    while (True):
        config = raw_input('Would you like to use default settings or configure manually? --default/manual\n')
        config = config.lower()
        if (config == 'default' or config == 'd' or config == 'manual' or config == 'm'):
            break;
        else:
            print "Invalid Input. Please try again."

    settings = [0]*10; settings[0] = f;
    if (config == 'manual' or config == 'm'):
        while (True):
            settings[1] = raw_input('\nBusyness (integer): ')
            try:
                if (int(settings[1]) <= 9 and int(settings[1]) >= 1):
                    dic['busy'] = int(settings[1])/10.0
                    break;
                else: print "Input is not between 1 - 9"
            except:
                print "input is not an integer type"

        while (True):
            settings[2] = raw_input('Dynamics (integer): ')
            try:
                if (int(settings[2]) <= 9 and int(settings[2]) >= 1):
                    dic['dyn'] = int(settings[2])/10.0
                    break;
                else: print "Input is not between 1 - 9"
            except:
                print "input is not an integer type"

        while (True):
            settings[3] = raw_input('Window Size (integer): ')
            try:
                if (int(settings[3])):
                    if (int(settings[3]) <= 9 and int(settings[3]) >= 1):
                        dic['window'] = int(settings[3])/10.0
                        break;
                    else: print "Input is not between 1 - 9"
                if (settings[3] == 'xs'): dic['window'] = 0.1; break
                elif (settings[3] == 's'): dic['window'] = 0.3; break
                elif (settings[3] == 'm'): dic['window'] = 0.5; break
                elif (settings[3] == 'l'): dic['window'] = 0.7; break
                elif (settings[3] == 'xl'): dic['window'] = 0.9; break
                else:
                    print "Input must be 'xs', 's', 'm', 'l', 'xl', or valid integer."
            except:
                print "Invalid Input. Type help for a list of valid inputs."

        while (True):
            settings[4] = raw_input('Instrument One (name): ')
            try:
                dic['inst1'] = int(midiConversion.programs(settings[4]))
                break;
            except:
                print "Input is not in the list of valid instruments. Type help for a list of valid instruments."

        while (True):
            settings[5] = raw_input('Instrument Two (name): ')
            try:
                dic['inst2'] = int(midiConversion.programs(settings[5]))
                break;
            except:
                print "Input is not in the list of valid instruments. Type help for a list of valid instruments."

        while (True):
            settings[6] = raw_input('Instrument Three (name): ')
            try:
                dic['inst3'] = int(midiConversion.programs(settings[6]))
                break;
            except:
                print "Input is not in the list of valid instruments. Type help for a list of valid instruments."

        while (True):
            settings[7] = raw_input('Pattern (genre): ')
            try:
                dic['pattern'] = int(midiConversion.genres(settings[7]))
                break;
            except:
                print "Input is not in the list of valid genres. Type help for a list of valid genres."
        
        while (True):
            settings[8] = raw_input('Chord Style (closed or open): ')
            if (settings[8] == 'closed'):
                dic['style'] = 0; break;
            elif (settings[8] == 'open'):
                dic['style'] = 1; break;
            else:
                print "Invalid input. Must be either 'open' or 'closed'."

        while (True):
            settings[9] = raw_input('Time Signature (3 or 4): ')
            try:
                if (int(settings[9]) == 4 or int(settings[9]) == 3):
                    dic['timeSig'] = int(settings[9]);
                    break;
                else:
                    print "Invalid input. Must be either '3' or '4'."
            except:
                print "Input is not a valid integer type."
    else:
        dic['busy'] = 0.1
        dic['dyn'] = 0.7
        dic['window'] = 0.3
        dic['inst1'] = 35
        dic['inst2'] = 0
        dic['inst3'] = 0
        dic['pattern'] = 0
        dic['style'] = 0
        dic['timeSig'] = 4

    return dic

def process_arguments(args, UI_show, settings):
    dic = settings
    try:
        cmd, param1, param2 = args.split()
    except:
        try:
            cmd, param = args.split()
        except:
            cmd = args
    if (cmd == 'load'):
        try:
            filename = param;
            print filename
            if (os.path.isfile(filename)):
                dic['filename'] = filename
            else:
                print "File does not exist or is corrupt."
                return cmd, UI_show, dic
        except:
            print "no file specified"
            return cmd, UI_show, dic

        logging.captureWarnings(not UI_show)
        dic = get_arguments(filename, dic)

        print "...Opening '" + ntpath.basename(dic['filename']) + "'"
    
    elif (cmd == 'save'):
        print "This piece of the program has not yet been implemented. The .mid file will be saved in the directory of the input audio file.\n"
    elif (cmd == 'help'):
        help()
    elif (cmd == 'quit'):
        sys.exit()
    elif (cmd == 'diagnostics'):
        try:
            if (param == 'on'):
                UI_show = True
                print "Diagnostics are on"
            else:
                UI_show = False
                print "Diagnostics are off"
        except:
            print "toggle (on/off) not specified"
            return cmd, UI_show, dic
    elif (cmd == 'printcontrols'):
        print dic
    elif (cmd == 'savesettings'):
        save = True;
    else:
        print "Invalid Command. Type help for a list of valid commands"

    return cmd, UI_show, dic

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx], idx

def preview(filename):
    FNULL = open(os.devnull, 'w')
    subprocess.call(['fluidsynth', '-T', 'wav', '-F', filename[:-4]+'.raw', '-ni', '../lib/sf2/sf.sf2', filename[:-4]+'.mid', '-g', '0.8', '-r', '22050'], stdout=FNULL, stderr=subprocess.STDOUT)
    subprocess.call(['SoX', '-t', 'raw', '-r', '22050','-e', 'signed', '-b', '16', '-c', '1', filename[:-4]+'.raw', filename[:-4]+'_temp.wav'])
    
    frames1, fs1, encoder1 = audiolab.wavread(filename[:-4]+'_temp.wav')
    frames2, fs2, encoder2 = audiolab.wavread(filename)

    mixed = np.zeros(max(len(frames1), len(frames2)), dtype=frames1.dtype)
    mixed[:len(frames1)] += frames1 / 2
    mixed[:len(frames2)] += frames2 / 2

    audiolab.play(mixed[:len(mixed)/4], fs=44100)
    result = raw_input('Are you happy with this accompaniment? --yes/no\n')
    
    if (result == 'yes'): return True
    return False
    
def clean(filename):
    print "...Finalizing Output"
    os.remove(filename[:-4]+'_temp.wav')
    os.remove(filename[:-4]+'.raw')
    print "...Accompaniment Completed"