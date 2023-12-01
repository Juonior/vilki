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
    927: "Ф1",
    928: "Ф2",
    989: "Ф1",
    991: "Ф2",
    1569: "Ф1",
    1572: "Ф2",
    1672: "Ф1",
    1675: "Ф2",
    1677: "Ф1",
    1678: "Ф2",
    1680: "Ф1",
    1681: "Ф2",
    1683: "Ф1",
    1684: "Ф2",
    1686: "Ф1",
    1687: "Ф2",
    1845: "Ф1",
    1846: "Ф2",



    921: "П1",
    922: "Ничья",
    923: "П2",
    924: "П1 или Ничья",
    925: "П2 или Ничья",

    930: "ТБ",
    931: "ТМ",
    1696: "ТБ",
    1697: "ТМ",
    1727: "ТБ",
    1728: "ТМ",
    1730: "ТБ",
    1731: "ТМ",
    1739: "ТБ",
    1791: "ТМ",
    1793: "ТБ",
    1794: "ТМ",
    1796: "ТБ",
    1797: "ТМ",
    1733: "ТБ",
    1734: "ТМ",
    1736: "ТБ",
    1737: "ТМ",
    1848: "ТБ",
    1849: "ТМ",
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
                    events[event["team1"]+" - "+event["team2"]] = {"id": event["id"], "childs": [],"type": "basketball"}
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
            events[event_name]["url"] = f"https://www.fon.bet/live/basketball/{sport_id}/{event_id}/"
            # print(event_name, events[event_name]["url"])
            for factor in event["factors"]:
                if factor['f'] in bet_types.keys() and "pt" in factor.keys():
                    if 921 >= factor["f"] <= 925:
                        events[event_name][bet_types[factor['f']]] = factor["v"]
                    else:
                        events[event_name][bet_types[factor['f']] + " ("+factor["pt"]+")"] = factor["v"]
            # for factor in event["factors"]:
            #     if not factor['f'] in bet_types.keys():
            #         print(factor)
            # if event_name == "Нью-Тайпей Кингс - Мералко Болтс":
            #     return
        elif event["e"] in childs_event_by_id.keys():
            event_name =  events_name_by_id[childs_event_by_id[event["e"]]["parent"]]["name"]
            child_name = childs_event_by_id[event["e"]]["name"]
            for factor in event["factors"]:
                if factor['f'] in bet_types.keys():
                    if 921 <= factor["f"] <= 925:
                        events[event_name][f"({child_name}) "+bet_types[factor['f']]] = factor["v"]
                    else:
                        events[event_name][f"({child_name}) "+bet_types[factor['f']] + " ("+factor["pt"]+")"] = factor["v"]

            
    # return events
# main("192.168.2.211") 
main("10.192.219.161")
print(events)