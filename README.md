# 📱 PhonePe Transaction Insights

An end-to-end Data Analysis project that analyzes PhonePe transaction 
data across India using Python, SQL and Streamlit.

This project was completed during my AIML Internship at Labmentix.

---

## 📌 About

PhonePe is one of India's leading digital payment platforms processing 
billions of transactions every day across 36 states and union territories. 
This project analyzes **real transaction data from 2018 to 2024** to 
uncover meaningful insights about payment behavior, user engagement 
and insurance growth.

The project uses **data extraction, SQL analysis, Python visualization 
and an interactive Streamlit dashboard** to present findings.

---

## 📊 Dataset

Data Source: PhonePe Pulse GitHub Repository
```
https://github.com/PhonePe/pulse
```

Clone this repository to get the data:
```
git clone https://github.com/PhonePe/pulse.git
```

The dataset contains 9 tables across 3 categories:
```
Aggregated Tables  →  State level transaction, user and insurance data
Map Tables         →  District level transaction, user and insurance data  
Top Tables         →  Top performing districts and pin codes
```

---

## 🔍 Project Workflow

The project follows a complete data analysis pipeline:

- Data Extraction from JSON files using Python
- Data Cleaning (state names, district names, formatting)
- Loading data into MySQL database
- Exploratory Data Analysis (EDA) with 20+ visualizations
- SQL queries and Business Case Studies
- Interactive Streamlit Dashboard development

---

## 📈 Key Findings

- PhonePe transactions grew from near zero in 2018 to 10000 Crore in 2024
- Total transaction amount crossed 130 Lakh Crore rupees
- Maharashtra leads in registered users with 110 Crore users
- Telangana leads in total transaction amount at 40 Lakh Crore
- Bengaluru Urban is the top district with 20 Lakh Crore transactions
- Q4 is the busiest quarter due to festive season at 30% of annual transactions
- COVID 2020 was the major turning point for digital payment adoption

---

## 🗄️ SQL Analysis

- MySQL database with 9 tables loaded using SQLAlchemy
- 5 Basic SQL queries for data analysis
- 5 Business Case Studies with SQL queries and visualizations:
  - Business Case 1 → Transaction Dynamics Analysis
  - Business Case 2 → User Engagement and Growth Strategy
  - Business Case 3 → Insurance Penetration Analysis
  - Business Case 4 → Transaction Analysis Across Districts
  - Business Case 5 → User Registration Analysis

---

## 📱 Streamlit Dashboard

An interactive dashboard with 5 pages:
```
🏠 Home            →  Key metrics and overview charts
💳 Transactions    →  Transaction type and state analysis
👥 Users           →  User registration and engagement
🛡️ Insurance       →  Insurance growth and penetration
🗺️ Districts       →  District level analysis
```

Features:
- Filter by Year, Quarter and State
- Real time chart updates based on filters
- Connected to MySQL database

---

## ▶️ How to Run the Project

Before running, make sure MySQL is installed and running on your system.

**Step 1 - Clone PhonePe data:**
```
git clone https://github.com/PhonePe/pulse.git
```

**Step 2 - Install required libraries:**
```
pip install pandas numpy matplotlib seaborn plotly streamlit sqlalchemy pymysql mysql-connector-python jupyter
```

**Step 3 - Open and run the notebook:**
```
Sample_EDA_Submission_Template.ipynb
```
Run all cells sequentially from top to bottom.

**Step 4 - Run the Streamlit dashboard:**
```
streamlit run phonepe_dashboard.py
```

---

## 📁 Files in This Repository
```
Sample_EDA_Submission_Template.ipynb  →  Main EDA and SQL notebook
phonepe_dashboard.py                  →  Streamlit dashboard
README.md                             →  Project documentation
```

---

## 🛠️ Tools and Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- MySQL
- SQLAlchemy
- Streamlit
- Jupyter Notebook

---

## 🧠 Skills Demonstrated

- Data Extraction from JSON files
- SQL Database design and querying
- Exploratory Data Analysis
- Data Visualization
- Dashboard Development
- Business Case Analysis

---

## 👨‍💻 Developed By

**Abhishek Yadav**

📧 For queries or collaboration:
abhishek.y1753@gmail.com

---

⭐ If you found this project useful, consider starring the repository.
