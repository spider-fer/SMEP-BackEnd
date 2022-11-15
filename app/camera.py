from app import app
from flask import Flask, request,jsonify
from face_rec import FaceRec, fer
from PIL import Image
import base64
import io
import os
import shutil
import time

@app.route('/camera', methods=['POST', 'GET'])
def camera():
	data = request.get_json()
	resp = 'Nobody'
	directory = './stranger'
	if data:
		if os.path.exists(directory):
			shutil.rmtree(directory)

		if not os.path.exists(directory):
			try:
				os.mkdir(directory)
				time.sleep(1)
				result = data['data']
				b = bytes(result, 'utf-8')
				image = b[b.find(b'/9'):]
				im = Image.open(io.BytesIO(base64.b64decode(image)))
				im.save(directory+'/stranger.jpeg')

				if fer.recognize_faces() == 'fer':
					resp = 'fer'
				else:
					resp = 'Nobody'
			except:
				pass
	return resp
    
if __name__ == "__main__":
    app.run(debug=True)