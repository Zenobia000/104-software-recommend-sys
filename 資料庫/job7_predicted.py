import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from sqlalchemy import String
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

username = ''  # 資料庫帳號
password = ''  # 資料庫密碼
host = 'localhost'  # 資料庫位址
port = '3306'  # 資料庫埠號
database = 'sql_tutorial'  # 資料庫名稱
# 连接到 MySQL 数据库
engine = db.create_engine(
    f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

# 创建基类
Base = declarative_base()


# 定義表
class MyTable(Base):
    __tablename__ = 'job7'
    id = Column(Integer, primary_key=True)
    job_link = Column(String(200))
    job_category = Column(String(100))
    job_categories = Column(String(100))
    position = Column(String(100))
    county = Column(String(50))
    area = Column(String(50))
    company_name = Column(String(150))
    job_title = Column(String(300))
    work_content = Column(String(4000))
    work_category = Column(String(50))
    working_hours = Column(String(50))
    responsibility = Column(String(50))
    conditions = Column(String(50))
    work_place = Column(String(300))
    work_experience = Column(String(100))
    academic_requirements = Column(String(200))
    department_requirements = Column(String(1800))
    tools = Column(String(500))
    skills = Column(String(300))
    capital = Column(String(100))
    Predicted = Column(Integer)
    Foreign = Column(Integer)
    salary_avg = Column(Integer)


table = MyTable.__table__
#创建表
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# 讀取 CSV 文件
df = pd.read_csv(
    r'C:\Users\student\python_web_scraping-master\SQL\MYSQL\Predicted.csv')
# Insert the data into the database
df.to_sql('job7', engine, if_exists='append', index=False)
# 提交session
session.commit()

# 關閉連結
session.close()