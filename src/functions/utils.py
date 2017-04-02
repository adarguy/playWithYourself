import argparse
import numpy as np
import warnings, logging

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx], idx

def process_arguments(args, UI_show):
    logging.captureWarnings(not UI_show)
    parser = argparse.ArgumentParser(description='Play With Yourself Accompaniment Tool')
    parser.add_argument('input_file',
                        action='store',
                        help='path to the input file (wav, mp3, etc)')
    args = vars(parser.parse_args(args))
    print "...Opening File: '" + args['input_file'] + "'"
    return args