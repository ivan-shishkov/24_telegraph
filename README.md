# Telegraph Clone

This service is intended to create posts and give a unique URL's to them. 
The author also has the ability to edit the post created by him. 
All created posts is saved to the SQLite database.
Online version of service is available [here](https://simplyuser.pythonanywhere.com/).

# Quickstart

For service launch on localhost need to install Python 3.5 and then install all dependencies:

```bash

$ pip install -r requirements.txt

```

To create database need to execute:

```bash

$ python3 db.py

```

Usage:

```bash
$ export SECRET_KEY='your_secret_key'
$ python3 server.py

```

Then open page [localhost:5000](http://localhost:5000) in browser.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
