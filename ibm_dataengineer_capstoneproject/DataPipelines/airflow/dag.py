from datetime import timedelta
import pandas as pd
import os
import re
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def parse_log_line(line):
    """Parses a log line into a dictionary."""
    pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "([^"]*)" "([^"]*)"'
    match = re.match(pattern, line)
    if match:
        return {
            'ip': match.group(1),
            'timestamp': match.group(2),
            'request': match.group(3),
            'status': match.group(4),
            'bytes': match.group(5),
            'referer': match.group(6),
            'user_agent': match.group(7)
        }
    else:
        return None
    
def parse_log_file(filename):
    """Parses a log file into a Pandas DataFrame."""
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            parsed_line = parse_log_line(line.strip())
            if parsed_line:
                lines.append(parsed_line)
    return pd.DataFrame(lines)

def parse_log_file_ip_addr(filename, ip_addr):
    """Parses a log file into a Pandas DataFrame."""
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            parsed_line = parse_log_line(line.strip())
            if parsed_line:
                lines.append(parsed_line)
    df = pd.DataFrame(lines)
    df = df[df['ip'] == ip_addr]
    df.to_csv(f'{current_path}/data/transformed_data.txt', index=False)

#defining DAG arguments
default_args = {
    'owner': 'Gabriel Zuany',
    'start_date': days_ago(0),
    'email': ['zuany@somemail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# define the DAG
process_web_log_dag = DAG(
    'process_web_log',
    default_args=default_args,
    description='IBM Data Engineer Capstone Project - Data Pipeline',
    schedule_interval=timedelta(days=1),
)

current_path = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(f'{current_path}/data'):
    os.makedirs(f'{current_path}/data')

extract = BashOperator(
    task_id='extract',
    bash_command=f'curl https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/ETL/accesslog.txt \
        > {current_path}/data/accesslog.txt',
    dag=process_web_log_dag,
)

transform = PythonOperator(
    task_id='transform',
    python_callable=parse_log_file_ip_addr,
    op_args=[f'{current_path}/data/accesslog.txt', '198.46.149.143'],
    dag=process_web_log_dag,
)

load = BashOperator(
    task_id='load',
    bash_command=f'tar -czf {current_path}/data/transformed_data.tar.gz {current_path}/data/transformed_data.txt',
    dag=process_web_log_dag,
)

# task pipeline
extract >> transform >> load