#!/bin/bash

if [ $EUID -gt 0 ]
   then echo "Please run with sudo. Exiting."
   exit
fi

echo "Exporting FLASK application..."
export FLASK_APP=hueGPIO.py

echo "Launching FLASK application..."
/usr/bin/python3 -m flask run --host=0.0.0.0 --port=5000