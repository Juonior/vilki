import requests,json

events = {}
events_name_by_id = {}
bet_types = {
    910: "Ф1",
    912: "Ф2",
    921: "П1",
    923: "П2",
    1696: "ТБ",
    1697: "ТМ",
    1727: "ТБ",
    1728: "ТМ",
    1845: "Ф1",
    1846: "Ф2",
    1848: "ТБ",
    1849: "ТМ",

}
def main():
    i = 0
    bets = {}
    response = requests.get("https://line55w.bk6bba-resources.com/events/listBase?lang=ru&scopeMarket=1600").json()
    
    sports_id = [sport["id"] for sport in response["sports"] if "Теннис" in sport["name"]]
    for event in response["events"]:
        if event["sportId"] in sports_id:
            if "team1" in event and "team2" in event:
                events[event["team1"]+" - "+event["team2"]] = {"id": event["id"], "childs": []}
                events_name_by_id[ event["id"]] = {"name": event["team1"]+" - "+event["team2"], "sportid": event["sportId"], "bets_type": "Основные" }
            if "parentId" in event:
                events[events_name_by_id[event["parentId"]]["name"]]["childs"].append({"id": event["id"], "name": event["name"]})
                #events_name_by_id[event["id"]] =  {"name": events_name_by_id[event["parentId"]] , "sportid": event["sportId"], "bets_type": event["name"] }
            # print(event)
    # print(events)
    outcomes_response = requests.get("https://line06w.bk6bba-resources.com/events/list?lang=ru&version=21257564342&scopeMarket=1600").json()
    for event in outcomes_response["customFactors"]:
        if event["e"] in events_name_by_id.keys():
            event_name = events_name_by_id[event["e"]]["name"]
            sport_id = events_name_by_id[event["e"]]["sportid"]
            event_id = event["e"]
            events[event_name]["url"] = f"https://www.fon.bet/live/tennis/{sport_id}/{event_id}/"
            for factor in event["factors"]:
                if factor['f'] in bet_types.keys():
                    if factor["f"] == 921 or factor["f"] == 923:
                        events[event_name][bet_types[factor['f']]] = factor["v"]
                    else:
                        events[event_name][bet_types[factor['f']] + " ("+factor["pt"]+")"] = factor["v"]
            for child in events[event_name]["childs"]:
                for event in outcomes_response["customFactors"]:
                    if event["e"] == child["id"]:
                        for factor in event["factors"]:
                            if factor['f'] in bet_types.keys():
                                if factor["f"] == 921 or factor["f"] == 923:
                                    events[event_name][bet_types[factor['f']]+ " ("+child["name"]+")"] = factor["v"]
                                else:
                                    events[event_name][bet_types[factor['f']] + " ("+factor["pt"]+") ("+child["name"]+")"] = factor["v"]
            # if event_name == "Монтейро Т - Серундоло Х-М":
            #     print(events[event_name])
    return events