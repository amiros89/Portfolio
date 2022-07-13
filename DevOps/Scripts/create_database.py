# script to create new database (for newly introduced micro-service) across all envs which all run the product on k8s
# staging and production are using RDS postgres, accesible externally
# local envs are running postgres locally which is exposed only internally inside the k8s cluster
# in order to connect to it, user must port-forward the postgres service port to the local port 
# sensitive credentials for staging and production are passed using env variables in CI/CD 

from sqlalchemy import create_engine
import sys
import os
import time

database_name = sys.argv[1]
envs = {
    'local_env': {
        "user": "postgres",
        "password": "",
        "host": "localhost"
    },
    'staging': {
        "user": os.getenv('staging_user'),
        "password": os.getenv('staging_password'),
        "host": os.getenv('staging_postgres')
    },
    'production': {
        "user": os.getenv('production_user'),
        "password": os.getenv('production_password'),
        "host": os.getenv('production_postgres')
    }
}


def open_port(environment):
    os.system(f"kubectl port-forward svc/postgres 5432:5432 -n {environment} > /dev/null 2>&1 &")
    socket_ready = False
    retries = 0
    max_retries = 60
    while not socket_ready and retries < max_retries:
        time.sleep(0.3)
        return_code = os.system(f"nc -vz localhost 5432 > /dev/null 2>&1")
        socket_ready = (return_code == 0)
        retries += 1
    if retries == max_retries:
        raise Exception(f"Failed to port-forward port 5432 for {environment}")
    return


def close_port():
    os.system('pkill kubectl -9')
    return


def create_db(connection_details: dict, environment, local: bool):
    if local:
        password = os.popen(
            f'kubectl get secret postgres -o jsonpath="{{.data.postgresql-password}}"'
            f' -n {environment} | base64 -d').read()
        connection_string = f'postgresql://{connection_details["user"]}:{password}' \
                            f'@{connection_details["host"]}/postgres'
    else:
        connection_string = f'postgresql://{connection_details["user"]}:{connection_details["password"]}' \
                            f'@{connection_details["host"]}/postgres'
    engine = create_engine(connection_string)
    try:
        with engine.connect() as conn:
            print(f'Connected successfully to {env} postgres')
            conn.execute('commit')
            try:
                conn.execute(f'CREATE DATABASE {database_name}')
                print(f'Successfully created database {database_name} in {env}')
            except Exception as e:
                print(f"Failed creating database {database_name} in {env}, error: {e.args}")
        engine.dispose()
    except Exception as e:
        print(f'Failed connecting to {env}, error: {e.args}')
    return


for env, conn_details in envs.items():
    if conn_details['host'] == 'localhost':
        open_port(env)
        create_db(conn_details, env, local=True)
        close_port()
    else:
        create_db(conn_details, env, local=False)