import logging, subprocess, os, shutil
import numpy as np
from scipy.io.wavfile import read, write
import wave, pyaudio, librosa

import dictionaries





init = True

def help():
    print ("\nWelcome to Play With Yourself!\n" #App Description
    "A music accompaniment tool for the modern musician\n\n"
    "Play With Yourself is an accompaniment tool that allows users to\n"
    "create automatic accompaniments to their working songs and projects.\n"
    "This has been developed in part for a university class on music\n"
    "information retrieval hosted at the University of Victoria, BC Canada.\n"
    "Contact the administrator with any inquiries at adarguy10@gmail.com\n")
    

    print ("\nValid user settings (after load) are:\n" #Parameter Description

    "General Settings Options:\n"   
    "  -YESInstrument 1- <name>        -- instrument for melodic accompaniment (type options for a list of instruments)\n"
    "  -YESInstrument 2- <name>        -- instrument for harmonic accompaniment (type options for a list of instruments)\n"
    "  -YESInstrument 3- <name>        -- instrument for percussive accompaniment (type options for a list of instruments)\n"
    "  -YESPercussion Style- <genre>   -- pattern by genre for percussive accompaniment (type options for a list of genres)\n"
    "  -YESTime Signature- <num>       -- time signature for accompaniment (3/4 or 4/4 only)\n"
    
    "Advanced Settings Options:\n"
    "  -YESBusyness- <num>             -- onset (beat) detection threshold (1-10)\n"
    "  -YESDynamics- <num>             -- dynamics threshold (1-10)\n"
    "  -YESWindow- <num>               -- beat correction window by number (1-10)\n"
    "  -YESChord Style- <style>        -- chord style for harmonic accompaniment (closed or open)\n" 
    "  -YESTempo- <size>               -- speed of accompaniment (half, regular, double, quadruple)\n")

def process_args(settings, UI_show):
    logging.captureWarnings(not UI_show)
    dic = { 'inst1':int(dictionaries.instToPrgNum(settings[0])),    'dyn':float(int(settings[1])/10.0),
            'inst2':int(dictionaries.instToPrgNum(settings[2])),    'pattern':int(dictionaries.genreToPrgNum(settings[3])),
            'inst3':int(dictionaries.instToPrgNum(settings[4])),    'timeSig':int(settings[5].split('/')[0]),
 
            'style':int(dictionaries.styleToPrgNum(settings[6])),   'busy':float((10-int(settings[7]))/10.0),
            'window':float(int(settings[8])/10.0),                  'speed':int(dictionaries.speedToPrgNum(settings[9])),
            'filename':str(settings[10])
    }
    return dic

def preview(filename, directory):
    print '...Previewing Accompaniment'
    FNULL = open(os.devnull, 'w')
    subprocess.call(['fluidsynth', '-T', 'wav', '-F', directory+"/"+filename[:-4]+'.raw', '-ni', directory[:-10]+'lib/sf2/sf.sf2', directory+"/"+filename[:-4]+'.mid', '-g', '0.8', '-r', '22050'], stdout=FNULL, stderr=subprocess.STDOUT)
    subprocess.call(['SoX', '-t', 'raw', '-r', '22050','-e', 'signed', '-b', '16', '-c', '1', directory+"/"+filename[:-4]+'.raw', directory+"/"+filename[:-4]+'_midi.wav'])
    
    y, sr = librosa.load(directory+"/"+filename)
    z, sr2 = librosa.load(directory+"/"+filename[:-4]+'_midi.wav')
    y = librosa.resample(y,sr,sr*2)
    mix = np.zeros(max(len(y), len(z)), dtype=float)
    mix[:len(y)] += y / 2
    mix[:len(z)] += z / 2
    mix = np.int16(mix/np.max(np.abs(mix)) * 16383)
    write(directory+"/"+filename[:-4]+'_mix.wav', 44100, mix)

def clean(directory):
    global init
    if (init):
        shutil.rmtree(directory)
        os.mkdir(directory)
        init = False
        print '...Clearing Directory'

def set_defaults(settings={}):
    UI_show = False; save = False;
    settings['busy'] = 0.1;     settings['inst1'] = 32
    settings['dyn'] = 0.7;      settings['inst2'] = 0; 
    settings['window'] = 0.3;   settings['inst3'] = 128
         
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
