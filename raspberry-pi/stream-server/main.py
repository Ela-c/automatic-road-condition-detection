from flask import Flask, render_template, Response, request, send_from_directory, json
from camera import VideoCamera
import os
import base64
from utils import geolocateByAddress

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') # web page for debugging

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/location')
def geolocate():
	param = request.args.get('address')
	address = base64.b64decode(param)
	return json.dumps(geolocateByAddress(address))

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)
