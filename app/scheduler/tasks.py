from apscheduler.schedulers.background import BackgroundScheduler
from app.etl.pipeline import run_etl_pipeline
from app.data.extract import fetch_and_store_data


def schedule_tasks():
    """
    Initialize and configure the scheduler with ETL and data fetching tasks.

    Returns:
        BackgroundScheduler: Configured scheduler instance
    """
    scheduler = BackgroundScheduler()

    # Define tasks with their schedules
    tasks = [
        {
            "task": fetch_and_store_data,
            "trigger": "interval",
            "seconds": 60,  # Fetch new data every minute
            "kwargs": {"pages": 20, "per_page": 1000, "delay": 1},
        },
        {
            "task": run_etl_pipeline,
            "trigger": "interval",
            "seconds": 30,  # Run ETL pipeline every minute
            "kwargs": {"days": 30},  # Process last day's data
        },
    ]

    # Register the tasks with the scheduler
    for task in tasks:
        scheduler.add_job(
            task["task"],
            task["trigger"],
            **{
                k: v
                for k, v in task.items()
                if k not in ["task", "trigger", "args", "kwargs"]
            },
            args=task.get("args", []),
            kwargs=task.get("kwargs", {})
        )

    scheduler.start()
    print("Scheduler started with ETL and data fetching tasks.")

    return scheduler
