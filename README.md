# 🧠 AI Retail Data Analyst

An **AI-powered retail analytics assistant** built with **Python and Streamlit** that automatically cleans datasets, detects relationships, identifies KPIs, generates charts, and produces business insights.

The tool simulates the workflow of a **data analyst**, turning raw datasets into **actionable insights with minimal manual work**.

---

# 🚀 Live Demo

*(Add after deployment)*

```
https://ai-retail-data-analyst.onrender.com
```

---

# 📊 Features

### Automated Data Processing

* Smart dataset ingestion (CSV / Excel)
* Data profiling
* Issue detection
* Automated data cleaning
* Duplicate removal
* Missing value handling
* Outlier detection

---

### Intelligent Dataset Analysis

* Automatic **relationship detection between tables**
* Smart **auto join engine**
* Dataset normalization
* Human-like data cleaning logic

---

### Calculated Column Builder

Create new features using formulas such as:

```
price * quantity
price * quantity - discount
round(price * quantity,2)
sqrt(price)
```

Useful for generating:

* Revenue
* Profit
* Margin
* Derived metrics

---

### Automated KPI Detection

The system automatically identifies key business metrics such as:

* Revenue
* Sales
* Profit
* Price
* Amount

---

### AI Chart Builder

Generates **Top 10 most relevant charts automatically**.

Charts are selected based on:

* column importance
* variance
* categorical relevance

Includes:

* bar charts
* time series
* aggregated insights

---

### AI Insight Engine

The system generates natural-language insights such as:

```
Electronics contributes the highest revenue ($1.8M),
while Office Supplies contributes the least.
```

---

### AI Data Story

Automatically generates a narrative explaining the dataset:

Example:

```
• Dataset contains 125,000 records
• Total revenue is $4.2M
• Electronics contributes the highest revenue
• Revenue shows an increasing trend over time
```

---

### Root Cause Analysis

Explains **drivers behind KPI changes**.

Example:

```
Region: United States drives the highest revenue
Category: Electronics is the main revenue contributor
```

---

### Anomaly Detection

Detects unusual patterns in the data.

Example:

```
Revenue shows a significant spike in July
Revenue dropped sharply in March
```

---

# 🧱 Architecture

```
Upload Data
      ↓
Data Profiling
      ↓
Issue Detection
      ↓
AI Data Cleaning
      ↓
Relationship Detection
      ↓
Auto Join Engine
      ↓
Calculated Column Builder
      ↓
KPI Detection
      ↓
Chart Builder
      ↓
AI Insights
      ↓
Root Cause Analysis
      ↓
Anomaly Detection
```

---

# 🛠 Tech Stack

**Languages**

* Python

**Libraries**

* Streamlit
* Pandas
* NumPy
* Plotly
* DuckDB
* Scikit-learn

**Concepts**

* Automated analytics
* Data cleaning pipelines
* Feature engineering
* Exploratory data analysis
* Insight generation
* Business intelligence automation

---

# 📂 Project Structure

```
ai-retail-data-analyst/
│
├── app.py
├── requirements.txt
├── runtime.txt
│
├── models/
│   └── dataset_context.py
│
├── modules/
│   ├── anomaly_engine.py
│   ├── column_logic_engine.py
│   ├── data_cleaner.py
│   ├── data_profiler.py
│   ├── file_loader.py
│   ├── issue_detector.py
│   ├── join_engine.py
│   ├── pipeline_engine.py
│   ├── relationship_detector.py
│   ├── root_cause_engine.py
│   ├── story_engine.py
│   └── visualization_engine.py
```

---

# ⚙️ Installation (Local)

Clone the repository:

```
git clone https://github.com/amolcrasta/ai-retail-data-analyst.git
```

Navigate to the project:

```
cd ai-retail-data-analyst
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the app:

```
streamlit run app.py
```

---

# 📈 Future Improvements

Potential enhancements:

* Natural language queries
  *(“Show revenue by region”)*

* LLM-powered insight generation

* Predictive analytics

* Automated dashboard recommendations

---

# 👨‍💻 Author

**Amol Crasta**

MBA – Big Data Management
Aspiring Data Analyst / Analytics Engineer

GitHub:

```
https://github.com/amolcrasta
```
