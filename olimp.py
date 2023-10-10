import requests, json
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36",
    "X-GUID": "01d43413c9f7a92f544ec04e5f23b60b",
    "cookie": "visitor_id=01d43413c9f7a92f544ec04e5f23b60b; visitor_id_version=2; user_ukey=34ea0b2e-cd1f-41f1-824c-6b819370d82f; theme=dark"
}
bets = {}
def main():
    response = requests.get("https://www.olimp.bet/api/v4/0/live/broadcast/sports-with-competitions-with-events", headers=headers).json()
    # for args in response[0]["payload"]:
    #     print(response[0][args])
    i = 0
    for sport in range(len(response)):
        sport_name = response[sport]["payload"]["sport"]["name"]
        if sport_name == "Теннис":
            # print(sport_name)
            for competition in response[sport]["payload"]["competitionsWithEvents"]:
                i +=1
                # print(competition["competition"]["name"])
                for event in competition["events"]:
                    event_name = event["names"]["0"].replace('.','')
                    bets[event_name] = {"П1": 0, "П2": 0, "url": "https://www.olimp.bet/live/"+str(event["sportId"])+"/"+str(event["competitionId"])+"/"+str(event['id'])}
                    # print("-",event_name)
                    if len(event["outcomes"]) > 0:
                        for outcome in event["outcomes"]:
                            # print(outcome["shortName"])
                            bets[event_name][outcome["shortName"]] = float(outcome["probability"])
            break
    return bets
# print(main())