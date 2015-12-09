#!/bin/env python
from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app,'http://safe-refuge-1607.herokuapp.com')
    #socketio.run(app)
