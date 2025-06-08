# Cryptocurrency Data Analysis Pipeline
## Real-time Market Intelligence Platform

### 🚀 Key Features
- **Real-time Data Collection**: Automated fetching from CoinGecko API
- **ML-Powered Data Cleaning**: Intelligent anomaly detection for data quality
- **Automated ETL Pipeline**: Scheduled data processing every 30 seconds
- **Interactive Dashboard**: Real-time visualization of market insights

### 💡 Core Components
1. **Data Collection**
   - Fetches 20,000 cryptocurrency records every minute
   - Stores in MongoDB for historical analysis

2. **ML Data Cleaning**
   - Uses Isolation Forest for anomaly detection
   - Automatically identifies and handles data quality issues

3. **ETL Pipeline**
   - Processes 30 days of historical data
   - Generates comprehensive market analysis
   - Updates every 30 seconds

4. **Analysis Features**
   - Market Cap Analysis
   - Price Change Tracking
   - Supply Metrics
   - Top Performers Identification

### 🛠️ Technical Stack
- **Backend**: Python, Flask
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Database**: MongoDB
- **Containerization**: Docker & Docker Compose
- **Scheduling**: APScheduler

### 📊 Dashboard Access
```
http://localhost:8080
```

*Built for MADSC301 Business Intelligence Course* 