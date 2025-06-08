# app/main.py
import argparse
import subprocess
import signal
import sys

from app.data.extract import fetch_and_store_data
from app.etl.pipeline import run_etl_pipeline
from app.visualization.dashboards import run_dashboard_server
from app.scheduler.tasks import schedule_tasks


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\nShutting down scheduler...")
    if "scheduler" in globals():
        scheduler.shutdown()
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Cryptocurrency Data Pipeline")
    parser.add_argument(
        "--mode",
        choices=["fetch", "etl", "dashboard"],
        default="dashboard",
        help="Operation mode",
    )
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to fetch")
    parser.add_argument(
        "--per-page", type=int, default=100, help="Items per page to fetch"
    )
    parser.add_argument("--delay", type=int, default=1, help="Delay between requests")
    parser.add_argument("--days", type=int, default=1, help="Days of data to process")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--port", type=int, default=8080, help="Port for dashboard")

    args = parser.parse_args()

    if args.mode == "fetch":
        fetch_and_store_data(pages=args.pages, per_page=args.per_page, delay=args.delay)
    elif args.mode == "etl":
        run_etl_pipeline(days=args.days)
    elif args.mode == "dashboard":
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start the scheduler
        global scheduler
        scheduler = schedule_tasks()

        # Run the dashboard
        run_dashboard_server(debug=args.debug, port=args.port)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

"""
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
  
  
Example:

# Dashboard
python -m app.main --mode dashboard --debug --port 8051

# ETL
python -m app.main --mode etl --days 1

# Fetch
python -m app.main --mode fetch --pages 5 --per-page 50 --delay 2
"""
