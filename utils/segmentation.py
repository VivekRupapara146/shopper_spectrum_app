"""
segmentation.py

Core prediction logic for the Customer Segment Predictor module.

Deliberately framework-independent (no Streamlit imports here) -- these
functions take plain values and sklearn/joblib objects in, and return
plain values out. That means they could be unit-tested directly, or
reused later behind a FastAPI endpoint, without any change.

Preprocessing here MUST mirror the notebook's Section 6 pipeline exactly:
    raw RFM -> log1p -> scaler.transform() -> kmeans.predict()
Using scaler.fit_transform() on new data here would be a critical bug --
it would compute a different mean/std than what the model was trained on.
"""

import numpy as np
import pandas as pd


def predict_segment(recency, frequency, monetary, kmeans_model, scaler, cluster_name_map):
    """
    Predicts the customer segment for a single new customer.

    Args:
        recency: days since last purchase
        frequency: number of distinct past orders
        monetary: total historical spend
        kmeans_model: fitted KMeans model (loaded from kmeans_model.pkl)
        scaler: the SAME StandardScaler fitted during training (rfm_scaler.pkl)
        cluster_name_map: dict mapping cluster id -> persona name

    Returns:
        (cluster_id: int, segment_name: str)
    """
    new_data_log = np.log1p([[recency, frequency, monetary]])
    new_data_scaled = scaler.transform(new_data_log)
    cluster_id = int(kmeans_model.predict(new_data_scaled)[0])
    segment_name = cluster_name_map[cluster_id]
    return cluster_id, segment_name


def get_segment_profiles(kmeans_model, scaler, cluster_name_map):
    """
    Reconstructs the *typical* (centroid) Recency/Frequency/Monetary values
    for each segment, in original real-world units (days / count / currency).

    Why this works without needing a separately saved centroid table:
    the KMeans model stores its centroids in scaled-log space. Reversing
    the exact same pipeline used to create that space --
    scaler.inverse_transform() then np.expm1() (the inverse of log1p) --
    recovers an approximate "average customer" profile per segment, derived
    purely from the 3 already-saved artifacts.

    Returns:
        pandas.DataFrame with columns: Segment, Recency, Frequency, Monetary
    """
    centroids_scaled = kmeans_model.cluster_centers_
    centroids_log = scaler.inverse_transform(centroids_scaled)
    centroids_raw = np.expm1(centroids_log)

    profiles = pd.DataFrame(centroids_raw, columns=["Recency", "Frequency", "Monetary"])
    profiles["Segment"] = [cluster_name_map[i] for i in range(len(profiles))]
    return profiles[["Segment", "Recency", "Frequency", "Monetary"]]
