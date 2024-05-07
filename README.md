# Garden Buddy

Garden Buddy is an innovative self-cultivating garden system designed to streamline and automate the challenges typically encountered in traditional plant cultivation. Serving as both an indoor, portable greenhouse and a gardening solution, the Smart Garden enables users to easily establish their own garden, regardless of their living environment

## garden-buddy-rasp-hub

This repository contains the code for the Raspberry PI attached to each Garden Buddy container. Its main functionality would be: relaying data from sensors to backend server and triggering actuations

## Setup Instructions

In order for you to be able to follow along the instruction below, you should have already set up the [Garden Buddy backend server](https://github.com/ireneliee/garden-buddy-backend) and [Garden Buddy mobile application](https://github.com/ireneliee/garden-buddy-mobile)

1. Clone this repository to your local computer
2. Create a new virtual environment for this repository and install all the required packages using
```
pip install -r requirements.txt
```
3. Run the script by using 
```
sudo python3 readSensorValue.py
```

