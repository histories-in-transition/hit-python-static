ID_FIELD = "hit_id"

MODEL_CONFIG = [
    {
        "data_source": "data/manuscripts",
        "verbose_name_pl": "Manuscripts",
        "verbose_name_sg": "Manuscript",
        "file_name": "manuscripts",
        "label_lookup_expression": "$..shelfmark[0].value",
        "related_objects": [],
    },
    {
        "data_source": "data/strata",
        "verbose_name_pl": "Strata",
        "verbose_name_sg": "Stratum",
        "file_name": "strata",
        "label_lookup_expression": "$..label[0].value",
        "related_objects": [],
    },
]
