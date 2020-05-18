from flask import Flask, redirect, render_template, request
import io
import os
import base64
import re
import json
from flask_cors import CORS

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

app = Flask(__name__)
CORS(app)

@app.route('/UploadPhoto', methods=['GET', 'POST'])
def UploadPhoto():
	image_b64 = request.values['imageBase64']
	image_data = base64.b64decode(re.sub('^data:image/.+;base64,', '', image_b64))
	return json.dumps({'emotion':getEmotionLabel(image_data)})



def getEmotionLabel(image_data):
	# Instantiates a client
	client = vision.ImageAnnotatorClient()
	
	# Loads the image into memory
	image = types.Image(content=image_data)

	# facial detection
	response = client.face_detection(image=image)
	faceNotes = response.face_annotations

   	for note in faceNotes:
		emotions = [note.joy_likelihood, note.sorrow_likelihood, note.anger_likelihood, note.surprise_likelihood]
		dominantEmotion = emotions.index(max(emotions))
		if(dominantEmotion==0):
			dominantEmotion = "happy"

		if(dominantEmotion==1):
			dominantEmotion = "sad"

		if(dominantEmotion == 2):
			dominantEmotion = "angry"

		if(dominantEmotion == 3):
			dominantEmotion = "surprised"

  	return [dominantEmotion]

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
