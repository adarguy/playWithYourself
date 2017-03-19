import argparse

def process_arguments(args):
    parser = argparse.ArgumentParser(description='Beat tracking example')
    parser.add_argument('input_file',
                        action='store',
                        help='path to the input file (wav, mp3, etc)')
    return vars(parser.parse_args(args))