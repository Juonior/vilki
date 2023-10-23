import requests, json, threading, time
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36",
    "X-GUID": "01d43413c9f7a92f544ec04e5f23b60b",
    "cookie": "visitor_id=01d43413c9f7a92f544ec04e5f23b60b; visitor_id_version=2; user_ukey=34ea0b2e-cd1f-41f1-824c-6b819370d82f; theme=dark"
}
bets = {}
proxies = [
    "http://gR8bNG1g:jknP4TJU@194.156.122.187:64290",
    "http://gR8bNG1g:jknP4TJU@45.152.226.38:61950",
    "http://gR8bNG1g:jknP4TJU@194.61.77.242:64644",
    "http://gR8bNG1g:jknP4TJU@195.19.168.209:62036",
    "http://gR8bNG1g:jknP4TJU@109.94.211.231:61930"
]
groupNames = [
    "Основные",
    "Ставки по сетам",
    "Доп.тотал",
    "Победа с учетом форы",
]
i = 1
def get_info(event_id):
    global i, bets
    response = requests.get("https://www.olimp.bet/api/v4/0/live/events?vids[]="+str(event_id)+":&main=false", headers=headers,proxies={"https": proxies[i]}).json()
    i = (i + 1) % len(proxies)
    if len(response) > 0:
        event = response[0]["payload"]
        event_name = event["names"]["0"].replace('.','')
        bets[event_name] = {"url": "https://www.olimp.bet/live/"+str(event["sportId"])+"/"+str(event["competitionId"])+"/"+str(event['id'])}
        if len(event["outcomes"]) > 0:
            for outcome in event["outcomes"]:
                if outcome["shortName"] == "П1" or outcome["shortName"] == "П2":
                    bets[event_name][outcome["shortName"]] = float(outcome["probability"])
                else:
                    bet_type = outcome["unprocessedName"]
                    if outcome["groupName"] in groupNames:
                        if outcome["groupName"] == "Основные":
                            if "Тотал" in bet_type: 
                                if "мен" in bet_type:
                                    bet_type = bet_type.replace("мен", "").replace("Тотал", "ТМ").replace(") ", ")")
                                else:
                                    bet_type = bet_type.replace("бол", "").replace("Тотал", "ТБ").replace(") ", ")")
                            elif "с форой" in bet_type:
                                bet_type = bet_type.replace("П1 с форой", "Ф1")
                                bet_type = bet_type.replace("П2 с форой", "Ф2")
                                if not "(-" in bet_type:
                                    bet_type = bet_type.replace("(","(+")
                                # if "Ф2" in bet_type: 
                                #     if "Ф2 (+" not in bet_type and "Ф2 (-" not in bet_type:
                                #         bet_type = bet_type.replace("Ф2 (", "Ф2 (+")
                        elif outcome["groupName"] == "Ставки по сетам":
                            if "П" in bet_type and "в " in bet_type and "-м сете" in bet_type:
                                winner, set = bet_type.split(" ")[0], bet_type.split(" ")[2][0]
                                bet_type = winner+ " "+  f"({set}-й сет)"
                            elif "в" in bet_type and "-м c. с форой" in bet_type:
                                winner,vo, set, summ = bet_type.split(" ")[0],bet_type.split(" ")[1], bet_type.split(" ")[2][0],  bet_type.split(" ")[-1]
                                if not "-" in summ:
                                    summ = "(+" + summ[1:-1] + ")"
                                bet_type =  f"Ф{winner[1]} {summ} ({set}-й сет)"
                            elif "Тотал в" in bet_type and "-м сете " in bet_type:
                                set, score, sign =  bet_type.split(" ")[2][0], bet_type.split(" ")[4], bet_type.split(" ")[5]
                                bet_type = ("ТБ" if sign == "бол"  else "ТМ") + " " + score + " "+ f"({set}-й сет)"
                        elif outcome["groupName"] == "Доп.тотал":
                            score, sign = bet_type.split(" ")[1], bet_type.split(" ")[2]
                            bet_type = ("ТБ" if sign == "бол"  else "ТМ") + " " + score
                        elif outcome["groupName"] == "Победа с учетом форы":
                            p1,p2 = event["names"]["0"].split("-")[0][:-1],event["names"]["0"].split("-")[1][1:]
                            bet_type = bet_type.replace(p1,'Ф1').replace(p2,"Ф2")
                            if not "(-" in bet_type:
                                bet_type = bet_type.replace("(","(+")
                        bets[event_name][bet_type] = float(outcome["probability"])
                    elif "гейм" in outcome["groupName"]:
                        p1,p2 = event["names"]["0"].split("-")[0][:-1],event["names"]["0"].split("-")[1][1:]
                        set = ""
                        if "сет" in outcome["groupName"]:
                            set =  "("+outcome["groupName"].split(" ")[0][:-1]+"-й сет)"
                        if bet_type == p1 or bet_type == p2:
                            game = outcome["groupName"].split(" ")[2][:-1]
                            bet_type = bet_type.replace(p1,'П1').replace(p2,"П2")
                            bet_type = f"{bet_type} (Гейм {game}) "+set
                            bets[event_name][bet_type] = float(outcome["probability"])
        # if event_name == "Лис Е - Кристиан Ж-А":
            # print(bets[event_name])
        # if "Томич" in event_name:
            # print(bets[event_name])
def main(proxy):
    global bets
    response = requests.get("https://www.olimp.bet/api/v4/0/live/sports-with-competitions-with-events?vids[]=3:", headers=headers,proxies={"https":proxy}).json()
    i = 0
    threads = []
    for sport in range(len(response)):
        sport_name = response[sport]["payload"]["sport"]["name"]
        if sport_name == "Теннис":
            for competition in response[sport]["payload"]["competitionsWithEvents"]:
                for event in competition["events"]:
                    i += 1
                    # print(i,event["names"]["0"].replace('.',''))
                    thread = threading.Thread(target=get_info, args=(event["id"],))
                    thread.start()
                    threads.append(thread)
    for thread in threads:
        thread.join()
main("http://gR8bNG1g:jknP4TJU@45.152.226.38:61950")
# print(main("http://gR8bNG1g:jknP4TJU@45.152.226.38:61950"))