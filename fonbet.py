import requests,json

events = {}
events_name_by_id = {}
bet_type = {
    921: "П1",
    923: "П2",
    1845: "Фора 1",
    1846: "Фора 2",
    1848: "ТотБ",
    1849: "ТотМ"
}
def main():
    i = 0
    bets = {}
    response = requests.get("https://line55w.bk6bba-resources.com/events/listBase?lang=ru&scopeMarket=1600").json()
    sports_id = [sport["id"] for sport in response["sports"] if "Теннис" in sport["name"]]
    for event in response["events"]:
        if event["sportId"] in sports_id:
            if "team1" in event and "team2" in event:
                events[event["team1"]+" - "+event["team2"]] = {"id": event["id"]}
                events_name_by_id[ event["id"]] = {"name": event["team1"]+" - "+event["team2"], "sportid": event["sportId"] }
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
                # if factor['f'] == 921:
                if factor['f'] in bet_type.keys():
                    events[event_name][bet_type[factor['f']]] = factor["v"]

    return events
        # for row in event["markets"][0]["rows"]:
            # print(row["cells"])
            # if row["cells"][0]['caption'] == 'Матч':
            #     print("Тип ставки: П1",'Коэффицент: ',row["cells"][1]['value'])
            #     print("Тип ставки: П2",'Коэффицент: ',row["cells"][2]['value'])
            # print(row["cells"])
        # break
# print(response)
# print(main())