import os
import jinja2
import json

try:
    from .build_static import out_dir
except ImportError:
    from build_static import out_dir

try:
    from .fetch_data import MODEL_CONFIG
except ImportError:
    from fetch_data import MODEL_CONFIG


templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)


def build_list_views():
    print("building list views")
    with open("project.json", "r", encoding="utf-8") as f:
        project_data = json.load(f)
    os.makedirs(out_dir, exist_ok=True)
    page_template = templateEnv.get_template("./templates/dynamic/generic_list_view.j2")

    for x in MODEL_CONFIG:
        save_path = os.path.join(out_dir, f'{x["file_name"]}.html')
        print(save_path)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(page_template.render({"project_data": project_data, "data": x}))


if __name__ == "__main__":
    build_list_views()
