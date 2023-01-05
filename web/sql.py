from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
# from sqlalchemy import Column, or_
from sqlalchemy import Text, create_engine , text , select, MetaData, Table  ,func , Column , String , Integer, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#連接資料庫
username = 'test'  # 資料庫帳號
password = 'test01'  # 資料庫密碼
host = '192.168.31.105'  # 資料庫位址
port = '3306'  # 資料庫埠號
database = 'sql_tutorial'  # 資料庫名稱
table = 'job7'  # 表格名稱
# 建立資料庫引擎
engine = db.create_engine(
    f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

Base = declarative_base()
# Base.metadata.create_all(engine)
metadata = MetaData(engine)
metadata.reflect()
table2 = metadata.tables["job7"]
Session = sessionmaker(bind=engine)
session = Session()
# 建立資料庫連線
# connection = engine.connect()

# # 取得資料庫的元資料（資料庫預設編碼、表格清單、表格的欄位與型態、... 等）
# metadata = db.MetaData()
# # 取得 office 資料表的 Python 對應操作物件
# table_office = db.Table(table, metadata, autoload=True, autoload_with=engine)

class job(Base):
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

    # def to_dict(self):
    #     return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    # Base.to_dict = to_dict
    def to_json(self):
        return {
            'id':self.id,
            'job_link':self.job_link,
            'job_category':self.job_category,
            'job_categories':self.job_categories,
            'position':self.position,
            'county':self.county,
            'area':self.area,
            'company_name':self.company_name,
            'job_title':self.job_title,
            'work_content':self.work_content,
            'work_category':self.work_category,
            'working_hours':self.working_hours,
            'responsibility':self.responsibility,
            'conditions':self.conditions,
            'work_place':self.work_place,
            'work_experience':self.work_experience,
            'academic_requirements':self.academic_requirements,
            'department_requirements':self.department_requirements,
            'tools':self.tools,
            'skills':self.skills,
            'capital':self.capital
        }


# select 
def selJob(req):
    print(req)
    # print(table2)
    # select * from job7
    rs = session.query(job)
    # print(rs)
    # rs = query.filter(or_(table.tools.like('%python%')))
    # print(rs)
    # 縣市
    if req['county'] != '':
        c = req['county']
        rs = rs.filter(job.county.like("%" + c + "%"))

    # 區域
    if req['district'] != '':
        d = req['district']
        rs = rs.filter(job.area.like("%" + d + "%"))

    # 薪資
    if req['salary'] != '':
        s = req['salary']
        rs = rs.filter(job.conditions.like("%" + s + "%"))

    # 職位類別
    if req['jobCategories'] != '':
        jc = req['jobCategories']
        rs = rs.filter(job.job_categories.like("%" + jc + "%"))

    # 職位
    if req['position'] != '':
        d = req['position']
        rs = rs.filter(job.position.like("%" + d + "%"))

    # 工作經歷
    if req['exp'] != '':
        exp = req['exp']
        rs = rs.filter(job.work_experience.like("%" + exp + "%"))

    # 學歷
    if req['edu'] != '':
        edu = req['edu']
        rs = rs.filter(job.academic_requirements.like("%" + edu + "%"))

    # 科系
    if req['dep'] != '':
        dep = req['dep']
        rs = rs.filter(job.department_requirements.like("%" + dep + "%"))

    # 擅長工具
    if req['tools'] != '':
        tools = req['tools'].split(",")
        for i in tools:
            if i == 'Java':
                rs = rs.filter(or_(job.tools.like("%|" + i + "|%")))
            else:
                rs = rs.filter(or_(job.tools.like("%" + i + "%")))

    # print(rs)
    res = rs.all()
    temp = []
    for x in res:
        temp.append(x.to_json())
    return temp
    # query4 = db.select(table_office.columns.job_title, table_office.columns.tools).where(table_office.c.tools== "python" or table_office.c.tools like "%sss%")
    # proxy = connection.execute(query4)
    # results = proxy.fetchall()
    # print(results, end="\n" + ("-" * 80) + "\n")

def pos():
    p = set()
    rs = session.query(job.position).all()
    for i in rs:
        for j in i:
            p.add(j)
    print(p)