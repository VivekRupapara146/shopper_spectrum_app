import streamlit as st

from utils.recommender import (
    get_product_choices,
    get_recommendations,
)


def render_recommender(artifacts, go_to):

    st.button(
        "← Back to Home",
        on_click=go_to,
        args=("home",)
    )

    st.title("🔗 Product Recommender")

    st.markdown(
        """
Find products that customers frequently purchase together using
**Item-Based Collaborative Filtering**.
"""
    )

    similarity_matrix = artifacts["similarity_matrix"]
    stockcode_to_desc = artifacts["stockcode_to_desc"]

    product_options = get_product_choices(
        stockcode_to_desc
    )

    selected_label = st.selectbox(
        "Search Product",
        options=list(product_options.keys()),
        index=None,
        placeholder="Start typing a product..."
    )

    if not selected_label:
        return

    selected_stockcode = product_options[selected_label]

    st.write("")

    st.markdown(
        f"""
    <div style="
    border:1px solid rgba(128,128,128,0.3);
    border-radius:12px;
    padding:1rem;
    margin-bottom:1rem;
    background-color:rgba(128,128,128,0.05);
    ">
    <h3 style="margin-top:0;">📦 Selected Product</h3>

    <b>{stockcode_to_desc[selected_stockcode]}</b><br>

    StockCode:
    <code>{selected_stockcode}</code>

    </div>
    """,
        unsafe_allow_html=True,
    )
    top_n = st.slider(
    "Number of Recommendations",
    min_value=5,
    max_value=20,
    value=10,
    )
    def similarity_color(score):

        if score >= 0.70:
            return "#2E7D32"

        elif score >= 0.40:
            return "#1565C0"

        elif score >= 0.20:
            return "#EF6C00"

        return "#757575"

    recommendations = get_recommendations(
        selected_stockcode,
        similarity_matrix,
        stockcode_to_desc,
        top_n=top_n,
    )

    if not recommendations:
        st.warning("No similar products found for this item.")
        return

    st.write("")
    st.markdown("### Recommended Products")
    st.caption(
        f"Showing top {top_n} products most frequently purchased "
        f"by customers who also bought this item."
    )
    
    cols = st.columns(2)

    for idx, rec in enumerate(recommendations, start=1):

        similarity_pct = rec["similarity"] * 100

        color = similarity_color(rec["similarity"])

        with cols[(idx - 1) % 2]:

            st.markdown(
                f"""
    <div style="
    border:1px solid rgba(128,128,128,0.25);
    border-radius:12px;
    padding:0.8rem;
    margin-bottom:1rem;
    ">

    <b>{idx}. {rec['description']}</b>
    <br>
    StockCode:
    <code>{rec['stockcode']}</code>
    <span style="
    color:{color};
    font-weight:bold;
    ">
    <br>
    Match Score: {similarity_pct:.1f}%
    
    </span>

    </div>
   
    """,
                unsafe_allow_html=True,
            )
            st.progress(rec["similarity"])
    st.write("")

    st.write("")

    tab1, tab2 = st.tabs(
        ["📖 Why These Recommendations?", "📊 Model Details"]
    )

    with tab1:

        st.markdown("""
    Recommendations are generated using **Item-Based Collaborative Filtering**.

    The model looks at historical customer purchase behavior and identifies
    products that tend to be bought by the same customers.

    ### Example

    If many customers purchased:

    - Product A
    - Product B

    together,

    then Product B becomes a strong recommendation whenever Product A is selected.

    ### Similarity Score

    The match score represents cosine similarity between products based on customer purchase behavior.

    - 70%+ → Very Strong Match (green)
    - 40-70% → Strong Match (blue)
    - 20-40% → Moderate Match (orange)
    - Below 20% → Weak Match (grey)

    Higher scores indicate that customers who purchased the selected product frequently purchased the recommended product as well.
    """)

    with tab2:

        st.markdown("""
    ### Algorithm

    **Item-Based Collaborative Filtering**

    ### Similarity Metric

    - Cosine Similarity

    ### Supported Products

    - 3,148 products

    ### Recommendation Length

    - Top 10 products

    ### Evaluation

    - Recommendation Precision: **10.7%**
    - Hit Rate: **61%**

    ### Purpose

    Generate personalized product recommendations based on
    historical co-purchase behavior.
    """)