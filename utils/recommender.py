import pandas as pd


def get_product_choices(stockcode_to_desc: dict):
    """
    Creates user-friendly dropdown options.

    Returns:
        dict:
        {
            "WHITE HANGING HEART T-LIGHT HOLDER (85123A)": "85123A"
        }
    """
    options = {}

    for stockcode, desc in stockcode_to_desc.items():
        label = f"{desc.strip()} ({stockcode})"
        options[label] = stockcode

    return dict(sorted(options.items()))


def get_recommendations(
    stockcode: str,
    similarity_matrix: pd.DataFrame,
    stockcode_to_desc: dict,
    top_n: int = 10,
):
    """
    Returns top N similar products.
    """

    if stockcode not in similarity_matrix.index:
        return []

    scores = similarity_matrix.loc[stockcode]

    recommendations = (
        scores
        .sort_values(ascending=False)
        .iloc[1 : top_n + 1]
    )

    results = []

    for rec_code, similarity in recommendations.items():
        results.append(
            {
                "stockcode": rec_code,
                "description": stockcode_to_desc.get(
                    rec_code,
                    "Unknown Product"
                ),
                "similarity": similarity,
            }
        )

    return results