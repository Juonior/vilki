from flask import request, jsonify, render_template
from app import UpdateEvents
from app import app
from app import events_flask
import threading, time
from fuzzywuzzy import fuzz
from datetime import datetime
from fonbet import main as fonbet_bets
from olimp import main as olimp_bets
overlapping_bids = [
    ["П1", "П2"],
    ["Ф1 (-6.5)", "Ф2 (+6.5)"],
    ["Ф1 (-5.5)", "Ф2 (+5.5)"],
    ["Ф1 (-4.5)", "Ф2 (+4.5)"],
    ["Ф1 (-3.5)", "Ф2 (+3.5)"],
    ["Ф1 (-2.5)", "Ф2 (+2.5)"],
    ["Ф1 (-1.5)", "Ф2 (+1.5)"],
    ["Ф1 (-0.5)", "Ф2 (+0.5)"],
    ["ТБ (19.5)", "ТМ (19.5)"],
    ["ТБ (20.5)", "ТМ (20.5)"],
    ["ТБ (21.5)", "ТМ (21.5)"],
    ["ТБ (22.5)", "ТМ (22.5)"],
    ["ТБ (23.5)", "ТМ (23.5)"],
    ["ТБ (24.5)", "ТМ (24.5)"],
    ["ТБ (25.5)", "ТМ (25.5)"],
    ["ТБ (26.5)", "ТМ (26.5)"],
    ["ТБ (27.5)", "ТМ (27.5)"],
    ["ТБ (28.5)", "ТМ (28.5)"],
    ["ТБ (29.5)", "ТМ (29.5)"],
    ["ТБ (30.5)", "ТМ (30.5)"],
    ["ТБ (31.5)", "ТМ (31.5)"]
]


# Define a dictionary to store the first appearance time for each event
first_appearance_times = {}

def find_similar_strings(dict1, dict2, threshold):
    similar_pairs = []

    for str1 in dict1:
        for str2 in dict2:
            similarity = fuzz.ratio(str1, str2)
            if similarity >= threshold:
                similar_pairs.append((str1, str2))

    return similar_pairs

cooldown = 0

def start_scanner():
    cooldown = 0
    print("[STATUS] Scanner started.")
    while True:
        o = olimp_bets()
        f = fonbet_bets()
        events_flask.clear()
        similar_strings = find_similar_strings(o, f, 70)
        for event2, event in similar_strings:
            for overlapping_bid in overlapping_bids:
                if overlapping_bid[0] in o[event2].keys() and overlapping_bid[0] in f[event].keys() and overlapping_bid[1] in o[event2].keys() and overlapping_bid[1] in f[event].keys():
                    # print(event,overlapping_bid)
                    o1, o2, f1, f2 = o[event2][overlapping_bid[0]], o[event2][overlapping_bid[1]], f[event][overlapping_bid[0]], f[event][overlapping_bid[1]]
                    if o1 != 0 and o2 != 0 and f1 != 0 and f2 != 0:
                        k1 = (1 / o1) + (1 / f2)
                        k2 = (1 / f1) + (1 / o2)
                        if k1 < k2:
                            percent = round((1 - k1) * 100, 2)
                            if 10 > percent > 0:
                                if not "".join([event,str(k1),str(k2)]) in first_appearance_times:
                                    first_appearance_times[ "".join([event,str(k1),str(k2)])] = datetime.now()
                                event_flask = {
                                    'site1': "Fonbet",
                                    'type1': overlapping_bid[1],
                                    'link1': f[event]["url"],
                                    'coefficient1': f2,
                                    'matchName1': event,
                                    'site2': "Olimp",
                                    'type2': overlapping_bid[0],
                                    'link2': o[event2]["url"],
                                    'coefficient2': o1,
                                    'matchName2': event2,
                                    'profit': percent,
                                    'time': first_appearance_times[ "".join([event,str(k1),str(k2)])].isoformat()
                                }
                                events_flask.append(event_flask)
                                
                        else:
                            percent = round((1 - k2) * 100, 2)
                            if 10 > percent > 0:
                                if not "".join([event,str(k1),str(k2)]) in first_appearance_times:
                                    first_appearance_times[ "".join([event,str(k1),str(k2)])] = datetime.now()
                                event_flask = {
                                    'site1': "Fonbet",
                                    'type1': overlapping_bid[1],
                                    'link1': f[event]["url"],
                                    'coefficient1': f2,
                                    'matchName1': event,
                                    'site2': "Olimp",
                                    'type2': overlapping_bid[0],
                                    'link2': o[event2]["url"],
                                    'coefficient2': o1,
                                    'matchName2': event2,
                                    'profit': percent,
                                    'time': first_appearance_times[ "".join([event,str(k1),str(k2)])].isoformat()
                                }
                                events_flask.append(event_flask)
        with app.app_context():
            UpdateEvents(events_flask)
        time.sleep(cooldown)
