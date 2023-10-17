import requests, json
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36",
    "X-GUID": "01d43413c9f7a92f544ec04e5f23b60b",
    "cookie": "visitor_id=01d43413c9f7a92f544ec04e5f23b60b; visitor_id_version=2; user_ukey=34ea0b2e-cd1f-41f1-824c-6b819370d82f; theme=dark"
}
bets = {}
def main():
    response = requests.get("https://www.olimp.bet/api/v4/0/live/broadcast/sports-with-competitions-with-events", headers=headers).json()
    i = 0
    for sport in range(len(response)):
        sport_name = response[sport]["payload"]["sport"]["name"]
        if sport_name == "Теннис":
            for competition in response[sport]["payload"]["competitionsWithEvents"]:
                i +=1
                for event in competition["events"]:
                    event_name = event["names"]["0"].replace('.','')
                    bets[event_name] = {"url": "https://www.olimp.bet/live/"+str(event["sportId"])+"/"+str(event["competitionId"])+"/"+str(event['id'])}
                    if len(event["outcomes"]) > 0:
                        for outcome in event["outcomes"]:
                            if outcome["shortName"] == "П1" or outcome["shortName"] == "П2":
                                bets[event_name][outcome["shortName"]] = float(outcome["probability"])
                            else:
                                bet_type = outcome["unprocessedName"]
                                if "Тотал" in bet_type: 
                                    if "мен" in bet_type:
                                        bet_type = bet_type.replace("мен", "").replace("Тотал", "ТМ").replace(") ", ")")
                                    else:
                                        bet_type = bet_type.replace("бол", "").replace("Тотал", "ТБ").replace(") ", ")")
                                elif "с форой" in bet_type:
                                    bet_type = bet_type.replace("П1 с форой", "Ф1")
                                    bet_type = bet_type.replace("П2 с форой", "Ф2")
                                    if "Ф2" in bet_type: 
                                        if "Ф2 (+" not in bet_type and "Ф2 (-" not in bet_type:
                                            bet_type = bet_type.replace("Ф2 (", "Ф2 (+")
                                bets[event_name][bet_type] = float(outcome["probability"])
            break
    return bets