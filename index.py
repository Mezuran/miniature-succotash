import streamlit as st

from pathlib import Path
from libs import Utils

st.set_page_config(layout='wide')

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
pages_dir = current_dir / "pages"

page_files = [f for f in pages_dir.glob("*.py") if f.name != "__init__.py"]
if not page_files:
    st.error(f"No pages found! I looked in: `{pages_dir}`")
    st.stop()

page_files.sort()

all_pages = []

for file_path in page_files:
    # Get config securely
    config = Utils.get_page_config(file_path)
    
    # Defaults
    default_title = file_path.stem.replace("_", " ").title()
    title = config.get("title", default_title)
    icon = config.get("icon", ":material/article:")
    
    # Create the page
    page = st.Page(str(file_path), title=title, icon=icon)
    all_pages.append(page)

# 4. Run Navigation
if all_pages:
    pg = st.navigation(all_pages, position="top")
    pg.run()
else:
    st.error("No pages found.")