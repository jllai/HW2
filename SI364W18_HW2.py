## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file.

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################

from flask import Flask, request, render_template, flash, redirect, url_for
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
import requests
import json

#####################
##### APP SETUP #####
#####################

# >>>>>>> a6eb0a1... Add structure and import stmts necessary
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

@app.route('/artistform')
def artist_form():
	return render_template('artistform.html')

@app.route('/artistlinks')
def artist_links():
	return render_template('artist_links.html')



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistinfo', methods = ['GET', 'POST'])
def artist_info():
	if request.method == 'GET':
		artist = request.args.get('artist')
		inp = 'https://itunes.apple.com/search?term=' + artist
		results = requests.get(inp)
		json_file = json.loads(results.text)
		print(json_file)
		return render_template('artist_info.html', objects = json_file)

@app.route('/specific/song/<artist_name>', methods = ['GET', 'POST'])
def specific_artist(artist_name):
	if request.method == 'GET':
		inp = 'https://itunes.apple.com/search?term=' + artist_name
		results = requests.get(inp)
		json_file = json.loads(results.text)
		# return('hi')
		return render_template('specific_artist.html', results = json_file['results'])



class AlbumEntryForm(FlaskForm):
	album = StringField('Enter the name of an album: ' , validators=[Required()])
	rating = RadioField('How much do you like this album? (1 low, 3 high)' , choices=[("1", '1'), ("2", '2'), ("3", '3')] , validators=[Required()])
	submit = SubmitField('Submit')

@app.route('/album_entry')
def album_entry():
	form = AlbumEntryForm()
	return render_template('album_entry.html' , form=form)

@app.route('/album_result' , methods = ['GET' , 'POST'])
def album_result():
	form = AlbumEntryForm()
	if form.validate_on_submit():
		album = form.album.data
		rating = form.rating.data
		return render_template('album_data.html', album = album, rating = rating)
	flash(form.errors)
	return redirect(url_for('album_entry'))

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
