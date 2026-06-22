"""
data_loader.py

Centralized, cached loading of all model artifacts produced by the
Customer_Segmentation_and_Product_Recommendations notebook (Section 8).

Why this lives in its own module rather than inline in app.py:
- Keeps app.py focused on UI/routing only.
- st.cache_resource ensures these (potentially large) objects -- especially
  the item-item similarity matrix -- are loaded from disk exactly once per
  app session, not on every rerun/interaction.
- A single source of truth for file paths and load logic, so a future
  FastAPI service could reuse this same function without touching Streamlit.
"""

import os
import joblib
import streamlit as st

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")

REQUIRED_FILES = {
    "kmeans_model": "kmeans_model.pkl",
    "scaler": "rfm_scaler.pkl",
    "cluster_name_map": "cluster_name_map.pkl",
    "similarity_matrix": "item_similarity_matrix.pkl",
    "stockcode_to_desc": "stockcode_to_description.pkl",
}


@st.cache_resource(show_spinner="Loading model artifacts...")
def load_artifacts():
    """
    Loads all 5 saved artifacts from the models/ directory.

    Returns:
        dict with keys: kmeans_model, scaler, cluster_name_map,
        similarity_matrix, stockcode_to_desc

    On failure (missing/corrupted file), shows a clear Streamlit error
    and stops the app -- rather than letting a raw traceback surface,
    which would be a poor experience for anyone other than the developer.
    """
    artifacts = {}
    missing = []

    for key, filename in REQUIRED_FILES.items():
        filepath = os.path.join(MODELS_DIR, filename)
        if not os.path.exists(filepath):
            missing.append(filename)
            continue
        try:
            artifacts[key] = joblib.load(filepath)
        except Exception as e:
            st.error(
                f"Failed to load '{filename}'. The file may be corrupted "
                f"or saved with an incompatible library version.\n\nDetails: {e}"
            )
            st.stop()

    if missing:
        st.error(
            "Missing required model file(s):\n\n"
            + "\n".join(f"- `{m}`" for m in missing)
            + f"\n\nPlace all 5 `.pkl` files (saved in Section 8 of the notebook) "
              f"inside the `models/` folder at:\n`{MODELS_DIR}`"
        )
        st.stop()

    return artifacts
