# pages/decision-lookup.py
import streamlit as st
import importlib.util
import pandas as pd
import os
import io

# ============================================================
#  LOAD LOGIC TỪ scripts/decision-lookup.py
# ============================================================
SCRIPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'scripts', 'decision-lookup.py')
)
spec = importlib.util.spec_from_file_location("decision_lookup_logic", SCRIPT_PATH)
logic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logic)

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Decision Lookup | FE QA Tools",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ... phần còn lại giữ nguyên từ "THEME" trở xuống ...
# (toàn bộ code UI bạn đã gửi, từ dòng THEME cho đến hết file)
