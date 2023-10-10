import time, os
from fuzzywuzzy import fuzz
from fonbet import main as fonbet_bets
from datetime import datetime
from olimp import main as olimp_bets

overlapping_bids = [
    ["П1","П2"],
    ["Фора 1", "Фора 2"],
    ["ТотМ","ТотБ"]
]
def find_similar_strings(dict1, dict2, threshold):
    similar_pairs = []

    for str1 in dict1:
        for str2 in dict2:
            similarity = fuzz.ratio(str1, str2)
            if similarity >= threshold:
                similar_pairs.append((str1, str2, similarity))

    return similar_pairs

cooldown = 0
# cooldown = float(input("[Scanner] Enter scanner cooldown (miliseconds): "))
print("[STATUS] Scanner stated.")
start_time = time.time()
while True:
    o = olimp_bets()
    f = fonbet_bets()
    end_time = time.time()
    execution_time = end_time - start_time
    os.system('cls')
    print(execution_time)
    similar_strings = find_similar_strings(o, f, 70)
    for event2, event, similarity in similar_strings:
        for overlapping_bid in overlapping_bids:
            if overlapping_bid[0] in o[event2].keys() and overlapping_bid[0] in f[event].keys():
                o1, o2, f1, f2 = o[event2][overlapping_bid[0]], o[event2][ overlapping_bid[1]], f[event][overlapping_bid[0]], f[event][overlapping_bid[1]]
                if o1 != 0 and o2 != 0 and f1 != 0 and f2 != 0:
                    # f2 = 150
                    k1 = (1/o1)+(1/f2)
                    k2 = (1/f1)+(1/o2) 
                    # Расчет возможного заработка
                    time_now = datetime.now().strftime("[%H:%M:%S]")
                    if k1 < k2:
                        percent = round((1-k1)*100,2)
                        if 10 > percent > 0:
                            print(time_now,event)
                            print(time_now,f"Вилка {percent}%")
                            print(time_now,f"[Fonbet] Поставить на {overlapping_bid[1]} ({f2}):", f[event]["url"])
                            print(time_now,f"[Olimp] Поставить на {overlapping_bid[0]} ({o1}):", o[event2]["url"])
                            print("\n")
                    else:
                        percent = round((1-k2)*100,2)
                        if  10 >percent > 0:
                            print(time_now,event)
                            print(time_now,f"Вилка {percent}%")
                            print(time_now,f"[Fonbet] Поставить на {overlapping_bid[0]} ({f1}):", f[event]["url"])
                            print(time_now,f"[Olimp] Поставить на {overlapping_bid[1]} ({o2}):", o[event2]["url"])
                            print("\n")
    # break
    time.sleep(cooldown/1000)
    start_time = time.time()