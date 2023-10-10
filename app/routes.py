from flask import request, jsonify, render_template
from app import events_flask
import threading,time
from fuzzywuzzy import fuzz
from datetime import datetime
from fonbet import main as fonbet_bets
from olimp import main as olimp_bets
overlapping_bids = [
    ["П1", "П2"],
    ["Фора 1", "Фора 2"],
    ["ТотМ", "ТотБ"]
]


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
                if overlapping_bid[0] in o[event2].keys() and overlapping_bid[0] in f[event].keys():
                    o1, o2, f1, f2 = o[event2][overlapping_bid[0]], o[event2][overlapping_bid[1]], f[event][overlapping_bid[0]], f[event][overlapping_bid[1]]
                    if o1 != 0 and o2 != 0 and f1 != 0 and f2 != 0:
                        k1 = (1 / o1) + (1 / f2)
                        k2 = (1 / f1) + (1 / o2)
                        if k1 < k2:
                            percent = round((1 - k1) * 100, 2)
                            if 10 > percent > 0:
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
                                    'profit': percent
                                }
                                events_flask.append(event_flask)
                        else:
                            percent = round((1 - k2) * 100, 2)
                            if 10 > percent > 0:
                                event_flask = {
                                    'site1': "Fonbet",
                                    'type1': overlapping_bid[0],
                                    'link1': f[event]["url"],
                                    'coefficient1': f1,
                                    'matchName1': event,
                                    'site2': "Olimp",
                                    'type2': overlapping_bid[1],
                                    'link2': o[event2]["url"],
                                    'coefficient2': o2,
                                    'matchName2': event2,
                                    'profit': percent
                                }
                                events_flask.append(event_flask)
        time.sleep(cooldown)
