# Automatic Road Condition Survey

## Project Overview

The Automatic Road Condition Survey project aims to automate the road inspection process for municipal councils, enhancing efficiency and reducing maintenance costs. The system employs a combination of Raspberry Pi, Arduino, and computer vision techniques to detect road conditions in real time.

## Demonstration Video

[![Watch the demonstration video](https://img.youtube.com/vi/fx3eOhopYiI/0.jpg)](https://youtu.be/fx3eOhopYiI)


## Background

Municipal councils manage extensive road networks, often exceeding 500 kilometres, requiring substantial effort and funding for maintenance. Traditional inspection methods are manual and costly, relying on external consultants and specialized equipment. This project proposes an automated solution to streamline the inspection process using affordable and accessible technology.

## Problem Statement

Current road condition inspection methods are manual and expensive, leading to inefficiencies and delayed maintenance. By automating the inspection process with a real-time system, councils can optimize their maintenance efforts and reduce costs.

## Requirements

- 1 Raspberry Pi 3
- 1 Raspberry Pi Camera Model 2
- 1 Arduino Nano 33 IoT
- 1 Light Sensor (BH1750)
- 1 Buzzer Module
- 1 Computer Server
- 1 Database
- Internet connection (WiFi)
- Jumper Wires

## Design Principles

- **Cost**: Ensure components are cheap to acquire and test.
- **Robustness**: Sanitize and test human input thoroughly.
- **Communication**: Ensure smooth and fast communication between Raspberry Pi, server, and Arduino.
- **Fault Tolerance**: Handle errors gracefully, including power or internet failures.
- **Performance**: Optimize code and processes for real-time performance.

### Communication

- HTTP communication between the server and Raspberry Pi for image capture.
- Asynchronous serial communication over USB between Raspberry Pi and Arduino.
- HTTP webhooks for status notifications to system admins.

## Setup Instructions

### Raspberry Pi

1. Connect the Raspberry Pi camera.
2. Enable the legacy camera interface in the Raspberry Pi configuration.
3. Download the code from the `raspberry-pi` folder.
4. Connect the Raspberry Pi to the internet.
5. Install all Python dependencies by running `pip install -r requirements.txt`.

### Arduino Nano 33 IoT

1. Connect the Light Sensor and Buzzer to the Arduino as labelled.
2. Download the code from the `monitor` folder.
3. Set up an IFTTT account and create a webhook service for email notifications.
4. Provide WiFi credentials and the webhook URL in the `.ino` file.
5. Install all Arduino libraries.

### Server

1. Download the code from the `ai-model` folder.
2. Ensure the server is on the same network as the Raspberry Pi.
3. Create a new SQLite3 database with the command `sqlite3 database.db`.
4. Install all Python dependencies by running `pip install -r requirements.txt`.

## Usage Instructions

1. Power on the Raspberry Pi.
2. Log in to the Raspberry Pi and run the `run.sh` script located in the `raspberry-pi` folder.
3. On the server, run the `detect.py` and `server.py` scripts in separate terminals.
4. The system will now be able to identify potholes and allow data queries via the API.
