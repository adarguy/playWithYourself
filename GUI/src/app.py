# IMPORT PYTHON LIBRARIES
import sys, os, inspect, ntpath, webbrowser


cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# IMPORT MIR LIBRARIES
sys.path.append(cwd+'/lib')
import librosa
import pymir
import midiutil


# IMPORT OUR MIR FUNCTIONS
sys.path.append(cwd+'/functions')
import utils
import dictionaries
import beatDetection
import chordPrediction
import midiConversion
import midiFileCreation

from flask import Flask, render_template, request, url_for, flash, send_from_directory, redirect
from werkzeug.utils import secure_filename


# Initialize the Flask application
UPLOAD_FOLDER = cwd+'/static/wav'
ALLOWED_EXTENSIONS = set(['wav', 'WAV'])
app = Flask(__name__, template_folder='www')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
utils.clean(UPLOAD_FOLDER+"/")
webbrowser.open_new("http://localhost:5000")

# Define a route for the default URL, which loads the form
@app.route('/')
def form():		
	return render_template('index.html', filename='Browse for file...', disabled_radio="true")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['POST'])
def upload_file():
    if request.method == 'POST':     
        file = request.files['file']
        if (allowed_file(file.filename)):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('index.html', filename=filename, disabled_radio="false", error=None)
	error = "Sorry! Must be a wav file. MP3 is coming soon though!"
	return render_template('index.html', filename='Browse for file...', disabled_radio="true", error=error)

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/'+'static/wav'+'/', methods=['POST'])
def hello():
	if request.method == 'POST':
		settings = [request.form['inst1'],		request.form['dyn'],
					request.form['inst2'],		request.form['pattern'],
					request.form['inst3'],		request.form['timeSig'],

					request.form['style'],		request.form['busy'],
					request.form['tight'],		request.form['speed'],
					request.form['filename']]
		return pwy(settings)

def pwy(settings):
	show_diagnostics = True;
	settings = utils.process_args(settings, show_diagnostics)


	# OPEN FILE
	settings['filename'] = UPLOAD_FOLDER+'/'+settings['filename']
	UI_instrument_notes = settings['inst1']; 	UI_onset_threshold = settings['busy'];
	UI_instrument_chords = settings['inst2']; 	UI_dynamic_threshold = settings['dyn'];
	UI_instrument_beats = settings['inst3']; 	UI_beat_windowSize = settings['window']; #300 msec
	UI_beat_pattern = settings['pattern'];		UI_chord_style = settings['style'];
	UI_time_signature = settings['timeSig'];	y, sr = librosa.load(settings['filename'])


	# TRACK BEATS
	onsets, beats, volume_notes, times, tempo, msec_tempo = beatDetection.track_beats(y, sr, UI_onset_threshold, UI_dynamic_threshold, UI_beat_windowSize)
	#beatDetection.plot_beats_and_onsets(onsets, beats, times, show_diagnostics) //Breaks GUI


	# PREDICT CHORDS
	notes, reg_notes, startTimes_notes, endTimes_notes, frameIndex_notes = chordPrediction.get_chords(settings['filename'], times[beats], times)
	chords, reg_chords, startTimes_chords, endTimes_chords, frameIndex_chords, volume_chords = midiConversion.determine_durations(list(notes), list(reg_notes), list(startTimes_notes), list(endTimes_notes), frameIndex_notes, list(volume_notes))
	chordPrediction.print_chords_and_times(chords, startTimes_chords, endTimes_chords, frameIndex_chords, times, show_diagnostics)
	startTimes_beats, endTimes_beats, volume_beats = beatDetection.alter_beats(startTimes_notes, endTimes_notes, volume_notes, msec_tempo, UI_beat_windowSize, settings['speed'])


	# NOTES TO MIDI
	midi_notes = midiConversion.convert_note_to_midi(notes, reg_notes)
	midi_chords = midiConversion.convert_chord_to_midi(chords, reg_chords, UI_chord_style)
	midi_beats = midiConversion.convert_beat_to_midi(notes, UI_beat_pattern, UI_time_signature, UI_instrument_beats, reg_notes, settings['speed'])


	# WRITE MIDI
	midi_tracks = [midi_notes, midi_chords, midi_beats]
	startTimes = [startTimes_notes, startTimes_chords, startTimes_beats]
	endTimes = [endTimes_notes, endTimes_chords, endTimes_beats]
	UI_instrument = [UI_instrument_notes, UI_instrument_chords, UI_instrument_beats]
	volumes = [volume_notes, volume_chords, volume_beats]
	duration = [0]*len(midi_tracks); program = [0]*len(midi_tracks); volume = [0]*len(midi_tracks);
	for i in range(len(midi_tracks)):
		duration[i], program[i], volume[i] = midiFileCreation.build_track(UI_instrument[i], midi_tracks[i], startTimes[i], endTimes[i], volumes[i], msec_tempo, UI_dynamic_threshold)
	midiFileCreation.write_midi_file(settings['filename'], midi_tracks, program, duration, tempo[0], volume)
	utils.preview(ntpath.basename(settings['filename']), UPLOAD_FOLDER)

	return render_template('download.html', filename=ntpath.basename(settings['filename'][:-4]), path=UPLOAD_FOLDER)

# Run the app :)
if __name__ == '__main__':
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.debug = False
	app.run()
