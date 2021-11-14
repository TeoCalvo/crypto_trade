import argparse
import datetime
import requests
import os

import sqlalchemy
import pandas as pd
from sqlalchemy import sql

def import_query(path:str)->str:
    with open(path, "r") as open_file:
        query = open_file.read()
    return query

def connect_db()->sqlalchemy.engine:
    con = sqlalchemy.create_engine("sqlite:///data/crypto.db")
    return con

def get_data(time_start:int, time_end:int, crypto_id=1, currency_id=2781)->dict:
    url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={crypto_id}&convertId={currency_id}&timeStart={time_start}&timeEnd={time_end}"
    data = requests.get(url).json()
    return data

def get_full_history()->dict:
    now = int(datetime.datetime.now().timestamp())
    first = int(datetime.datetime.strptime("2010-01-01", "%Y-%m-%d").timestamp())
    data = get_data(time_start=first, time_end=now)
    return data

def json_to_df(data:dict)->pd.DataFrame:
    cp_data = data.copy()
    new_data= []
    for q in cp_data["data"]["quotes"]:
        q.update(q["quote"])
        del q["quote"]
        new_data.append(q)
    return pd.DataFrame(new_data)
        
def save_data(data:pd.DataFrame, if_exists:str):
    con = connect_db()
    data.to_sql("tb_bitcoin", con, index=False, if_exists=if_exists)

def get_and_save_history():
    data = get_full_history()
    df = json_to_df(data)
    save_data(df, "replace")

def get_update()->dict:
    con = connect_db()
    query = import_query("max_date.sql")
    value = pd.to_datetime(pd.read_sql_query(query, con)["date"])
    value += pd.DateOffset(days=1)
    
    first = int((value.astype("int64")[0]) / 10 ** 9) 
    now = int(datetime.datetime.now().timestamp())

    data = get_data(time_start=first, time_end=now)
    return data

def get_and_save_update():
    data = get_update()
    df = json_to_df(data)
    if df.shape[0] != 0:
        save_data(df, if_exists="append")
        print("Dados atualizados!")
    else:
        print("Não há novos dados.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m", help="Mode of data collect. [all, update]", choices=["all", "update"])
    args = parser.parse_args()

    if args.mode == "all":
        if not os.path.exists("data"):
            os.mkdir("data")
        get_and_save_history()

    elif args.mode == "update":
        get_update()

if __name__ == "__main__":
    main()
