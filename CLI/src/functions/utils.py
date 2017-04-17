import argparse, warnings, logging, subprocess, sys, os, ntpath
import scikits.audiolab as audiolab
import numpy as np

import dictionaries

def instruments():
    inst_list = dictionaries.getInstruments()
    genre_list = dictionaries.getGenres()
    print "\nValid MIDI instrument options are:"
    print fmtcols(inst_list, 4)
    print "\nValid Percussive MIDI instrument options are:"
    print fmtcols(genre_list, 1)


def help():
    print ("\nWelcome to Play With Yourself!\n" #App Description
    "A music accompaniment tool for the modern musician\n\n"
    "Play With Yourself is an accompaniment tool that allows users to\n"
    "create automatic accompaniments to their working songs and projects.\n"
    "This has been developed in part for a university class on music\n"
    "information retrieval hosted at the University of Victoria, BC Canada.\n"
    "Contact the administrator with any inquiries at adarguy10@gmail.com\n")
    
    print ("\nValid program commands are:\n" #Command Description
    "load <filename>                -- read in a wav audio file and start accompaniment creation\n"
    "save <filename> <path>         -- save accompaniment to specified location\n"
    "diagnostics <toggle>           -- report diagnostics on the input audio file during processing (specify before loading file)\n"
    "settings <cmd>                 -- save or print the settings for a previously created accompaniment\n"
    "options                        -- show a list of all available MIDI instrument and genre options\n"
    "help                           -- display this help message\n"
    "quit                           -- exit the program\n")

    print ("\nValid user settings (after load) are:\n" #Parameter Description
    "default (recommended)          -- use default program settings for the accompaniment\n"
    "saved                          -- use saved program settings from previous accompaniment (if settings are saved)\n"
    "manual                         -- configure program settings manually\n\n"

    "General Settings Options:\n"   
    "  -Instrument 1- <name>        -- instrument for melodic accompaniment (type options for a list of instruments)\n"
    "  -Instrument 2- <name>        -- instrument for harmonic accompaniment (type options for a list of instruments)\n"
    "  -Instrument 3- <name>        -- instrument for percussive accompaniment (type options for a list of instruments)\n"
    "  -Percussion Style- <genre>   -- pattern by genre for percussive accompaniment (type options for a list of genres)\n"
    "  -Time Signature- <num>       -- time signature for accompaniment (3/4 or 4/4 only)\n"
    
    "Advanced Settings Options:\n"
    "  -Busyness- <num>             -- onset (beat) detection threshold (1-10)\n"
    "  -Dynamics- <num>             -- dynamics threshold (1-10)\n"
    "  -Window- <num>               -- beat correction window by number (1-10)\n"
    "  -Window- <size>              -- beat correction window by size (xs-xl)\n"
    "  -Preview Window- <size>      -- length of preview (quarter, half, full)\n"
    "  -Chord Style- <style>        -- chord style for harmonic accompaniment (closed or open)\n" 
    "  -Tempo- <size>               -- speed of accompaniment (half, regular, double, quadruple)\n")

def get_settings(f, dic, saved):
    while (True):
        if (saved == True):
            config = raw_input("\nWould you like to use default settings, saved settings or a manual configuration? Type 'manual advanced' for more options.\n")
        else:
            config = raw_input("\nWould you like to use default settings or a manual configuration? Type 'manual advanced' for more options.\n") 
        try:
            config, advanced = config.lower().split()
            if (advanced != 'advanced'): 
                print "Invalid Input. Type 'manual advanced' to get more configuration options."
                continue
            advanced = True;
        except:
            config = config.lower()
            advanced = False;
        if (config == 'default' or config == 'manual'):
            break
        elif (config == 'saved'):
            if (len(dic) == 0):
                print "WHAT"
            else:
                print "\nUsing saved settings from previous accompaniment build.\n"
                break
        else:
            print "Invalid Input. Must be either 'default' or 'manual'."

    settings = [0]*12; settings[0] = f;
    if (config == 'manual'):
        while (True):
            settings[4] = raw_input('\nInstrument One (name): ')
            try:
                dic['inst1'] = int(dictionaries.instToPrgNum(settings[4]))
                break;
            except:
                print "Input is not in the list of valid instruments. Type 'help' for a list of valid instruments."

        while (True):
            settings[5] = raw_input('Instrument Two (name): ')
            try:
                dic['inst2'] = int(dictionaries.instToPrgNum(settings[5]))
                break;
            except:
                print "Input is not in the list of valid instruments. Type 'help' for a list of valid instruments."

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
                                inst += 1000  
                            except:
                                assert cont == 'no'
                                good = False
                            break;
                        except:
                            print "Invalid input. Must be either 'yes' or 'no'."
                dic['inst3'] = inst
                if (good): break
            except:
                print "Input is not in the list of valid instruments. Type 'help' for a list of valid instruments."
        
        while (True):
            settings[7] = raw_input('Percussion Style (genre): ')
            try:
                dic['pattern'] = int(dictionaries.genreToPrgNum(settings[7]))
                break;
            except:
                print "Input is not in the list of valid genres. Type 'help' for a list of valid genres."
        
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

        #Advanced Settings
        while (advanced):
            settings[1] = raw_input('Busyness (integer): ')   
            try:
                settings[1] = int(settings[1])
                if (settings[1] <= 9 and settings[1] >= 1):
                    dic['busy'] = settings[1]
                    break;
                else: print "Input is not between 1 - 9."
            except:
                print "Input is not an integer type."

        while (advanced):
            settings[2] = raw_input('Dynamics (integer): ')
            try:
                settings[2] = int(settings[2])
                if (int(settings[2]) <= 9 and int(settings[2]) >= 1):
                    dic['dyn'] = int(settings[2])/10.0
                    break;
                else: print "Input is not between 1 - 9."
            except:
                print "Input is not an integer type."

        while (advanced):
            settings[3] = raw_input('Window Size (integer): ')
            try:      
                if (settings[3] == 'xs'): dic['window'] = 0.1; break
                elif (settings[3] == 's'): dic['window'] = 0.3; break
                elif (settings[3] == 'm'): dic['window'] = 0.5; break
                elif (settings[3] == 'l'): dic['window'] = 0.7; break
                elif (settings[3] == 'xl'): dic['window'] = 0.9; break
                elif (int(settings[3])):
                    if (int(settings[3]) <= 9 and int(settings[3]) >= 1):
                        dic['window'] = int(settings[3])/10.0
                        break;
                    else: print "Input is not between 1 - 9"
                else:
                    print "Input must be 'xs', 's', 'm', 'l', 'xl', or valid integer."
            except:
                print "Invalid Input. Type 'help' for a list of valid inputs."
        
        while (advanced):
            settings[11] = raw_input('Preview Window (size): ').lower()
            if (settings[11] == 'quarter'):
                dic['preview'] = 0.25; break;
            elif (settings[11] == 'half'):
                dic['preview'] = 0.5; break;
            elif (settings[11] == 'full'):
                dic['preview'] = 1.0; break;
            else:
                print "Invalid input. Must be either 'quarter', 'half' or 'full'."
        
        while (advanced):
            settings[8] = raw_input('Chord Style (closed or open): ').lower()
            if (settings[8] == 'closed'):
                dic['style'] = 0; break;
            elif (settings[8] == 'open'):
                dic['style'] = 1; break;
            else:
                print "Invalid input. Must be either 'open' or 'closed'."

        while (advanced):
            settings[10] = raw_input('Tempo (scalar): ').lower()
            try:
                dic['speed'] = float(dictionaries.speedToPrgNum(settings[10]))
                break;
            except:
                print "Invalid input. Must be either 'half', 'regular', 'double' or 'quadruple'."
        dic['default'] = False
    elif (config == "default"):
        UI_show, dic, save = set_defaults(dic)
    return dic

def process_command(args, UI_show, settings, save):
    dic = settings
    try:
        cmd, param1, param2 = args.lower().split()
    except:
        try:
            cmd, param = args.split()
            cmd = cmd.lower()
        except:
            cmd = args.lower()
    if (cmd == 'load'): #1
        try:
            filename = param;
            if (os.path.isfile(filename)):
                dic['filename'] = filename
                logging.captureWarnings(not UI_show)
                dic = get_settings(filename, dic, save)               
                print "\n...Opening '" + ntpath.basename(dic['filename']) + "'"
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
                assert param.lower() == 'on'
                UI_show = True
                print "\nDiagnostics are on"
            except:
                assert param.lower() == 'off'
                UI_show = False
                print "\nDiagnostics are off"
        except:
            print "\nDiagnostics toggle (on/off) not specified."
    elif (cmd == 'settings'): #6
        if (dic['default']):
            print "\nDefault setting are currently being used. To configure manual settings, load a file and specify manual for settings configuration."
        try:
            try:
                assert param.lower() == 'save'
                save = True
                print "\nSettings have been saved."
            except:
                assert param.lower() == 'print'
                if (save):
                    print "Busyness: "+str(int(dic['busy']))+" "+dictionaries.getBusy(int(dic['busy']))
                    print "Dynamics: "+str(int(dic['dyn']))+" "+dictionaries.getDyn(int(dic['dyn']))
                    print "Window Size: "+str(int(dic['window']))+" "+dictionaries.getWindow(int(dic['window']))
                    
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
    elif (cmd == 'options'): #7
        instruments()
    else:
        print "\nInvalid Command. Type 'help' for a list of valid commands."
    
    return cmd, UI_show, dic, save

def preview(filename, length):
    print '...Previewing Accompaniment'
    FNULL = open(os.devnull, 'w')
    subprocess.call(['fluidsynth', '-T', 'wav', '-F', filename[:-4]+'.raw', '-ni', '../lib/sf2/sf.sf2', filename[:-4]+'.mid', '-g', '0.8', '-r', '22050'], stdout=FNULL, stderr=subprocess.STDOUT)
    subprocess.call(['SoX', '-t', 'raw', '-r', '22050','-e', 'signed', '-b', '16', '-c', '1', filename[:-4]+'.raw', filename[:-4]+'_temp.wav'])
    
    frames1, fs1, encoder1 = audiolab.wavread(filename[:-4]+'_temp.wav')
    frames2, fs2, encoder2 = audiolab.wavread(filename)

    mixed = np.zeros(max(len(frames1), len(frames2)), dtype=frames1.dtype)
    mixed[:len(frames1)] += frames1 / 2
    mixed[:len(frames2)] += frames2 / 2

    audiolab.play(mixed[:len(mixed)*length], fs=44100)
    
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

def set_defaults(settings={}):
    UI_show = False; save = False;
    settings['busy'] = 9;     settings['inst1'] = 32
    settings['dyn'] = 7;      settings['inst2'] = 0; 
    settings['window'] = 3;   settings['inst3'] = 128
         
    settings['pattern'] = 0;    settings['style'] = 0
    settings['timeSig'] = 4;    settings['default'] = True
    settings['speed']   = 1.0;  settings['preview'] = 0.25
    return UI_show, settings, save

def fmtcols(mylist, cols):
    maxwidth = max(map(lambda x: len(x), mylist))
    justifyList = map(lambda x: x.ljust(maxwidth), mylist)
    lines = (' '.join(justifyList[i:i+cols]) for i in xrange(0,len(justifyList),cols))
    return "\n".join(lines)

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx], idx
