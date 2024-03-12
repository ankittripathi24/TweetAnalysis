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

4. Start the Streamlit app:
    ```
    streamlit run your_streamlit_app.py
    ```

## DAG

A brief description of the DAG and its tasks:

1. `get_data`: This task downloads data from a GitHub URL and pushes it to XCom.

2. `recreate_model`: This task pulls the data from XCom, creates a blank model for testing purposes, and pushes the model to XCom.

3. `save_model`: This task pulls the model from XCom and saves it to a .pkl file in a specific folder.


## Streamlit App

The Streamlit app provides an interactive interface for analyzing tweet data. It offers the following options:

1. **Enter Tweet:** Manually enter a tweet for analysis.
2. **Upload Tweet CSV:** Upload a CSV file of tweets for analysis.
3. **Get Tweets from Scrapper:** Get tweets from a web scrapper for analysis.

In addition to these options, the app also displays stats of the uploaded data. The data for the Streamlit app gets refreshed by the Airflow DAG as per the schedule.


## Contributing


## License

Information about the project's license.