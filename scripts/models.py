ID_FIELD = "hit_id"

MODEL_CONFIG = [
    {
        "data_source": "data/manuscripts",
        "verbose_name_pl": "Manuscripts",
        "verbose_name_sg": "Manuscript",
        "file_name": "manuscripts",
        "label_lookup_expression": "$..shelfmark[0].value",
        "related_objects": [
            {
                "source_file": "ms_items",
                "lookup_field": "manuscript"
            }
        ],
    },
    {
        "data_source": "data/strata",
        "verbose_name_pl": "Strata",
        "verbose_name_sg": "Stratum",
        "file_name": "strata",
        "label_lookup_expression": "$..label[0].value",
        "related_objects": [],
    },
    {
        "data_source": "data/works",
        "verbose_name_pl": "Works",
        "verbose_name_sg": "Work",
        "file_name": "works",
        "label_lookup_expression": "$.title",
        "related_objects": [],
    },
    {
        "data_source": "data/ms_items",
        "verbose_name_pl": "Manuscript Items",
        "verbose_name_sg": "Manuscript Item",
        "file_name": "ms_items",
        "label_lookup_expression": "$..label[0].value",
        "related_objects": [],
    },
]
