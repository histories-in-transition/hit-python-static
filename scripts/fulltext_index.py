import json
import os
from acdh_cfts_pyutils import TYPESENSE_CLIENT as client
from typesense.api_call import ObjectNotFound

from .fetch_data import DATA_DIR, MAIN_DATA_FILE, ID_FIELD


def fulltext_index():
    print("startin with fulltext index")
    COLLECTION_NAME = "JAD"
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
            {"name": "language", "type": "object", "facet": True, "optional": True},
            {"name": "manuscript", "type": "object[]", "facet": True, "optional": True},
            {"name": "work", "type": "object[]", "facet": True, "optional": True},
        ],
    }
    client.collections.create(current_schema)
    with open(os.path.join(DATA_DIR, MAIN_DATA_FILE), "r", encoding="utf-8") as f:
        data = json.load(f)
    records = []
    for _, value in data.items():
        item = {"id": value[ID_FIELD]}
        item["rec_id"] = f"{value[ID_FIELD]}.html"
        item["title"] = f'{value["passage"]}'
        item["full_text"] = f'{value["passage"]} {value["text_paragraph"]}'
        item["language"] = value["language"]
        item["manuscript"] = value["manuscript"]
        item["work"] = value["work"]
        records.append(item)
    make_index = client.collections[COLLECTION_NAME].documents.import_(records)
    print(make_index)
    print(f"done with indexing {COLLECTION_NAME}")


if __name__ == "__main__":
    fulltext_index()
