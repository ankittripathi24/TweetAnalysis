# TweetAnalysis

# Project Title

A brief description of what this project does and who it's for.

## Installation

Instructions on how to install the project, for example:

1. Clone the repository:
    ```
    git clone https://github.com/ankittripathi24/TweetAnalysis.git
    ```

2. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

Instructions on how to use the project, for example:

1. Start the Airflow web server:
    Precondition: Airflow Quick Start: https://airflow.apache.org/docs/apache-airflow/stable/start.html
    
    ```
    airflow webserver -p 8080
    ```

2. Access the Airflow web interface at `http://localhost:8080`.

3. Unpause the DAG in the Airflow web interface.

## DAG

A brief description of the DAG and its tasks:

1. `get_data`: This task downloads data from a GitHub URL and pushes it to XCom.

2. `recreate_model`: This task pulls the data from XCom, creates a blank model for testing purposes, and pushes the model to XCom.

3. `save_model`: This task pulls the model from XCom and saves it to a .pkl file in a specific folder.

## Contributing

Information about how to contribute to the project.

## License

Information about the project's license.