from scripts.fetch_data import fetch_data, add_related_objects
from scripts.build_static import build_static

# from scripts.build_dynamic import build_dynamic
# from scripts.fulltext_index import fulltext_index
# from scripts.list_views import build_list_views

fetch_data()
add_related_objects()
build_static()
# build_dynamic()
# build_list_views()
# try:
#     fulltext_index()
# except Exception as e:
#     print(f"building fulltext index failed due to {e}")
