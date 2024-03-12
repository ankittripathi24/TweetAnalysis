import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pickle
from sklearn.base import BaseEstimator



# Define the Python functions for your tasks
def get_data(**kwargs):
    print("Hello, Airflow! I started Getting Data Successfully")
    url = 'https://raw.githubusercontent.com/sharmaroshan/Twitter-Sentiment-Analysis/master/train_tweet.csv'
    data = pd.read_csv(url)
    print("Hello, Airflow! Data Recieved")
    kwargs['ti'].xcom_push(key='data', value=data)

def recreate_model(**kwargs):
    print("Hello, Airflow! I started Recreating Model")
    ti = kwargs['ti']
    data = ti.xcom_pull(key='data')
    # Code to recreate the model using 'data'
    print(data)
    model = open("model.txt", "a")
    model.write("Now the file has more content!")
    model.close()
    # model = BlankModel()
    print("Hello, Airflow! Model is created")

    # Push the model to XCom
    # kwargs['ti'].xcom_push(key='model', value=model)

def save_model():
    print("Hello, Airflow! I will now push the model to right folder")
    # Code to save the model to a specific folder
    # Get the model from XCom
    # ti = kwargs['ti']
    # model = ti.xcom_pull(key='model')

    # Specify the path to the folder where you want to save the model
    folder_path = 'C:/Users/cefb8t/Documents/Code/My Trials/AI ML'
    file_path = f'{folder_path}/model_new.txt'
    
    folder_path = '/mnt/c/Users/cefb8t/Documents/Code/My Trials/AI ML'
    file_path = f'{folder_path}/model_new.txt'
    import shutil
    
    print("Hello, Airflow! Model Pushed")
    # Save the model
    # with open(file_path, 'wb') as file:
        # pickle.dump(model, file)
    shutil.copyfile('model.txt', file_path)

# Define the default arguments for your DAG
default_args = {
    'owner': 'ankit',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define your DAG
with DAG(
    'get_tweets_create_model',
    default_args=default_args,
    description='A simple DAG to get_tweets_create_model',
    schedule_interval=None,
) as dag:

    # Define your tasks
    t1 = PythonOperator(
        task_id='get_data',
        python_callable=get_data,
        provide_context=True,
    )

    t2 = PythonOperator(
        task_id='recreate_model',
        python_callable=recreate_model,
        provide_context=True,
    )

    t3 = PythonOperator(
        task_id='save_model',
        python_callable=save_model,
    )

    # Define the order of your tasks
    t1 >> t2 >> t3
