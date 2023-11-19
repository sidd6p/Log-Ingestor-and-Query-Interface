# Log-Ingestor-and-Query-Interface



### Running the Application
To run the application, execute the 
`python -m log_ingestor_package.rabbitmq_consumer`
`uvicorn log_ingestor_query_backend:app --host 0.0.0.0 --port 3000 --workers 4 --reload`.
`streamlit run log_ingestor_query_interface.py`
### Explanation
- **`database.py`**: Manages database connection and session.
- **`models.py`**: Defines the database models (tables).
- **`schemas.py`**: Defines Pydantic schemas for request validation and response serialization.
- **`crud.py`**: Contains functions for database interactions.
- **`config.py`**: Reserved for future configuration settings.
- **`test_log_ingestor.py`**: The test file for the FastAPI application.
- **`log_ingestor.py`**: The entry point for the FastAPI application.

### Note
- In a larger application, you might further refine this structure, separating endpoints into different files or organizing CRUD operations more granularly.
- Remember to adjust import statements as needed, depending on your project structure. If you place these files in a package, you'll need to adjust the imports accordingly.
