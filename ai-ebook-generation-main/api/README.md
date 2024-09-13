# Project Template: Backend API

### 🛠️ Directory Structure

```
   api                      # API related code
    ├── Dockerfile           # Dockerfile for the API
    ├── README.md            # README for the API
    ├── __init__.py          # API package initialization
    ├── app                  # Main application package
    │   ├── __init__.py      # App package initialization
    │   ├── config.py        # Configuration file
    │   ├── data
    │   │   └── database_service.py # Database service
    │   ├── entry
    │   │   ├── __init__.py
    │   │   └── entry_service.py # All endpoints will enter here to be triaged to the appropriate path
    │   ├── health
    │   │   ├── __init__.py
    │   │   └── health_service.py # Health check service
    │   ├── routes.py        # Route definitions
    │   └── utils            # Utility functions and classes
    ├── main.py              # Main entry for running the API
    ├── requirements.txt     # Required Python packages
    ├── swagger.json         # Swagger specification
    └── tests                # Test package
        ├── __init__.py      # Test package initialization
        ├── conftest.py      # Pytest configuration
        └── test_routes.py   # Tests for the routes
```

## 🧭 How To Run

### (Local) - Current Recommended

1. ```sh
   cd api
   ```

2. ```sh
   pip3 install -r requirements.txt
   ```

3. ```sh
   python3 app.py
   ```

4. Trigger endpoints with:
   ```sh
   curl -X 'GET' \
   'http://127.0.0.1:8000/health' \
   -H 'accept: application/json'
   ```

5. Run tests with:   curl -X 'GET' \
   'http://127.0.0.1:8000/health' \
   -H 'accept: application/json'
   ```sh
   python -m pytest -p no:warnings
   ```

### Kafka
You will need to start-up a Kafka server: https://kafka.apache.org/quickstart

For this, you will need to run Zookeeper:
```sh
bin/zookeeper-server-start.sh config/zookeeper.properties
```

and the Kafka server:
```sh
bin/kafka-server-start.sh config/server.properties
```

(these happen in separate terminals)

Then, run
```sh
   python3 -m app.ai_book_generation.saas.kafka.kafka_consumer
```
to start a daemon that consumes requests from Kafka.

## CI/CD + Dev Notes

### Python Version and Code Style
- Using **Python 3.7** for development.
- Code formatting is handled by [**black**](https://black.readthedocs.io/en/stable/), a code formatter that enforces PEP 8 style guide.
- Linting is done with [**flake8**](https://flake8.pycqa.org/en/latest/), which helps to identify coding errors and maintain code quality.

### Pre-commit Hooks
- The project uses [**pre-commit**](https://pre-commit.com/) to manage and maintain pre-commit hooks.
- Run `pre-commit install` to install pre-commit formatting and linting. This ensures that every commit adheres to the code style guide and passes linting checks.
- You can manually run all pre-commit hooks on a repository with `pre-commit run --all-files`.
