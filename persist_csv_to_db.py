import pandas as pd

from sqlalchemy import create_engine, Table, MetaData, select
from sqlalchemy.orm import sessionmaker

import os
from datetime import datetime

DATABASE_URL = "mysql+mysqlconnector://root:Syadav%401999@localhost/ETL_ASSIGNMENT"


def loadCurrencyTableData(session, table):
    results = session.query(table.c.REF_CURRENCY_ID, table.c.CURRENCY_CODE).all()
    key_value_pairs = {row.REF_CURRENCY_ID: row.CURRENCY_CODE for row in results}
    return key_value_pairs

def createEntryForCsvFile(csv_path, session, csvTable):
    file_name = os.path.basename(csv_path)
    directory_name = os.path.abspath(csv_path)
    creation_date = datetime.fromtimestamp(os.path.getctime(csv_path))
    
    insert_statement = csvTable.insert().values(
        FILE_NAME = file_name,
        FILE_PATH = directory_name,
        UPLOAD_TIME = creation_date,
    )
    
    session.execute(insert_statement)
    session.commit()
    
    stmt = select(csvTable.c.CSV_FILE_ID).where(csvTable.c.FILE_NAME == file_name)
    resultId = session.execute(stmt).fetchone()
    return resultId[0]

def checkInMap(key_value_pairs, val):
    for k, v in key_value_pairs.items():
        if v == val:
            return k

#entry point for this file
def save_csv_to_db(csv_path, mainCurrencyCode):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()

    csvTable = Table('CSV_FILE', metadata, autoload_with=engine)        #access file using defined engine 
    fileId = createEntryForCsvFile(csv_path, session, csvTable)

    table = Table('REF_CURRENCY', metadata, autoload_with=engine)
    key_value_pairs = loadCurrencyTableData(session, table)

    df = pd.read_csv(csv_path)

    filteredDf = df[~df['code'].isin(key_value_pairs.values())]

    # Insert reference data for currency table
    for index, row in filteredDf.iterrows():
        insert_statement = table.insert().values(
            CURRENCY_NAME=row['name'],
            CURRENCY_CODE=row['code'],
            CURRENCY_ALPHA_CODE=row['alphaCode'],
            CURRENCY_NUMERIC_CODE=row['numericCode']
        )
        session.execute(insert_statement)

    session.commit()
    key_value_pairs = loadCurrencyTableData(session, table)

    conversionTable = Table('CURRENCY_CONVERSION_RATES', metadata, autoload_with=engine)

    currency_id_1 = checkInMap(key_value_pairs, mainCurrencyCode)
    print(df)

    for index, row in df.iterrows():
        insert_statement = conversionTable.insert().values(
            CSV_FILE_ID=fileId,
            CURRENCY_ID_1=currency_id_1,
            CURRENCY_ID_2=checkInMap(key_value_pairs, row['code']),
            CONVERSION_RATE=row['rate'],
            INVERSE_CONVERSION_RATE=row['inverseRate'],
            DATE=datetime.now()
        )
        session.execute(insert_statement)
    session.commit()
    session.close()
