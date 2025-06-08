<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/ktechhub/doctoc)*

<!---toc start-->

* [Cryptocurrency Data Analysis Pipeline](#cryptocurrency-data-analysis-pipeline)
  * [Features](#features)
  * [Project Structure](#project-structure)
  * [Data Analysis Components](#data-analysis-components)
    * [1. Market Cap Analysis](#1-market-cap-analysis)
    * [2. Price Analysis](#2-price-analysis)
    * [3. Supply Analysis](#3-supply-analysis)
    * [4. Top Performers Analysis](#4-top-performers-analysis)
  * [Installation](#installation)
* [MongoDB connection](#mongodb-connection)
  * [Usage](#usage)
    * [Data Fetching](#data-fetching)
    * [ETL Analysis](#etl-analysis)
  * [Output](#output)
  * [Analysis Results Structure](#analysis-results-structure)
  * [Contributing](#contributing)
  * [License](#license)

<!---toc end-->

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
# Cryptocurrency Data Analysis Pipeline

This project implements a complete ETL/ELT pipeline for cryptocurrency market data analysis, meeting the requirements for the MADSC301 Business Intelligence course. It demonstrates end-to-end data workflow skills from data collection to analysis and visualization.

## Features

- Data Collection from CoinGecko API
- Data Cleaning & Preparation with Pandas/NumPy
- MongoDB Storage with logical schema
- Automated ETL Pipeline with Scheduler
- Data Analysis & Visualization with plotly
- Containerization with Docker and Docker Compose
- Virtual Environment Management
- Notification System for Pipeline Status

## Project Structure

```
.
├── analysis.ipynb
├── app
│   ├── __init__.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── config.py
│   ├── data
│   │   ├── __init__.py
│   │   ├── extract.py
│   │   └── store.py
│   ├── etl
│   │   ├── __init__.py
│   │   ├── extract.py
│   │   ├── load.py
│   │   ├── pipeline.py
│   │   └── transform.py
│   ├── main.py
│   ├── ml
│   │   ├── __init__.py
│   │   ├── data_cleaner.py
│   │   └── models
│   │       └── data_cleaner.joblib
│   ├── scheduler
│   │   ├── __init__.py
│   │   └── tasks.py
│   ├── storage
│   │   ├── __init__.py
│   │   └── mongo.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── email.py
│   └── visualization
│       ├── dashboards.py
│       └── graphs.py
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── tests
    ├── __init__.py
```

## Data Analysis Components

The ETL pipeline performs several types of analysis on the cryptocurrency data:

### 1. Market Cap Analysis
- Total market capitalization across all cryptocurrencies
- Top 10 cryptocurrencies by market cap
- Market cap distribution statistics (mean, median, standard deviation)
- Market cap concentration analysis
- Market cap trends over time

### 2. Price Analysis
- 24-hour price change statistics
- Most volatile cryptocurrencies (top 5 gainers and losers)
- Price change distribution
- Average price movement across the market
- Price correlation analysis between major cryptocurrencies

### 3. Supply Analysis
- Supply utilization metrics (circulating vs total supply)
- Cryptocurrencies with highest and lowest supply utilization
- Supply distribution analysis
- Supply impact on market cap
- Supply growth trends

### 4. Top Performers Analysis
- Top cryptocurrencies by market cap
- Top cryptocurrencies by trading volume
- Top cryptocurrencies by price change
- Performance metrics across different timeframes
- Historical performance comparison

## Installation & Running

### Manual
1. Clone the repository
2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start the dashboard
```bash
python -m app.main --mode dashboard --port 8080
```

### With Docker and DockerCompose
```bash
docker compose build
docker compose up -d
```
or
```bash
docker compose up --build
```

## Usage

```bash
usage: main.py [-h] [--mode {fetch,etl,dashboard}] [--pages PAGES] [--per-page PER_PAGE] [--delay DELAY] [--days DAYS] [--debug] [--port PORT]

Cryptocurrency Data Pipeline

options:
  -h, --help            show this help message and exit
  --mode {fetch,etl,dashboard}
                        Operation mode
  --pages PAGES         Number of pages to fetch
  --per-page PER_PAGE   Items per page to fetch
  --delay DELAY         Delay between requests
  --days DAYS           Days of data to process
  --debug               Run in debug mode
  --port PORT           Port for dashboard
```

### Data Collection and ETL

The application provides two main operations: data fetching and ETL analysis.

#### Data Fetching

Fetch cryptocurrency data from CoinGecko:

```bash
python -m app.main --mode fetch --pages 5 --per-page 50 --delay 2
```

Options:
- `--pages`: Number of pages to fetch (default: 10)
- `--per-page`: Number of items per page (default: 100)
- `--delay`: Delay between requests in seconds (default: 1)

#### ETL Analysis

Run the ETL pipeline for data analysis:

```bash
python -m app.main --mode etl --days 1
```

Options:
- `--days`: Number of days of historical data to analyze (default: 1)

### Data Visualization

Access the visualization dashboard:

1. Start the visualization server:
```bash
python -m app.main --mode dashboard --debug --port 8080
```

2. Open http://localhost:8080 in your browser

## Output

The ETL pipeline generates analysis results in multiple formats:

1. MongoDB Storage:
   - Results are stored in the `analysis_results` collection
   - Each analysis run is timestamped
   - Historical analysis data is preserved

2. Visualization Dashboard:
   - Interactive charts and graphs
   - Real-time data updates
   - Customizable views and filters

## Analysis Results Structure

```json
{
    "market_cap_analysis": {
        "total_market_cap": 1234567890,
        "top_10_market_cap": 987654321,
        "market_cap_distribution": {
            "mean": 1234567,
            "median": 987654,
            "std": 123456
        }
    },
    "price_analysis": {
        "avg_price_change_24h": 2.5,
        "most_volatile": [...],
        "least_volatile": [...]
    },
    "supply_analysis": {
        "avg_supply_utilization": 0.75,
        "highest_utilization": [...],
        "lowest_utilization": [...]
    },
    "top_performers": {
        "by_market_cap": [...],
        "by_volume": [...],
        "by_price_change": [...]
    }
}
```

## Notification System

The pipeline includes a notification system that sends alerts for:
- Pipeline failures
- Data quality issues
- Significant market changes
- Scheduled maintenance

Configure notifications in `.env`:
```bash
NOTIFICATION_EMAIL=your@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.