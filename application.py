"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014

===================

Updated 13th April 2018

+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources

Updated 26th July 2019 - Jim Martens
+ Added an extra parameter
+ Added Google Charts UI 
TODO: 
+ Buttons and send value to server.
+ Change random to heat tracking to target.
"""

# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event

__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

class GrillSimulator(Thread):
    def __init__(self):
        self.delay = 2
        super(GrillSimulator, self).__init()

    def grillSimulatorGenerator(self):
        """
        Simulate the behaviour of a grill.
        """

        while not thread_stop_event.isSet():
            number = 0
            sleep(self.delay)

    def run(self):
        self.grillSimulatorGenerator()


class RandomThread(Thread):
    def __init__(self):
        self.delay = 4
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print("Making random numbers")
        while not thread_stop_event.isSet():
            number = round(random()*100, 0)
            print(number)
            socketio.emit('newnumber', {'number': number}, namespace='/test') #?? what's the test for?
            ##TODO send second number
            sleep(self.delay)

    def run(self):
        self.randomNumberGenerator()


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

def handle_message(message):
    print('>>>>>>>> RECEIVED MESSAGE >>>>>>>> ' + message)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
