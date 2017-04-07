import argparse, warnings, logging, subprocess, os
import scikits.audiolab as audiolab
import numpy as np

def get_arguments(args):
    config = raw_input('Would you like to use default settings or configure manually? --default/manual\n')  
    settings = [0]*7
    if (config == 'manual'):
        settings[0] = raw_input('-Busyness --Onset (beat) threshold\n')
        settings[1] = raw_input('-Dynamics --Dynamics threshold\n')
        settings[2] = raw_input('-Window --Beat Correction Window Size\n')
        settings[3] = raw_input('-Instrument1 --Instrument for Melodic Accompaniment\n')
        settings[4] = raw_input('-Instrument2 --Instrument for Harmonic Accompaniment\n')
        settings[5] = raw_input('-Instrument3 --Instrument for Percussive Accompaniment\n')
        settings[6] = raw_input('-Pattern --Pattern for Percussive Accompaniment\n')
    else:
        settings[0] = '0.1';    settings[4] = '0';
        settings[1] = '0.7';    settings[5] = '35'; 
        settings[2] = '0.3';    settings[6] = '0';
        settings[3] = '0';
    return args+settings

def process_arguments(args, UI_show):
    logging.captureWarnings(not UI_show)
    args = get_arguments(args)

    parser = argparse.ArgumentParser(description='An accompaniment tool for the modern musician')
    parser.add_argument('Filename', action='store', help='--Path to the input wav file')
    parser.add_argument('Busyness', action='store', help='--Onset (beat) threshold')
    parser.add_argument('Dynamics', action='store', help='--Dynamics threshold')
    parser.add_argument('Window', action='store', help='--Beat Correction Window Size')
    parser.add_argument('Instrument1', action='store', help='--Instrument for Melodic Accompaniment')
    parser.add_argument('Instrument2', action='store', help='--Instrument for Harmonic Accompaniment')
    parser.add_argument('Instrument3', action='store', help='--Instrument for Percussive Accompaniment')
    parser.add_argument('Pattern', action='store', help='--Pattern for Percussive Accompaniment')
    args = vars(parser.parse_args(args))
    
    print "...Opening File: '" + args['Filename'] + "'"
    return args

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