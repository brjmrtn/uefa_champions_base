# UEFA Champions Base

This repository contains a Django project to manage predictions for the UEFA Champions League and a small Spark pipeline to process exported data.

## Setup

1. **Create a virtual environment** and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install django pandas pyspark
   ```
2. **Environment variables**: copy `.env.example` to `.env` and edit the values as needed.
   ```bash
   cp .env.example .env
   # edit .env to provide your DJANGO_SECRET_KEY
   ```
   Load the variables in your shell before running Django:
   ```bash
   export $(grep -v '^#' .env | xargs)
   ```
3. **Apply migrations** to create the local SQLite database:
   ```bash
   python manage.py migrate
   ```

## Running the development server

Start the Django development server with:
```bash
python manage.py runserver
```
It will listen on `http://127.0.0.1:8000/` by default.

## Spark pipeline

Data for the Spark job is created with the management command `export_data` which writes Parquet files into the `data/` folder:
```bash
python manage.py export_data
```
After exporting the data you can execute the Spark pipeline:
```bash
python spark_jobs/pipeline.py
# or use spark-submit spark_jobs/pipeline.py
```
The pipeline will read the Parquet inputs and create `data/training.parquet`.
