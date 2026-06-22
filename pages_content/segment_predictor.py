"""
segment_predictor.py

UI for the Customer Segment Predictor module.

Design decisions worth noting:
- Inputs are wrapped in st.form so the model only runs once, on explicit
  submit -- not on every keystroke/widget rerun, which is both better UX
  and avoids wasted predict() calls.
- min_value constraints on the inputs do the validation work (e.g. a
  customer can't have a negative Monetary value, or 0 past Frequency,
  since they wouldn't exist in the dataset in the first place).
- The "compare to segment" metrics use delta_color="inverse" specifically
  for Recency, since for that one feature LOWER is better (more recent) --
  using the default "normal" coloring there would show a good outcome
  (very recent purchase) in red, which would be actively misleading.
"""

import streamlit as st
from utils.segmentation import predict_segment, get_segment_profiles

SEGMENT_DESCRIPTIONS = {
    "High-Value": (
        "Your most valuable customers — recent, frequent buyers with the "
        "highest spend. The primary revenue driver of the business despite "
        "being the smallest group."
    ),
    "Regular": (
        "Moderately engaged, established repeat buyers. Reliable revenue, "
        "with room to grow toward High-Value through targeted upselling."
    ),
    "Occasional": (
        "Recent but low-commitment buyers — possibly newer customers who "
        "haven't yet built a purchase habit. Good candidates for "
        "habit-building campaigns."
    ),
    "At-Risk": (
        "The largest segment, but the weakest across Recency, Frequency, "
        "and Monetary. Strong candidates for a win-back campaign before "
        "they churn entirely."
    ),
}

SEGMENT_ACTIONS = {
    "High-Value": [
        "Retain aggressively through VIP programs",
        "Offer early-access promotions",
        "Provide priority customer support"
    ],
    "Regular": [
        "Encourage upselling and cross-selling",
        "Increase purchase frequency",
        "Reward repeat purchases"
    ],
    "Occasional": [
        "Promote repeat purchases",
        "Send personalized recommendations",
        "Build purchasing habits with incentives"
    ],
    "At-Risk": [
        "Run win-back campaigns",
        "Offer re-engagement discounts",
        "Target with retention-focused messaging"
    ],
}

SEGMENT_COLORS = {
    "High-Value": "#2E7D32",
    "Regular": "#1565C0",
    "Occasional": "#F9A825",
    "At-Risk": "#C62828",
}


def render_segment_predictor(artifacts, go_to):
    st.button("← Back to Home", on_click=go_to, args=("home",))
    st.title("🧩 Customer Segment Predictor")
    st.write(
        "Enter a customer's purchase behavior to predict which segment "
        "they belong to, based on a KMeans clustering model trained on "
        "Recency, Frequency, and Monetary value (RFM)."
    )

    with st.form("segment_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            recency = st.number_input(
                "Recency (days since last purchase)",
                min_value=0, max_value=1000, value=30, step=1,
                help="How many days ago did this customer last make a purchase?",
            )
        with col2:
            frequency = st.number_input(
                "Frequency (number of past orders)",
                min_value=1, max_value=500, value=3, step=1,
                help="How many distinct orders has this customer placed in total?",
            )
        with col3:
            monetary = st.number_input(
                "Monetary (total amount spent, £)",
                min_value=0.01, max_value=300000.0, value=500.0, step=10.0,
                help="Total amount this customer has spent historically, in GBP.",
            )
        submitted = st.form_submit_button(
            "Predict Segment", type="primary", use_container_width=True
        )

    if not submitted:
        return

    cluster_id, segment_name = predict_segment(
        recency, frequency, monetary,
        artifacts["kmeans_model"], artifacts["scaler"], artifacts["cluster_name_map"],
    )

    color = SEGMENT_COLORS.get(segment_name, "#555555")
    st.markdown(
        f"""
        <div style="border-left: 6px solid {color}; padding: 1rem 1.5rem;
                    border-radius: 8px; background-color: rgba(128,128,128,0.08);
                    margin-top: 1rem;">
            <h3 style="margin-top:0; color:{color};">
                Predicted Segment: {segment_name}
            </h3>
            <p style="margin-bottom:0;">{SEGMENT_DESCRIPTIONS.get(segment_name, "")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.write("")

    st.markdown("#####  🎯 Recommended Business Actions")

    for action in SEGMENT_ACTIONS.get(segment_name, []):
        st.markdown(f"- {action}")
    st.write("")
    profiles = get_segment_profiles(
        artifacts["kmeans_model"], artifacts["scaler"], artifacts["cluster_name_map"]
    )
    predicted_row = profiles[profiles["Segment"] == segment_name].iloc[0]

    st.markdown("##### How this customer compares to the *typical* customer in this segment")
    m1, m2, m3 = st.columns(3)
    recency_diff = recency - predicted_row["Recency"]
    if abs(recency_diff) < 1:
        recency_delta = "Near segment average"
    else:
        recency_delta = (
            f"{abs(recency_diff):.0f} days "
            f"{'higher' if recency_diff > 0 else 'lower'} than segment avg"
        ) 
    
    m1.metric(
        "Recency (days)",
        f"{recency:.0f}",
        delta=recency_delta,
        delta_color="inverse"
    )
    
    freq_diff = frequency - predicted_row["Frequency"]
    if abs(freq_diff) < 1:
        freq_delta = "Near segment average"
    else:
        freq_delta = (
            f"{abs(freq_diff):.0f} order "
            f"{'above' if freq_diff > 0 else 'below'} segment avg"
        )     
    m2.metric(
        "Frequency (orders)",
        f"{frequency:.0f}",
        delta=freq_delta
    )
    
    money_diff = monetary - predicted_row["Monetary"]
    if abs(money_diff) < 1:
        money_delta = "Near segment average"
    else:
        money_delta = (
            f"£ {abs(money_diff):.0f} "
            f"{'above' if money_diff > 0 else 'below'} segment avg"
        ) 
    m3.metric(
        "Monetary (£)",
        f"£{monetary:,.2f}",
        delta=money_delta
    )
    with st.expander("Compare all four segment profiles"):
        display_df = profiles.copy()
        display_df["Recency"] = display_df["Recency"].round(1)
        display_df["Frequency"] = display_df["Frequency"].round(1)
        display_df["Monetary"] = display_df["Monetary"].round(2)

        def hex_to_rgba(hex_color, alpha=0.20):
            hex_color = hex_color.lstrip("#")
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f"rgba({r},{g},{b},{alpha})"


        def highlight_predicted(row):
            if row["Segment"] == segment_name:
                bg = hex_to_rgba(
                    SEGMENT_COLORS.get(segment_name, "#555555"),
                    alpha=0.20
                )
                return [f"background-color: {bg}"] * len(row)

            return [""] * len(row)

        st.dataframe(
            display_df.style.apply(highlight_predicted, axis=1),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "These are the *typical* (centroid) values for each segment, "
            "reconstructed directly from the trained model — not raw "
            "averages recomputed from the original dataset."
        )
        st.write("")

        with st.expander("ℹ️ About This Model"):
            st.markdown("""
        **Algorithm:** K-Means Clustering

        **Features Used**
        - Recency (days since last purchase)
        - Frequency (number of orders)
        - Monetary (total spend)

        **Training Dataset**
        - UCI Online Retail Dataset
        - 391,150 cleaned transactions
        - 4,334 customers

        **Model Performance**
        - Number of Clusters: 4
        - Silhouette Score: 0.338

        **Purpose**
        This model groups customers into behavior-based segments to support
        targeted marketing, retention campaigns, and customer value analysis.
        """)