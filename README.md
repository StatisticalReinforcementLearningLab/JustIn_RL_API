# JustIn Decision Making Algorithm API for Digital Interventions

This project is a Flask-based RESTful API that integrates **Flask-SQLAlchemy**
for database management and **Alembic** for migrations. It supports user
management, action handling, interaction data uploads, and algorithm updates.
The given template assumes a Reinforcement Learning (RL) algorithm being used
as the decision making algorithm and provides placeholder for the same; but any
decision making algorithm can be utilized in its place.

---

## Features

- **User Management**: Add and manage users with unique IDs.
- **Action Handling**: Request action based on user context.
- **Data Uploads**: Upload interaction data for users.
- **Model Updates**: Request the decision-making algorithm to update its model.
- **Database Migrations**: Manage schema changes using Alembic.
- **Environment Reproducibility**: Includes a `conda` environment file for easy setup.

---

## **Project Structure**

```plaintext
JustIn_RL_API/
│
├── app/
│   ├── __init__.py          # Flask app factory and CLI commands
│   ├── models.py            # Database model definitions using SQLAlchemy.
│   ├── routes/              # API route handlers
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── action.py
│   │   ├── data.py
│   │   └── update.py
├── migrations/              # Alembic migration files
├── tests/                   # Unit tests
├── config.py                # Application configuration
├── run.py                   # Application entry point
├── README.md                # Documentation
└── environment.yml          # Conda environment file
```

---

## **Pre-requisites**

1. Python 3.9+
2. Conda python package manager
3. Any DBMS software like PostgreSQL, SQLite, MySQL etc.

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

## **Usage**

### **Endpoints**

#### **Add User**

- **POST** `/api/v1/add_user`
- **Request**:

  ```json
  {
    "user_id": "unique_user_id"
  }
  ```

- **Response**:

  ```json
  {
    "user_id": "unique_user_id",
    "message": "User added successfully."
  }
  ```

#### **Request Action**

- **POST** `/api/v1/action`
- **Request**:

  ```json
  {
    "user_id": "unique_user_id",
    "timestamp": "ISO 8601 format",
    "context": {
      "key": "value"
    }
  }
  ```

- **Response**:

  ```json
  {
    "user_id": "unique_user_id",
    "action": {
      "action_type": "click",
      "context": {
        "key": "value"
      }
    }
  }
  ```

#### **Upload Data**

- **POST** `/api/v1/upload_data`
- **Request**:

  ```json
  {
    "user_id": "unique_user_id",
    "timestamp": "ISO 8601 format",
    "context": {
      "key": "value"
    }
  }
  ```

- **Response**:

  ```json
  {
    "message": "Data uploaded successfully."
  }
  ```

#### **Update Model**

- **POST** `/api/v1/update`
- **Request**:

  ```json
  {
    "timestamp": "ISO 8601 format"
  }
  ```

- **Response**:

  ```json
  {
    "message": "Model updated successfully."
  }
  ```

---
