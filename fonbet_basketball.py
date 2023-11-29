import requests,json
from urllib3.exceptions import InsecureRequestWarning
from app import session_for_src_addr
import warnings, time

# Отключите предупреждение InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
from app import session_for_src_addr
events = {}
bets = {}
events_name_by_id = {}
childs_event_by_id = {}
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
    1747: "Гейм",
    1748: "Гейм",
    1750: "Гейм",
    1751: "Гейм",
    1753: "Гейм",
    1754: "Гейм",
    9961: "Гейм",
    9962: "Гейм"

}
def main(localIP):
    global events
    i = 0
    bets = {}
    session = session_for_src_addr(localIP)
    response = session.get("https://line55w.bk6bba-resources.com/events/listBase?lang=ru&scopeMarket=1600", verify=False).json()
    session.close()
    sports_id = [sport["id"] for sport in response["sports"] if ("баскетбол" in sport["name"].lower() or "basketball" in sport["name"].lower())]

    for event in response["events"]:
        if event["sportId"] in sports_id:
            if int(time.time()) >= event["startTime"]:
                if "team1" in event and "team2" in event:
                    events[event["team1"]+" - "+event["team2"]] = {"id": event["id"], "childs": [],"type": "tennis"}
                    events_name_by_id[ event["id"]] = {"name": event["team1"]+" - "+event["team2"], "sportid": event["sportId"], "bets_type": "Основные" }
                if "parentId" in event:
                    if event["parentId"] in events_name_by_id.keys():
                        childs_event_by_id[event["id"]] = {"parent": event["parentId"], "name": event["name"],"type": "tennis"}
    session = session_for_src_addr(localIP)
    outcomes_response = session.get("https://line06w.bk6bba-resources.com/events/list?lang=ru&version=21257564342&scopeMarket=1600",verify=False).json()
    session.close()
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
            print(events[event_name])
            return
        # elif event["e"] in childs_event_by_id.keys():
        #     event_name =  events_name_by_id[childs_event_by_id[event["e"]]["parent"]]["name"]
        #     # print(event_name)
        #     child_name = childs_event_by_id[event["e"]]["name"]
        #     set = ""
        #     if "сет" in child_name:
        #         set = f"({child_name})"
        #     # if event_name == "Томич Б - Мицуи Ш":
        #         # print(event["factors"],child_name)
        #     child_name = childs_event_by_id[event["e"]]["name"]
        #     if not "/" in event_name:
        #         for factor in event["factors"]:
        #             if factor['f'] in bet_types.keys():
        #                 if factor["f"] == 921 or factor["f"] == 923:
        #                     events[event_name][bet_types[factor['f']]+ " ("+child_name+")"] = factor["v"]
        #                 elif factor["f"] == 1747 or factor["f"] == 1750 or factor["f"] == 1753 or factor["f"] == 9961:
        #                     events[event_name]["П1 (Гейм "+factor["pt"]+") "+set] = factor["v"]
        #                 elif factor["f"] == 1748 or factor["f"] == 1751 or factor["f"] == 1754 or factor["f"] == 9962:
        #                     events[event_name]["П2 (Гейм "+factor["pt"]+") "+set] = factor["v"]
        #                 else:
        #                     events[event_name][bet_types[factor['f']] + " ("+factor["pt"]+") ("+child_name+")"] = factor["v"]
        
    # return events
main("192.168.2.211")