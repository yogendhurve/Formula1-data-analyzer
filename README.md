# 🏎️ F1 Data Platform

[![Built with dbt](https://img.shields.io/badge/Built%20with-dbt-orange.svg)](https://www.getdbt.com/)
[![Tech Stack](https://img.shields.io/badge/Stack-Python%20%7C%20PostgreSQL-blue)](https://www.python.org/)

A production-ready **Formula 1 analytics pipeline** built on a modern ELT (Extract, Load, Transform) stack using **Python**, **dbt (data build tool)**, and **PostgreSQL**.

This platform reliably ingests F1 race data from the Jolpica Ergast API, transforms it through a layered dbt architecture, and provides optimized, analytics-ready data models for deep race strategy insights.

---

## 🧭 Table of Contents

* [✨ Features](#-features)
* [🏗️ Architecture](#-architecture)
* [🚀 Quick Start](#-quick-start)
* [💾 Data Models](#-data-models)
* [🛠️ Development & Testing](#%e2%9a%92%ef%b8%8f-development--testing)
* [🔭 Future Scope](#-future-scope)
* [🙏 Acknowledgments](#-acknowledgments)

---

## ✨ Features

This project is built to be robust, professional, and analytically powerful:

* **Robust Data Ingestion:** Implements **auto-retry logic** (exponential backoff) and **rate limiting** to ensure reliable data collection from the API.
* **Professional Architecture:** Uses a **modular Python package** (`f1_pipeline/`) for clear separation of concerns in the Extract & Load (E&L) phase.
* **Layered dbt Transformations:** Follows a strict **Staging → Intermediate → Marts** layered approach for traceable, maintainable, and progressive analytical modeling.
* **Data Quality Assurance:** Comprehensive data quality checks implemented via **dbt testing** across all layers.
* **Race Analytics Focus:** Produces models tailored for **driver performance**, **tire stint analysis**, **pit stop strategy**, and **lap time degradation**.

---

## 🏗️ Architecture

## Architecture

```
f1-data-platform/
├── f1_pipeline/                    # Core ingestion package
│   ├── config/                     # Configuration management
│   ├── ingestion/                  # API client, data transformation, orchestration
│   └── utils/                      # Database utilities
├── scripts/                        # Execution scripts
├── models/                         # dbt transformation layer
│   ├── staging/                    # Raw data cleaning
│   ├── intermediate/               # Business logic calculations
│   └── marts/                      # Summary datasets for analytics
│   └── analytics/                  # Strategic insights and performance metrics
├── macros/                         # dbt SQL utilities
└── tests/                          # Data quality tests
```
The pipeline separates data ingestion (Python) from data transformation (dbt/SQL), with **PostgreSQL** serving as the centralized data warehouse.

### **Project Structure**

## **Key Python Components**

| Component | Path | Function |
| :--- | :--- | :--- |
| **API Client** | `f1_pipeline/ingestion/api_client.py` | Handles all HTTP requests with exponential backoff retry logic. |
| **Data Transformer** | `f1_pipeline/ingestion/data_transformer.py` | Converts nested JSON to structured DataFrames. |
| **Orchestrator** | `f1_pipeline/ingestion/orchestrator.py` | Coordinates multi-season data collection workflows. |
| **Database Utilities** | `f1_pipeline/utils/` | Manages PostgreSQL connections and table operations. |

---

## 🚀 Quick Start

Follow these steps to set up the data platform locally and run the pipeline end-to-end.

### **Prerequisites**

* **PostgreSQL** (local instance or Docker)
* **Python 3.10+** (Conda/venv recommended)
* **dbt**

### **Installation & Configuration**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yogendhurve/formula1-data-analyzer](https://github.com/yogendhurve/formula1-data-analyzer)
    cd f1-data-platform
    ```

2.  **Setup Environment & Dependencies:**
    ```bash
    # Create and activate environment
    conda create -n f1-data-platform python=3.11
    conda activate f1-data-platform
    
    # Install Python and dbt dependencies
    pip install -r requirements.txt
    pip install -e . # For development
    dbt deps
    ```

3.  **Database and Environment Setup:**
    ```sql
    -- Create the target database in PostgreSQL
    CREATE DATABASE f1_analytics;
    ```
    ```bash
    # Configure environment variables
    cp .env.example .env
    # Edit .env with your PostgreSQL credentials (DB_USER, DB_PASSWORD, etc.)
    ```

    
### Configuration

Create a `.env` file in the project root:

```env
API_BASE_URL=http://api.jolpi.ca/ergast
DB_HOST=localhost
DB_PORT=5432
DB_NAME=f1_analytics
DB_USER=your_username
DB_PASSWORD=your_password
```

### **Usage**

The pipeline runs in two simple steps: Ingestion (Python) and Transformation (dbt).

1.  **Run Data Ingestion (E&L):** Fetches data from the Ergast API and loads it into your PostgreSQL raw tables.
    ```bash
    python scripts/ingest_f1_data.py
    ```

2.  **Run dbt Transformations (T):** Executes all SQL models (`dbt run`), building clean, intermediate, and final analytical tables.
    ```bash
    dbt run
    ```

3.  **View Analytics Data:** Connect a BI tool (like Superset) or query directly:
    ```sql
    SELECT * FROM mart_driver_race_summary LIMIT 10;
    SELECT * FROM mart_stint_degradation_summary LIMIT 10;
    ```

---

## 💾 Data Models

The dbt layer is organized for clarity and analytical depth:

### **Analytics Layer (Marts)**

These tables are the final product, optimized for reporting and analysis.

| Model Name | Analytical Focus |
| :--- | :--- |
| `mart_driver_race_summary` | Driver performance metrics by race (overall pace, pit time). |
| `mart_stint_summary` | Comprehensive analysis of every tire stint per race. |
| `mart_qualifying_consistency` | Qualifying performance patterns and lap-to-lap variance. |
| `mart_session_progression` | Session-by-session performance tracking. |

### **Intermediate Layer**

These models contain calculated business logic:

* `int_stint_segmentation`: Tire stint identification and analysis.
* `int_driver_lap_deltas`: Lap time comparisons and delta calculations.
* `int_stint_degradation`: Tire performance degradation analysis.

### **Staging Layer**

These models perform initial cleaning of raw data:

* `stg_lap_times`: Cleaned lap timing data with standardized formats.
* `stg_pit_stops`: Processed pit stop events with duration calculations.

---

## 🛠️ Development & Testing


The platform follows professional Python packaging standards with clear separation of concerns:

- **f1_pipeline/**: Core package containing all ingestion logic
- **scripts/**: Execution scripts that orchestrate workflows  
- **models/**: dbt transformation layer with staging to intermediate to marts flow
- **macros/**: Reusable SQL functions for dbt models

### Key Components

- **API Client**: Handles HTTP requests with exponential backoff retry logic
- **Data Transformer**: Converts nested JSON to structured DataFrames
- **Orchestrator**: Coordinates multi-season data collection workflows
- **Database Utilities**: Manages PostgreSQL connections and table operations

### Adding New Data Sources

1. Create new API methods in `f1_pipeline/ingestion/api_client.py`
2. Add transformation logic in `f1_pipeline/ingestion/data_transformer.py`
3. Update orchestrator to include new data types
4. Create corresponding dbt staging models

### **Performance Metrics**

The platform is designed for efficiency:

* **Ingestion Rate**: ~4 requests/second (API limit compliant).
* **Data Volume**: Handles 700+ lap records, 600+ pit stops per season.
* **Transformation Speed**: Complete dbt run typically in under 2 seconds.

### **Testing Methodology**

Data quality is enforced using dbt's testing framework (`dbt test`):

* **Schema tests**: Data validation (`not null`, `unique values`, `accepted ranges`).
* **Custom tests**: Validation of complex business logic (e.g., stint segmentation logic).

#### **Running Tests**

```bash
# Run all tests
dbt test

# Run tests for specific models
dbt test --select mart_qualifying_consistency
