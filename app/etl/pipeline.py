from app.etl.extract import extract_crypto_data
from app.etl.transform import transform_data
from app.etl.load import save_analysis_results
from app.utils.email import send_email


def run_etl_pipeline(days: int = 1):
    """
    Run the ETL pipeline for data analysis.

    Args:
        days: Number of days of historical data to analyze
    """
    try:
        print(f"Starting ETL pipeline for last {days} days...")

        # Extract
        print("Extracting data from MongoDB...")
        df = extract_crypto_data(days=days)
        print(f"Extracted {len(df)} records")
        print(f"df: {df.head(1)}")

        # Transform
        print("Transforming and analyzing data...")
        analysis_results = transform_data(df)
        print(f"analysis_results: {analysis_results}")

        # Load
        print("Saving analysis results to MongoDB...")
        save_analysis_results(analysis_results)

        # Send email
        print("Sending email...")
        send_email(
            subject="ETL pipeline completed successfully!",
            body=f"ETL pipeline completed successfully! {analysis_results}",
        )
        print("ETL pipeline completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        send_email(
            subject="ETL pipeline failed!",
            body=f"ETL pipeline failed! {e}",
        )
