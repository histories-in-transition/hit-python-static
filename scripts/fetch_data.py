import json
import os
import shutil
import requests
from jsonpath_ng import parse

try:
    from .models import MODEL_CONFIG, ID_FIELD
except ImportError:
    from models import MODEL_CONFIG, ID_FIELD

MAIN_DATA_FILE = "passages.json"
GH_URL = (
    "https://raw.githubusercontent.com/histories-in-transition/hit-baserow-dump/main/"
)
DATA_DIR = os.path.join("html", "data")


def fetch_data():
    shutil.rmtree(DATA_DIR, ignore_errors=True)

    os.makedirs(DATA_DIR, exist_ok=True)

    for x in MODEL_CONFIG:
        jsonpath_expr = parse(x["label_lookup_expression"])
        url = f"{GH_URL}{x['data_source']}.json"
        data = requests.get(url).json()
        save_path = os.path.join(DATA_DIR, f'{x["file_name"]}.json')
        print(f"downloading {url} and saving it to {save_path}")

        # add prev/next
        key_list = sorted(data.keys())
        for i, v in enumerate(key_list):
            prev_item = data[key_list[i - 1]][ID_FIELD]
            try:
                next_item = data[key_list[i + 1]][ID_FIELD]
            except IndexError:
                next_item = data[key_list[0]]
            value = data[key_list[i]]

            value["prev"] = f"{prev_item}.html"
            value["next"] = f"{next_item}.html"

        # add view_labels
        for _, value in data.items():
            if x["file_name"] == "ms_items":
                try:
                    value["view_label"] = (
                        f'{value["manuscript"][0]["shelfmark"][0]["value"]}, {value["id"]}'
                    )
                except IndexError:
                    value["view_label"] = "no manuscript realted to this item"
            else:
                try:
                    value["view_label"] = jsonpath_expr.find(value)[0].value
                except IndexError:
                    value["view_label"] = f"NO MATCH FOR {x['label_lookup_expression']}"
        with open(save_path, "w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False)


def remove_fields():
    for x in MODEL_CONFIG:
        try:
            to_delete = x["delete_fields"]
        except KeyError:
            continue
        save_path = os.path.join(DATA_DIR, f'{x["file_name"]}.json')
        for field_path in to_delete:
            print(f"removing {field_path} from {save_path}")
            with open(save_path, "r") as fp:
                source_data = json.load(fp)
            jsonpath_expr = parse(field_path)
            cleaned_data = jsonpath_expr.filter(lambda d: True, source_data)
            with open(save_path, "w", encoding="utf-8") as fp:
                json.dump(cleaned_data, fp, ensure_ascii=True)


def add_related_objects():
    for x in MODEL_CONFIG:
        try:
            rel_obj = x["related_objects"]
        except KeyError:
            continue
        save_path = os.path.join(DATA_DIR, f'{x["file_name"]}.json')
        with open(save_path, "r") as fp:
            source_data = json.load(fp)

        for item in rel_obj:
            source_file = item["source_file"]
            lookup_field = item["lookup_field"]

            feed_path = os.path.join(DATA_DIR, f"{source_file}.json")
            with open(feed_path, "r") as fp:
                feed_data = json.load(fp)

            for key, value in source_data.items():
                object_id = value[ID_FIELD]
                related_items = []
                for _, rel_value in feed_data.items():
                    for m in rel_value[lookup_field]:
                        if m[ID_FIELD] == object_id:
                            related_items.append(rel_value)
                            break
                value[f"related__{source_file}"] = related_items
        with open(save_path, "w", encoding="utf-8") as fp:
            json.dump(source_data, fp, ensure_ascii=True)


def custom_enrichment():

    with open(os.path.join(DATA_DIR, "ms_items.json"), "r") as fp:
        source_data = json.load(fp)

    with open(os.path.join(DATA_DIR, "hands.json"), "r") as fp:
        seed_data = json.load(fp)

    for key, value in source_data.items():
        for x in value["hands_role"]:
            new_value = []
            for y in x["hand"]:
                obj_id = f'{y["id"]}'

                orig_hand = seed_data[obj_id]
                hand = {
                    "hit_id": orig_hand["hit_id"],
                    "view_label": y["value"],
                    "hands_dated": orig_hand["hands_dated"],
                    "hands_placed": orig_hand["hands_placed"],
                    "role": x["role"],
                }

                new_value.append(hand)
            value["hands_role"] = new_value

    with open(os.path.join(DATA_DIR, "ms_items.json"), "w") as fp:
        json.dump(source_data, fp, ensure_ascii=False)


def process_data():
    fetch_data()
    remove_fields()
    custom_enrichment()
    add_related_objects()


if __name__ == "__main__":
    process_data()
