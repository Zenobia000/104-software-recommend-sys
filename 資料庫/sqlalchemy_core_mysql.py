#----------practice start------------
import sqlalchemy as db
from sqlalchemy import Column

#連接資料庫
username = ''  # 資料庫帳號
password = ''  # 資料庫密碼
host = 'localhost'  # 資料庫位址
port = '3306'  # 資料庫埠號
database = 'sql_tutorial'  # 資料庫名稱
table = 'job7'  # 表格名稱
# 建立資料庫引擎
engine = db.create_engine(
    f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')
# 建立資料庫連線
# con = engine.raw_connection()
connection = engine.connect()

# # 取得資料庫的元資料（資料庫預設編碼、表格清單、表格的欄位與型態、... 等）
metadata = db.MetaData()
# print(f"metadata: \n{metadata.sorted_tables}")

# # 取得 office 資料表的 Python 對應操作物件
table_office = db.Table(table, metadata, autoload=True, autoload_with=engine)
# print(f"metadata: \n{metadata.sorted_tables}",
#       end="\n" + ("-" * 80) + "\n")  # 比較Table建立前後的metadata

# SELECT fetchall
query = db.select(table_office)
proxy = connection.execute(query)
results = proxy.fetchall()

print(query, end="\n" + ("-" * 80) + "\n")

# # SELECT fetchone
# query = db.select(table_office)
# proxy = connection.execute(query)
# for _ in range(10):
#     results = proxy.fetchone()
#     print(results)
#     print("*" * 80)
# print("-" * 80)

# SELECT Specific Columns (like)
# query = db.select(table_office.c.officeCode)
# query2 = db.select([table_office.columns.job_title , table_office.columns.tools]).where(table_office.columns.tools == 'python')
# query3 = db.select(table_office.columns.job_title , table_office.columns.tools).filter(table_office.columns.tools.like("%python%"))

# proxy = connection.execute(query3)
# results = proxy.fetchall()
# print(results, end="\n" + ("-" * 80) + "\n")

# # SELECT where
query4 = db.select(
    table_office.columns.job_title,
    table_office.columns.tools).where(table_office.c.tools == "python")
proxy = connection.execute(query4)
results = proxy.fetchall()
# print(results, end="\n" + ("-" * 80) + "\n")

# SELECT limit & offset
query = db.select(table_office.c.tools).limit(10).offset(1)
proxy = connection.execute(query)
results = proxy.fetchall()
# print(results, end="\n" + ("-" * 80) + "\n")

x = 'mysql'
# SELECT limit & like
query3 = db.select(
    table_office.columns.job_title, table_office.columns.tools).filter(
        table_office.columns.tools.like("%" + x + "%")).limit(10)

proxy = connection.execute(query3)
results = proxy.fetchall()
# print(results, end="\n" + ("-" * 80) + "\n")

# SELECT order by
query3 = db.select([table_office
                    ]).order_by(db.desc(table_office.columns.job_title),
                                table_office.columns.tools).limit(5).offset(2)

proxy = connection.execute(query3)
# results = proxy.fetchall()
# print(results, end="\n" + ("-" * 80) + "\n")
# for _ in range(5):
#     results = proxy.fetchone()
#     print(results)
#     print("*" * 80)
# print("-" * 80)

# SELECT group by

# query3 = db.select([db.func.sum(table_office.columns.responsibility), table_office.columns.job_title]).group_by(table_office.columns.job_title).limit(5).offset(2)
# proxy = connection.execute(query3)
# for _ in range(5):
#     results = proxy.fetchone()
#     print(results)
#     print("*" * 80)
# print("-" * 80)

# SELECT like & like
query3 = db.select(
    table_office.columns.job_title, table_office.columns.tools).filter(
        table_office.columns.tools.like("%" + "python" + "%")).filter(
            table_office.columns.tools.like("%" + "mysql" + "%")).limit(5)

proxy = connection.execute(query3)
results = proxy.fetchall()
# print(results, end="\n" + ("-" * 80) + "\n")sss

#chatGPT給的答案
# stmt = select([Column('job_title'), Column('tools')]) \
# .where(and_(Column('tools').like('%python%'), Column('tools').like('%mysql%'))) \
# .limit(5)
stmt = db.select([table_office.columns.job_title, table_office.columns.tools]) \
    .where(db.and_(table_office.columns.tools.like('%python%'), table_office.columns.tools.like('%mysql%'))) \
    .limit(5)

# proxy = connection.execute(stmt)
# results = proxy.fetchall()
# print(results, end="\n" + ("-" * 80) + "\n")

# -----------------------------------
# Close connection & engine
connection.close()
engine.dispose()
#----------practice end--------------
