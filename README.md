# JustIn Decision Making Algorithm API for Digital Interventions

This is the JustIn Template, designed for deploying decision-making algorithms,
such as Reinforcement Learning (RL) algorithms, in digital interventions.
The template includes a demonstration implementation using a flat fixed
probability mock RL algorithm, showcasing its structure and functionality.

The template provides a Flask-based RESTful API for seamless integration with decision-making workflows. It supports:

- Database Management with Flask-SQLAlchemy.
- Schema Migrations with Alembic.
- Endpoints for user management, action requests, data uploads, and model updates.

This template is flexible and can accommodate any decision-making algorithm by replacing the mock algorithm provided.

---

## Features

- **User Management**: Add and manage users with unique IDs.
- **Action Handling**: Request action based on user context.
- **Data Uploads**: Upload interaction data for users.
- **Model Updates**: Request the decision-making algorithm to update its model.
- **Backend Database Support**: Provides robust database management with schema migrations handled by Alembic.
- **Auto Backups Before Updates**: Ensures automatic database backups prior to algorithm updates for safety.
- **Easy Priors Setup**: Simplifies the initialization and management of algorithm priors for efficient configuration.
- **Reproducibility**: Ensures reproducibility of both the environment (via a conda environment file) and algorithm behavior (through seeding).
- **Automatic Logging**: Configures detailed logging for debugging and application monitoring.
- **Comprehensive Testing Template**: Includes a comprehensive test template for ensuring application reliability.

---

## **Project Structure**

```plaintext
JustIn_RL_API/
│
├── app/                     # Core application logic and organization.
│   ├── algorithms/          # Contains decision-making algorithm implementations, including the mock RL algorithm.
│   │   ├── base.py          # Base class for algorithms providing a standard interface.
│   │   └── flat_prob.py     # Demonstration implementation of a flat fixed probability algorithm.
│   ├── routes/              # API endpoint definitions.
│   │   ├── action.py        # Endpoints for action requests.
│   │   ├── data.py          # Endpoints for uploading user interaction data.
│   │   ├── update.py        # Endpoints for model updates.
│   │   └── user.py          # Endpoints for user management.
│   ├── models.py            # Database models defining users, actions, model parameters, and study data.
│   ├── logging_config.py    # Configures detailed logging for debugging and application monitoring.
│   └── extensions.py        # Configures Flask extensions like SQLAlchemy and migrations.
│ 
├── migrations/              # Alembic migration files
│
├── tests/                   # Comprehensive test suite for ensuring application reliability.
│   ├── conftest.py          # Shared fixtures and configurations for tests.
│   ├── test_actions.py      # Tests for the action-related routes.
│   ├── test_data.py         # Tests for data upload functionality.
│   ├── test_update.py       # Tests for model update endpoints.
│   └── test_users.py        # Tests for user management endpoints.
│
├── config.py                # Application configuration
├── run.py                   # Application entry point
├── README.md                # Documentation
└── environment.yml          # Conda environment file
```

---

## **Pre-requisites**

1. Python 3.9+ (the provided environment.yml file is for Python 3.11.1).
2. [Conda](https://docs.anaconda.com/miniconda/). python package manager - Used for managing dependencies.
3. Any DBMS software like [PostgreSQL](https://www.postgresql.org/), [SQLite](https://www.sqlite.org/), [MySQL](https://www.mysql.com/) etc.

This template utilizes PostgreSQL as the database backend.

---

## **Steps**

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/JustIn_RL_API.git
    cd JustIn_RL_API
    ```

2. **Create and activate the conda environment**:

    ```sh
    conda env create -f environment.yml
    conda activate justin_rl_api
    ```

3. **Configure the database**:
    Setup a PostgreSQL database and create a new database for the application.
    Update the database connection string in ```config.py```. For PostgreSQL, the string looks like:

    ```sh
    SQLALCHEMY_DATABASE_URI = "postgresql://<username>:<password>@<host>:<port>/<database>"
    ```

4. **Initialize the database**:

    ```sh
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. **Run the application**:

    ```sh
    flask run
    ```

    Add ```--debug``` to launch the API in debug mode.

6. **Access the API**:
    Use an API client like Postman or cURL to send requests to `http://127.0.0.1:5000/` to access the API.

---

## **Reset tables**

To reset the database tables, use ```flask reset-db```

---

## **Configurable Parameters**

The template provides several configurable parameters in the `config.py` file:

- **SQLALCHEMY_DATABASE_URI**: Database connection string.
- **SQLALCHEMY_TRACK_MODIFICATIONS**: Set to False to disable tracking modifications.
- **PRIORS_PICKLE_FILE**: Path to the file containing the priors for the decision-making algorithm. If set to
  `None`, the algorithm will use the **MODEL_PRIORS** parameter.
- **BACKUP_DATABASE**: Set to True to enable automatic database backups before model updates. The backups are
  stored in the `backups` directory.
- **RL_ALGORITHM_SEED**: Seed for the random number generator used by the decision-making algorithm.

---

## **Usage**

### **Mock requests and responses**

#### **Add User**

- **FILE** - `routes/user.py`
- **DESCRIPTION** - Add a new user with a unique user ID.
- **POST** `/api/v1/add_user`
- **Request**:

  ```json
  {
    "user_id": "test_user_123"
  }
  ```

- **Response**:

  ```json
  {
    "message": "User added successfully.",
    "status": "success",
    "user_id": "test_user_123"
  }
  ```

#### **Request Action**

- **FILE** - `routes/action.py`
- **DESCRIPTION** - Request an action for a user based on the user's context.
  Requires the user ID, timestamp, and context information.
  The mock algorithm used in the template also requires the decision time.
- **POST** `/api/v1/action`
- **Request**:

  ```json
  {
    "user_id": "test_user_123",
    "timestamp": "2025-01-01T12:00:00Z",
    "decision_idx": 0,
    "context": {
      "temperature": 23
    }
  }
  ```

- **Response**:

  ```json
  {
    "action": 1,
    "action_prob": 0.5,
    "state": [
        23
    ],
    "status": "success",
    "timestamp": "2025-01-02T03:10:14.731478",
    "user_id": "test_user_123"
  }
  ```

#### **Upload Data**

- **FILE** - `routes/data.py`
- **DESCRIPTION** - Upload interaction data for a user. The data includes the user ID,
  timestamp, outcome and other relevant information for the decision-making algorithm.
- **POST** `/api/v1/upload_data`
- **Request**:

  ```json
  {
    "user_id": "test_user_123",
    "timestamp": "2025-01-01T12:00:00Z",
    "decision_idx": 0,
    "data": {
      "context": {
          "temperature": 30
      },
      "action": 1,
      "action_prob": 0.5,
      "state": [
          30
      ],
      "outcome": {
          "clicks": 4
      }
    }
  }
  ```

- **Response**:

  ```json
  {
    "message": "Data uploaded successfully.",
    "status": "success"
  }
  ```

#### **Update Model**

- **FILE** - `routes/update.py`
- **DESCRIPTION** - Request the decision-making algorithm to update its model.
  Requires a timestamp and a callback URL for receiving the update status.
  The algorithm will return a unique update ID for tracking the update status.
  Once the update is complete, the algorithm will send a POST request to the callback
  URL with the update status.
- **POST** `/api/v1/update`
- **Request**:

  ```json
  {
    "timestamp": "2025-01-01T12:00:00Z",
    "callback_url": "http://example.com/callback"
  }
  ```

- **Response**:

  ```json
  {
    "status": "processing",
    "update_id": "e999a61c-fb5c-4f01-9942-cb7dbe501013"
  }
  ```

---

## **Testing**

The template includes a comprehensive test suite for ensuring application reliability. There
are separate test files for each endpoint, and shared fixtures and configurations are defined
in `tests/conftest.py`. Please edit the test files to include additional test cases as needed.

To run the tests, use:

```sh
pytest tests/
```

To run a specific test file like `test_users.py`, use:

```sh
pytest tests/test_users.py
```

---

## **LOGGING**

The template configures detailed logging for debugging and application monitoring. The logging
configuration is defined in `app/logging_config.py`. The logs are stored in the `logs` directory.
The log level can be set to `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL` in the configuration.
There are two loggers defined in the configuration: `app_logger` and `rl_logger`. The `app_logger`
logs all messages, while the `rl_logger` logs only messages related to the decision-making algorithm.
The `app_logger` logs are stored in `logs/app.log`, and the `rl_logger` logs are stored in `logs/rl.log`.
