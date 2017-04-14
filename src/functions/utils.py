import argparse, warnings, logging, subprocess, sys, os, ntpath
import scikits.audiolab as audiolab
import numpy as np

import dictionaries

def fmtcols(mylist, cols):
    maxwidth = max(map(lambda x: len(x), mylist))
    justifyList = map(lambda x: x.ljust(maxwidth), mylist)
    lines = (' '.join(justifyList[i:i+cols]) for i in xrange(0,len(justifyList),cols))
    return "\n".join(lines)

def instruments():
    inst_list = dictionaries.getInstruments().values()
    print "\nValid MIDI instrument options are:\n"
    print fmtcols(inst_list, 4)

def help():
    print ("\nWelcome to Play With Yourself!\n" #App Description
    "An Accompaniment tool for the modern musician\n\n"
    "Play With Yourself is an accompaniment tool that allows users to\n"
    "create automatic accompaniments to their working songs and projects.\n"
    "This has been developed in part for a university class on music\n"
    "information retrieval hosted at the University of Victoria, BC Canada.\n"
    "Contact the administrator with any inquiries at adarguy10@gmail.com\n")
    
    print ("\nValid program commands are:\n" #Command Description
    "load <filename>              -- read in a wav audio file and start accompaniment creation\n"
    "save <filename> <path>       -- save accompaniment to specified location\n"
    "diagnostics <toggle>         -- report diagnostics on the input audio file during processing (specify before loading file)\n"
    "settings <cmd>               -- save or print the settings for a previously created accompaniment\n"
    "instruments                  -- show a list of all available MIDI instrument options\n"
    "help                         -- display this help message\n"
    "quit                         -- exit the program\n")

    print ("\nValid user settings (after load) are:\n" #Parameter Description
    "default (recommended)        -- use default program settings for the accompaniment\n"
    "saved                        -- use saved program settings from previous accompaniment (if settings are saved)\n"
    "manual                       -- configure program settings manually\n\n"

    "Settings Options:\n"
    "  -Busyness- <num>           -- onset (beat) detection threshold (1-10)\n"
    "  -Dynamics- <num>           -- dynamics threshold (1-10)\n"
    "  -Window- <num>             -- beat correction window size (1-10)\n"
    "  -Instrument 1- <name>      -- instrument for melodic accompaniment (valid instrument option)\n"
    "  -Instrument 2- <name>      -- instrument for harmonic accompaniment (valid instrument option)\n"
    "  -Instrument 3- <name>      -- instrument for percussive accompaniment (valid instrument option)\n"
    "  -Pattern- <genre>          -- pattern by genre for percussive accompaniment (valid genre option)\n"
    "  -Chord Style- <style>      -- chord style for harmonic accompaniment (closed or open)\n"
    "  -Time Signature- <num>     -- time signature for accompaniment (3/4 or 4/4 only)\n")

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

def get_arguments(f, dic, saved):
    while (True):
        if (saved == True):
            config = raw_input('\nWould you like to use default settings, saved settings or configure manually?\n')
            config = config.lower()
        else:
            config = raw_input('\nWould you like to use default settings or configure manually?\n')
            config = config.lower()
        
        if (config == 'default' or config == 'manual'):
            break
        elif (config == 'saved'):
            if (len(dic) == 0):
                print "WHAT"
            else:
                print "\nUsing saved settings from previous accompaniment build.\n"
                break
        else:
            print "Invalid Input. Please try again."

    settings = [0]*10; settings[0] = f;
    if (config == 'manual'):
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
                dic['inst1'] = int(dictionaries.instToPrgNum(settings[4]))
                break;
            except:
                print "Input is not in the list of valid instruments. Type help for a list of valid instruments."

        while (True):
            settings[5] = raw_input('Instrument Two (name): ')
            try:
                dic['inst2'] = int(dictionaries.instToPrgNum(settings[5]))
                break;
            except:
                print "Input is not in the list of valid instruments. Type help for a list of valid instruments."

        while (True):
            settings[6] = raw_input('Instrument Three (name): ')
            try:
                inst = int(dictionaries.instToPrgNum(settings[6]))
                perc_insts = [112, 113, 114, 115, 116, 117, 118, 119, 128]; good=True;
                if (inst not in perc_insts):
                    print "This instrument is not a common percussion instrument. Continuing will result in an unexpected accompaniment."
                    while (True):
                        try:
                            cont = raw_input('Would you like to continue with this choice?')
                            try:
                                assert cont == 'yes'   
                            except:
                                assert cont == 'no'
                                good = False;
                            break;
                        except:
                            print "Invalid input. Must be either yes or no."
                dic['inst3'] = inst
                if (good): break;
            except:
                print "Input is not in the list of valid instruments. Type help for a list of valid instruments."

        while (True):
            settings[7] = raw_input('Pattern (genre): ')
            try:
                dic['pattern'] = int(dictionaries.genreToPrgNum(settings[7]))
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
        dic['default'] = False
    elif (config == "default"):
        dic = default_settings(dic)

    return dic

def process_arguments(args, UI_show, settings, save):
    dic = settings
    try:
        cmd, param1, param2 = args.lower().split()
    except:
        try:
            cmd, param = args.lower().split()
        except:
            cmd = args
    if (cmd == 'load'): #1
        try:
            filename = param;
            if (os.path.isfile(filename)):
                dic['filename'] = filename
                logging.captureWarnings(not UI_show)
                dic = get_arguments(filename, dic, save)               
                print "...Opening '" + ntpath.basename(dic['filename']) + "'"
                cmd += '_yes'
            else:
                print "\nFile does not exist or is corrupt."
        except:
            print "\nNo file specified"
    elif (cmd == 'save'): #2
        print "\nThis piece of the program has not yet been implemented. The .mid file will be saved in the directory of the input audio file."
    elif (cmd == 'help'): #3
        help()
    elif (cmd == 'quit'): #4
        sys.exit()
    elif (cmd == 'diagnostics'): #5
        try:
            try:
                assert param == 'on'
                UI_show = True
                print "\nDiagnostics are on"
            except:
                assert param == 'off'
                UI_show = False
                print "\nDiagnostics are off"
        except:
            print "\nDiagnostics toggle (on/off) not specified."
    elif (cmd == 'settings'): #6
        if (dic['default']):
            print "\nDefault setting are currently being used. To configure manual settings, load a file and specify manual for settings configuration."
        try:
            try:
                assert param == 'save'
                save = True
                print "\nSettings have been saved."
            except:
                assert param == 'print'
                if (save):
                    print "Busyness: "+str(int(dic['busy']*10))+" "+dictionaries.getBusy(int(dic['busy']*10))
                    print "Dynamics: "+str(int(dic['dyn']*10))+" "+dictionaries.getDyn(int(dic['dyn']*10))
                    print "Window Size: "+str(int(dic['window']*10))+" "+dictionaries.getWindow(int(dic['window']*10))
                    
                    print "Instrument 1: "+dictionaries.prgNumToInst(int(dic['inst1']), 1)+" -melodic-"
                    print "Instrument 2: "+dictionaries.prgNumToInst(int(dic['inst2']), 2)+" -harmonic-"
                    print "Instrument 3: "+dictionaries.prgNumToInst(int(dic['inst3']), 3)+" -percussive-"
                    print "Pattern: "+dictionaries.prgNumToGenre(int(dic['pattern']))+" -percussive-"
                    
                    print "Chord Style: "+dictionaries.getStyle(dic['style'], 0)+" "+dictionaries.getStyle(dic['style'], 1)
                    print "Time Signature: "+str(dic['timeSig'])+"/4 "+dictionaries.getTimeSig(int(dic['timeSig']))
                else:
                    print "\nSettings must be saved before they are printed."
        except:
            print "\nSettings command (save/print) not specified."
    elif (cmd == 'instruments'): #7
        instruments()
    else:
        print "\nInvalid Command. Type help for a list of valid commands."
    
    return cmd, UI_show, dic, save

def default_settings(dic):
    dic['busy'] = 0.1
    dic['dyn'] = 0.7
    dic['window'] = 0.3
    dic['inst1'] = 35
    dic['inst2'] = 0
    dic['inst3'] = 128
    dic['pattern'] = 0
    dic['style'] = 0
    dic['timeSig'] = 4
    dic['default'] = True
    return dic

def set_defaults():
    UI_show = False; save = False; settings = {}
    settings = default_settings(settings)
    return UI_show, settings, save

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
    
    
def clean(filename):
    while (True):
        result = raw_input('Are you happy with this accompaniment? --yes/no\n')
        try:
            print '...Finalizing Output'
            os.remove(filename[:-4]+'_temp.wav')
            os.remove(filename[:-4]+'.raw')
            if (result=='yes'):         
                print "...Accompaniment Completed"
                break;
            elif (result=='no'):
                os.remove(filename[:-4]+'.mid')
                print "OK. Lets start again."
                break;
            else: assert result==('yes'or'no')
        except:
            print "Invalid input. Must be either yes or no."
    
