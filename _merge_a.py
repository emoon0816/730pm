import json, sys

P = "/home/admin/newspaper/data.json"
with open(P, encoding="utf-8") as f:
    data = json.load(f)
with open("/home/admin/newspaper/_new_a.json", encoding="utf-8") as f:
    new = json.load(f)

mine = {t["id"]: t for t in new["tabs"]}
order = [t["id"] for t in data["tabs"]]
assert order == ["head", "politics", "tech", "science", "ent", "sport", "hot", "game", "food", "trivia", "today", "reading"], order

data["date"] = new["date"]
data["weekday"] = new["weekday"]
data["issue"] = new["issue"]
data["lead"] = new["lead"]
data["tabs"] = [mine[t["id"]] if t["id"] in mine else t for t in data["tabs"]]

with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write("\n") if False else None

# report
print("tabs:", [(t["id"], sum(len(g["items"]) for g in t.get("groups", []))) for t in data["tabs"]])
print("date:", data["date"], data["weekday"], data["issue"])
print("lead:", data["lead"]["title"])
for t in data["tabs"]:
    if t["id"] in mine:
        for g in t["groups"]:
            for it in g["items"]:
                print(t["id"], "|", "u=", bool(it.get("u")), "|", it["t"])
