import os
import jinja2
import json

try:
    from .build_static import out_dir
except ImportError:
    from build_static import out_dir

try:
    from .fetch_data import DATA_DIR, MODEL_CONFIG, ID_FIELD
except ImportError:
    from fetch_data import DATA_DIR, MODEL_CONFIG, ID_FIELD

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)


def build_dynamic():
    with open("project.json", "r", encoding="utf-8") as f:
        project_data = json.load(f)

    for x in MODEL_CONFIG:

        print("#########################")
        print(f"building {x['verbose_name_sg']} detail view pages")

        with open(
            os.path.join(DATA_DIR, f'{x["file_name"]}.json'), "r", encoding="utf-8"
        ) as f:
            items = json.load(f)

        os.makedirs(out_dir, exist_ok=True)
        try:
            page_template = templateEnv.get_template(
                f"./templates/dynamic/{x['file_name']}_template.j2"
            )
        except jinja2.exceptions.TemplateNotFound:
            page_template = templateEnv.get_template(
                "./templates/dynamic/generic_detail.j2"
            )

        key_list = sorted(items.keys())
        for i, v in enumerate(key_list):
            prev_item = items[key_list[i - 1]][ID_FIELD]
            try:
                next_item = items[key_list[i + 1]][ID_FIELD]
            except IndexError:
                next_item = items[key_list[0]]
            value = items[key_list[i]]

            output_path = os.path.join(out_dir, f"{value[ID_FIELD]}.html")
            data = value
            data["prev"] = f"{prev_item}.html"
            data["next"] = f"{next_item}.html"
            passage = value.get("passage", None)
            if passage:
                if len(passage) >= 35:
                    data["view_label"] = f"{passage[:35]}..."
                else:
                    data["view_label"] = passage
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(
                    page_template.render(
                        {
                            "project_data": project_data,
                            "data": data,
                            "model": x,
                            "label": data["view_label"],
                        }
                    )
                )


if __name__ == "__main__":
    build_dynamic()
