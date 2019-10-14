#!/usr/bin/env python
from importlib import import_module
import os
import time
from flask import Flask, render_template, Response
import zmq
import sys
import time

class ZMQFrameReceiver:
    def __init__(self, endpoint="tcp://127.0.0.1:5600"):        
        self.endpoint = endpoint
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.SUB)
        self.sock.setsockopt(zmq.SUBSCRIBE, b"")
        self.sock.connect(self.endpoint)

    def frames(self):        
        while True:          
            frame = self.sock.recv()
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')        

# Globals

app = Flask(__name__)
videosource = ZMQFrameReceiver()

@app.route('/video_feed')
def video_feed():
    global videosource
    return Response( 
            videosource.frames(), 
            mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
