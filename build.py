from scripts.fetch_data import process_data
from scripts.build_static import build_static
from scripts.build_dynamic import build_dynamic
from scripts.list_views import build_list_views
from scripts.fulltext_index import fulltext_index


# from scripts.fulltext_index import fulltext_index

process_data()
build_static()
build_dynamic()
build_list_views()
try:
    fulltext_index()
except Exception as e:
    print(f"building fulltext index failed due to {e}")
