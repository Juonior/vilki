from flask import Flask, render_template
import time, os, threading
from datetime import datetime
from app import events_flask
from app import app
from app.routes import start_scanner
from fonbet import main as fonbet_bets
from olimp import main as olimp_bets


thread = threading.Thread(target=start_scanner)
thread.start()

if __name__ == '__main__':
    app.run(debug=True)
