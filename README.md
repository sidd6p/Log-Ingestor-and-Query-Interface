# Log-Ingestor-and-Query-Interface

### Overview
This project provides a robust system for ingesting, storing, and querying log data. It consists of two main components:

- Log Ingestor: A FastAPI application that ingests log data and stores it using RabbitMQ in a PostgreSQL database and indexes it in Elasticsearch for efficient querying.
- Query Interface: An interface for querying the ingested logs using various filters and full-text search capabilities.

### Features
- Efficient log ingestion over HTTP.
- Full-text search capabilities with Elasticsearch.
- Query interface with support for various filters.
- RabbitMQ integration for asynchronous processing.
- Combination of PostgreSQL and Elasticsearch for efficient storage and search capabilities
- Scalable architecture suitable for handling large volumes of log data.


### Technology Stack
- Backend: Python, FastAPI
- Database: PostgreSQL, Elasticsearch
- Message Broker: RabbitMQ
- Frontend (optional for Web UI): Streamlit or similar


### Installation


#### Prerequisites

- Python 3.8 or higher
- PostgreSQL running on localhost on port 5432, or provides correct URL in .env file.
- There should be a database named "log_ingestor_package_db" on PostgreSQL
- Elasticsearch running on localhost on port 9200, or provides correct URL in .env file
- RabbitMQ running on localhost, or provides correct URL in .env file


#### Running the Application

Clone the repo:

`git clone https://github.com/dyte-submissions/november-2023-hiring-sidd6p.git`

Navigate to the repo:

`cd november-2023-hiring-sidd6p`

Installation of python packages

`pip install -r requirements.txt`

Run the RabbitMQ consumer 

`python -m log_ingestor_package.rabbitmq_consumer`

Run the FastAPI Endpoints

`uvicorn log_ingestor_query_backend:app --host 0.0.0.0 --port 3000 --workers 4 --reload`.

Run streamlit Frontend

`streamlit run log_ingestor_query_interface.py`


### File Descriptions

#### 1. `log_ingestor_query_backend.py`
- **Purpose**: Main file for the FastAPI application, setting up the HTTP server and API endpoints.
- **Key Functions**:
  - Ingestion endpoint (`/ingest`): Processes log data.
  - Search endpoint (`/search`): Handles queries on logs.

#### 2. `log_ingestor_query_interface.py`
- **Purpose**: Contains code for a potential Streamlit-based web interface.
- **Key Functions**:
  - User interface for ingesting and querying logs.

#### 3. `config.py`
- **Purpose**: Manages configuration settings using environment variables.
- **Key Functions**:
  - Defines settings like database connections and Elasticsearch configuration.

#### 4. `crud.py`
- **Purpose**: Contains CRUD functions for database operations.
- **Key Functions**:
  - Add and retrieve log entries from the database.

#### 5. `database.py`
- **Purpose**: Sets up the SQLAlchemy database connection.
- **Key Functions**:
  - Defines `SessionLocal` for database sessions and initializes the database engine.

#### 6. `models.py`
- **Purpose**: Defines SQLAlchemy models (table schemas).
- **Key Functions**:
  - Data structure of log entries and related models.

#### 7. `query_reader.py`
- **Purpose**: Used for parsing and handling query requests.
- **Key Functions**:
  - Parses and formats query requests.

#### 8. `rabbitmq_consumer.py`
- **Purpose**: Handles consumption of messages from RabbitMQ.
- **Key Functions**:
  - Processes asynchronous tasks related to log data.

#### 9. `rabbitmq_producer.py`
- **Purpose**: Responsible for publishing messages to RabbitMQ.
- **Key Functions**:
  - Sends messages to RabbitMQ for asynchronous processing.

#### 10. `schemas.py`
- **Purpose**: Defines Pydantic models for data validation and serialization.
- **Key Functions**:
  - Validates incoming data for API endpoints and serializes database models.
