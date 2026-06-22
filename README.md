# 🛍️ Shopper Spectrum

### Customer Segmentation & Product Recommendation System

Shopper Spectrum is an end-to-end Machine Learning application that transforms raw retail transaction data into actionable business insights through:

- 🎯 **Customer Segmentation using K-Means Clustering**
- 🛒 **Product Recommendations using Item-Based Collaborative Filtering**
- 📊 **Interactive Streamlit Dashboard**
- 📈 **RFM-Based Customer Analytics**

Built using the UCI Online Retail Dataset, the project helps businesses identify valuable customer segments, understand purchasing behavior, and generate personalized product recommendations.

---

## 🚀 Live Features

### 🎯 Customer Segment Predictor

Predicts customer segments based on:

- Recency (Days since last purchase)
- Frequency (Number of purchases)
- Monetary Value (Total spend)

Generated segments:

| Segment | Description |
|----------|-------------|
| High-Value | Most valuable and loyal customers |
| Regular | Consistent repeat customers |
| Occasional | Infrequent but active customers |
| At-Risk | Customers showing signs of churn |

Additional insights:

- Segment-specific business actions
- Customer vs Segment comparison
- Segment profile benchmarking
- Model details and performance metrics

---

### 🛒 Product Recommender

Generates personalized product recommendations using:

- Item-Based Collaborative Filtering
- Customer purchase co-occurrence patterns
- Cosine Similarity

Features:

- Product search
- Adjustable recommendation count
- Similarity score visualization
- Recommendation explanations
- Model performance details

---

## 📊 Dataset

### Source

UCI Online Retail Dataset

### Dataset Overview

| Metric | Value |
|---------|---------|
| Transactions | 391,150+ |
| Customers | 4,334 |
| Products | 3,148 |
| Countries | 38 |
| Period | Dec 2010 – Dec 2011 |

The dataset contains transactional records from a UK-based online retailer selling gift and home décor products.

---

## 🧹 Data Preprocessing

The raw dataset underwent extensive cleaning:

- Removed missing Customer IDs
- Removed cancelled invoices
- Removed invalid quantities and prices
- Removed duplicate transactions
- Removed non-product entries (postage, bank charges)
- Generated clean customer-product purchase matrix

Final dataset retained approximately **72%** of original records while ensuring high data quality.

---

## 📈 Exploratory Data Analysis

Key insights discovered:

- Strong UK market dominance
- Clear weekday/business-hour purchasing patterns
- Significant customer value concentration
- Strong seasonality with holiday spikes
- Heavy right-skew in customer spending behavior
- High-value customer "whales" driving disproportionate revenue

A total of **15 visualizations** and **3 statistical hypothesis tests** were performed before model development.

---

## 🎯 Customer Segmentation Model

### Feature Engineering

RFM Framework:

- **Recency** → Days since last purchase
- **Frequency** → Number of invoices
- **Monetary** → Total customer spend

### Preprocessing

- Log Transformation (`log1p`)
- Standard Scaling (`StandardScaler`)

### Algorithm

```python
KMeans(n_clusters=4)
```

### Model Performance

| Metric | Value |
|---------|---------|
| Clusters | 4 |
| Silhouette Score | 0.338 |

### Final Customer Segments

| Segment | Share |
|----------|----------|
| High-Value | 15.8% |
| Regular | 27.2% |
| Occasional | 19.3% |
| At-Risk | 37.7% |

---

## 🛒 Recommendation Engine

### Algorithm

Item-Based Collaborative Filtering

### Similarity Metric

```python
Cosine Similarity
```

### Improvements Applied

- Binary purchase matrix
- Popularity-bias correction
- Minimum support filtering
- Product similarity optimization

### Performance

| Metric | Value |
|---------|---------|
| Precision@10 | 0.107 |
| Hit Rate@10 | 0.61 |

Compared to a popularity baseline, the recommender achieved:

- ~6× higher Precision@10
- ~4× higher Hit Rate

---

## 🏗️ Project Structure

```text
ShopperSpectrum/
│
├── app.py
│
├── models/
│   ├── kmeans_model.pkl
│   ├── rfm_scaler.pkl
│   ├── cluster_name_map.pkl
│   ├── item_similarity_matrix.pkl
│   └── stockcode_to_description.pkl
│
├── pages_content/
│   ├── segment_predictor.py
│   └── recommender.py
│
├── utils/
│   ├── data_loader.py
│   ├── segmentation.py
│   └── recommender.py
│
├── assets/
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/shopper-spectrum.git

cd shopper-spectrum
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Locally

```bash
streamlit run app.py
```

Application will launch at:

```text
http://localhost:8501
```

---

## ☁️ Streamlit Deployment

### 1. Push Repository to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Deploy on Streamlit Community Cloud

1. Visit https://share.streamlit.io
2. Sign in with GitHub
3. Select repository
4. Set:

```text
Main file path:
app.py
```

5. Click **Deploy**

---

## 🛠️ Technologies Used

### Programming

- Python

### Machine Learning

- Scikit-Learn
- K-Means Clustering
- Hierarchical Clustering
- Collaborative Filtering

### Data Processing

- Pandas
- NumPy

### Visualization

- Matplotlib
- Seaborn

### Deployment

- Streamlit
- Joblib

---

## 📌 Future Improvements

- Hybrid recommendation system
- Seasonal recommendations
- Real-time customer scoring
- Customer Lifetime Value prediction
- Advanced churn prediction
- Recommendation explainability enhancements

---

## 👨‍💻 Author

**Vivek Rupapara**

Machine Learning Engineer Aspirant

- GitHub: https://github.com/VivekRupapara146

---

## ⭐ If you found this project useful, consider starring the repository.