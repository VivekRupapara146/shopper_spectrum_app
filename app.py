"""
app.py

Shopper Spectrum -- main entry point.

Navigation pattern: a landing page with two clickable "module cards"
(Segment Predictor / Product Recommender), using st.session_state to
track the active view -- chosen instead of Streamlit's native pages/
folder system, since that auto-generates a sidebar we deliberately
aren't using here.
"""

import streamlit as st
from utils.data_loader import load_artifacts
from pages_content.segment_predictor import render_segment_predictor
from pages_content.recommender import render_recommender

# ----------------------------------------------------------------------------
# Page config -- must be the first Streamlit command in the script
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Shopper Spectrum",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# Session state initialization
# ----------------------------------------------------------------------------
if "view" not in st.session_state:
    st.session_state.view = "home"


def go_to(view_name: str):
    """Callback to switch the active view and trigger a rerun."""
    st.session_state.view = view_name


# ----------------------------------------------------------------------------
# Load model artifacts once (cached) -- used by Steps 2 & 3, loaded here
# up front so any missing-file error surfaces immediately on app start,
# rather than only when a user clicks into a module.
# ----------------------------------------------------------------------------
artifacts = load_artifacts()


# ----------------------------------------------------------------------------
# Minimal card styling for the landing page.
# Full light/dark theme system is added in a later step -- this is just
# enough CSS to make the landing page feel like a real product, not a
# default Streamlit form.
# ----------------------------------------------------------------------------
CARD_CSS = """
<style>
.module-card {
    border: 1px solid rgba(128,128,128,0.3);
    border-radius: 12px;
    padding: 1.75rem;
    text-align: center;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    height: 100%;
}
.module-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}
.module-card h2 {
    margin-bottom: 0.5rem;
}
.module-card p {
    opacity: 0.75;
    min-height: 48px;
}
</style>
"""
st.markdown(CARD_CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Views
# ----------------------------------------------------------------------------
def render_home():
    st.title("🛍️ Shopper Spectrum")

    st.markdown(
        "##### Customer Segmentation & Product Recommendations, "
        "powered by purchase behavior."
    )
    
    st.markdown("---")
    
    st.markdown("### What This Project Does")

    c1, c2 = st.columns(2)

    with c1:
        st.info("""
        🎯 Customer Segmentation

        Group customers into behavioral segments using:
        • Recency
        • Frequency
        • Monetary Value

        Helps identify:
        • High-value customers
        • At-risk customers
        • Growth opportunities
        """)

    with c2:
        st.info("""
        🛒 Product Recommendation

        Recommend products using:
        • Item-based Collaborative Filtering
        • Customer co-purchase patterns
        • Cosine Similarity

        Helps increase:
        • Cross-selling
        • Upselling
        • Customer engagement
        """)
    st.markdown("---")
    
    st.markdown(
    """
    <div style="
    border:1px solid rgba(255,255,255,0.15);
    border-radius:10px;
    padding:20px;
    background:rgba(255,255,255,0.03);
    ">

    <h3>📊 Dataset Overview</h3>

    <b>Source:</b> UCI Online Retail Dataset<br><br>

    <b>Transactions:</b> 391,150+<br>
    <b>Customers:</b> 4,334<br>
    <b>Products:</b> 3,148<br>
    <b>Time Period:</b> Dec 2010 – Dec 2011<br>
    <b>Country:</b> United Kingdom<br><br>

    <b>Project Applications:</b>
    <ul>
    <li>Customer Segmentation using K-Means</li>
    <li>RFM Customer Analysis</li>
    <li>Item-Based Collaborative Filtering</li>
    <li>Business Intelligence & Retention Strategy</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
    )
    
    st.markdown("---")

    st.markdown("### Model Performance")

    p1, p2, p3 = st.columns(3)

    p1.metric(
        "Silhouette Score",
        "0.338"
    )

    p2.metric(
        "Recommendation Precision",
        "0.107"
    )

    p3.metric(
        "Recommendation Coverage",
        "0.61"
    )

    st.write("")

    st.markdown("---")
    st.markdown("### Key Features")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        ✓ Customer Segmentation using K-Means

        ✓ RFM Analysis (Recency, Frequency, Monetary)

        ✓ Behavioral Customer Profiling

        ✓ Business Action Recommendations
        """)

    with c2:
        st.markdown("""
        ✓ Product Recommendation Engine

        ✓ Item-Based Collaborative Filtering

        ✓ Cosine Similarity Matching

        ✓ Interactive Streamlit Dashboard
        """)
    st.markdown("### Project Workflow")
    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.success("""
        Transactions → RFM Analysis → KMeans Clustering → Customer Segments
        """)

    with c2:
        st.success("""
        Transactions → Customer-Product Matrix → Cosine Similarity → Product Recommendations
        """)
    
    st.write("")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="module-card">
                <h2>🧩 Customer Segment Predictor</h2>
                <p>Enter a customer's Recency, Frequency, and Monetary values
                to predict which segment they belong to.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Open Segment Predictor",
            on_click=go_to,
            args=("segment",),
            use_container_width=True,
            type="primary",
        )

    with col2:
        st.markdown(
            """
            <div class="module-card">
                <h2>🔗 Product Recommender</h2>
                <p>Pick a product a customer has purchased, and get the
                top similar products based on real co-purchase patterns.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Open Product Recommender",
            on_click=go_to,
            args=("recommender",),
            use_container_width=True,
            type="primary",
        )
        
    st.divider()

    st.caption(
    """
    <div style='text-align:center; color:#888888; padding:5px;'>

    <b>Shopper Spectrum</b><br>

    Customer Segmentation & Product Recommendation System<br><br>

    Built using K-Means Clustering, Collaborative Filtering, Streamlit,
    and the UCI Online Retail Dataset.

    </div>
""",
unsafe_allow_html=True
    )



# ----------------------------------------------------------------------------
# Router
# ----------------------------------------------------------------------------
if st.session_state.view == "home":
    render_home()
elif st.session_state.view == "segment":
    render_segment_predictor(artifacts, go_to)
elif st.session_state.view == "recommender":
    render_recommender(
        artifacts,
        go_to
    )