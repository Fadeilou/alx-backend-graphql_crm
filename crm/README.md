# CRM Celery Setup

This document provides instructions on how to set up and run the Celery tasks for the CRM application.

## Prerequisites

- Redis must be installed and running.
- All Python dependencies must be installed from `requirements.txt`.

## Setup Instructions

1.  **Install Redis and Dependencies:**
    ```bash
    # On Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install redis-server

    # Install python dependencies
    pip install -r requirements.txt
    ```

2.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

3.  **Start the Celery Worker:**
    ```bash
    celery -A alx_backend_graphql worker -l info
    ```

4.  **Start the Celery Beat Scheduler:**
    ```bash
    celery -A alx_backend_graphql beat -l info
    ```

5.  **Verify Logs:**
    After the scheduled time, you can check the logs in the following files:
    - `/tmp/crm_report_log.txt`
