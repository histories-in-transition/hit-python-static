import json
import os
from acdh_cfts_pyutils import TYPESENSE_CLIENT as client
from typesense.api_call import ObjectNotFound

try:
    from .fetch_data import DATA_DIR, ID_FIELD
except ImportError:
    from fetch_data import DATA_DIR, ID_FIELD

MAIN_DATA_FILE = "ms_items.json"


def fulltext_index():
    COLLECTION_NAME = "hit__msitems"
    print(f"building typesense index for {COLLECTION_NAME} with fulltext index")

    with open(os.path.join(DATA_DIR, "hands.json"), "r", encoding="utf-8") as f:
        hands_lookup = json.load(f)

    try:
        client.collections[COLLECTION_NAME].delete()
    except ObjectNotFound:
        pass

    current_schema = {
        "name": COLLECTION_NAME,
        "enable_nested_fields": True,
        "fields": [
            {"name": "id", "type": "string", "sort": True},
            {"name": "rec_id", "type": "string", "sort": True},
            {"name": "title", "type": "string", "sort": True},
            {"name": "full_text", "type": "string", "sort": True},
            {"name": "incipit", "type": "string", "optional": True},
            {"name": "explicit", "type": "string", "optional": True},
            {"name": "rubric", "type": "string", "optional": True},
            {"name": "manuscript", "type": "object", "facet": True, "optional": True},
            {"name": "work", "type": "object", "facet": True, "optional": True},
            {"name": "hand_roles", "type": "string[]", "facet": True, "optional": True},
            {"name": "hand_dates", "type": "string[]", "facet": True, "optional": True},
        ],
    }
    client.collections.create(current_schema)
    with open(os.path.join(DATA_DIR, MAIN_DATA_FILE), "r", encoding="utf-8") as f:
        data = json.load(f)
    records = []
    for _, value in data.items():
        item = {"id": value[ID_FIELD]}
        item["rec_id"] = f"{value[ID_FIELD]}.html"
        item["title"] = f'{value["view_label"]}'
        item["incipit"] = f'{value["incipit"]}'
        item["explicit"] = f'{value["explicit"]}'
        item["rubric"] = f'{value["rubric"]}'
        try:
            title_work = f'{value["title_work"][0]["title"]}'
        except IndexError:
            title_work = ""
        item["full_text"] = (
            f'{value["incipit"]} {value["explicit"]} {value["rubric"]} {title_work}'.strip()
        )  # noqa: E501
        ms = {}
        try:
            sms = value["manuscript"][0]
        except IndexError:
            continue
        slib = sms["library_full"][0]
        ms["hit_id"] = sms["hit_id"]
        ms["shelfmark"] = sms["shelfmark"][0]["value"]
        ms["library"] = {
            "abbr": slib["label"],
            "name": slib["library_full"],
            "hit_id": slib["hit_id"],
        }
        item["manuscript"] = ms
        dates = []
        for x in sms["manuscripts_dated"]:
            for y in x["date"]:
                dates.append(
                    {
                        "not_before": y["not_before"],
                        "not_after": y["not_after"],
                        "label": y["label"],
                    }
                )
        ms["dated"] = dates
        hand_roles = []
        hand_dates = []
        for x in value["hands_role"]:
            hand_id = str(x["hand"][0]["id"])
            hand = hands_lookup[hand_id]
            for date in hand["hands_dated"]:
                for y in date["dated"]:
                    try:
                        hand_dates.append(y["label"])
                    except KeyError:
                        continue
            for y in x["role"]:
                hand_roles.append(y["value"])
        item["hand_roles"] = hand_roles
        item["hand_dates"] = hand_dates
        try:
            swork = value["title_work"][0]
        except IndexError:
            work = {}
            swork = {}
        if swork:
            work = {}
            work["title"] = swork["title"]
            work["hit_id"] = swork["hit_id"]
            try:
                work["author"] = swork["author"][0]["name"]
            except IndexError:
                work["author"] = ""

        item["work"] = work
        records.append(item)
    with open("hansi.json", "w", encoding="utf-8") as fp:
        json.dump(records, fp, ensure_ascii=False, indent=4)
    make_index = client.collections[COLLECTION_NAME].documents.import_(records)
    print(make_index)
    print(f"done with indexing {COLLECTION_NAME}")


if __name__ == "__main__":
    fulltext_index()
