#!/bin/bash

if [ $EUID > 0 ]
   then echo "Please run with sudo. Exiting."
   exit
fi

echo "Updating system and installing required software..."
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
echo "   done."

echo "Installing required modules..."
sudo pip3 install flask
echo "   done."

echo "Exporting FLASK application
export FLASK_APP=hueGPIO.py

echo "Setting up neocal service..."
sudo cp hueGPIO.service /etc/systemd/system/hueGPIO.service
sudo systemctl enable hueGPIO.service
echo "   done."

echo "Starting hueGPIO..."
sudo systemctl start hueGPIO.service
echo "   installation complete."
