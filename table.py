import requests
import sqlite3
from bs4 import BeautifulSoup
import os
import json
with open('config.json','r') as f:
    jdata = json.load(f)
    print(jdata)


def TableExtraction(reginfo):
    # with open(r"data.html",encoding='utf-8') as fp:
    #     soup = BeautifulSoup(fp, "html.parser")
    #     table = soup.find('table', class_='table table-responsive')
        table = reginfo
        print(table)
        count =0
        total_info = ['']
        for td_num in table.findAll('td'):
            try:
                td_num.text
            except:
                td_num.text = 'na'
            count +=1
            total_info.append(td_num.text)
        print(total_info[1],total_info[2])

        data_doc_no,data_dname,data_sro,data_seller = total_info[1],total_info[2],total_info[4],total_info[5]
        data_Purchaser =total_info[6]
        data_pd = total_info[7]
        data_srocode = total_info[8]
        data_status =total_info[9]
        data_rdate = total_info[3]

        insertVaribleIntoTable(data_doc_no,data_dname,data_sro,data_seller,data_Purchaser,data_pd,data_srocode,data_status,data_rdate)

         #json update: Module 
        jdata['DocNo'] = total_info[1]
        jdata['DName'] = total_info[2]
        jdata['SROName'] = total_info[4]
        jdata['Seller'] = total_info[5]
        jdata['Purchaser'] = total_info[6]
        jdata['PropertyDescription'] = total_info[7]
        jdata['SROCode']= total_info[8]
        jdata['Status'] = total_info[9]
        jdata['RDate'] = total_info[3]
        
        with open('config.json','w') as f:
            f.write(json.dumps(jdata))
            print("JSON RESPONSE",jdata)
        # return jdata
        return json.dumps(jdata,allow_nan = True,indent=4)


def create_database():
    conn = sqlite3.connect(os.path.join('database', 'registration_details.db'))
    conn.execute('''create table IF NOT EXISTS registration (DocNo varchar(30),DName text,SROName text,
                    Seller text,Purchaser text,PropertyDescription text, SROCode varchar(30),
                    Status varchar(30)
      )''')
    # addColumn = "ALTER TABLE registration ADD COLUMN RDate text"
    # conn.execute(addColumn)
    conn.commit()

    print ("Database Connected and Table created")
    conn.close()
# create_database()

import sqlite3

def insertVaribleIntoTable(DocNo,DName,SROName,Seller,Purchaser,PropertyDescription,SROCode,Status,RDate):
    try:
        sqliteConnection = sqlite3.connect(os.path.join('database', 'registration_details.db'))
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO registration
                          (DocNo,DName,SROName,Seller,Purchaser,PropertyDescription,SROCode,Status,RDate) 
                          VALUES (?,?,?,?,?,?,?,?,?);"""  

        data_tuple = (DocNo,DName,SROName,Seller,Purchaser,PropertyDescription,SROCode,Status,RDate)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")
        cursor.close()


    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


# TableExtraction()
