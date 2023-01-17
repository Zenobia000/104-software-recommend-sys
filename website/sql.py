from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
# from sqlalchemy import Column, or_
from sqlalchemy import Text, create_engine , text , select, MetaData, Table  ,func , Column , String , Integer, or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import load_only
from sqlalchemy.sql import func
import random

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
    Predicted = Column(Integer)
    Foreign = Column(Integer)
    salary_avg = Column(Integer)

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
            'capital':self.capital,
            'predicted':self.Predicted,
            'foreign':self.Foreign,
            'salary_avg':self.salary_avg
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
        if s == '3':
            rs = rs.filter(job.salary_avg <= 30000)
        elif s == '4':
            rs = rs.filter(and_(job.salary_avg > 30000, job.salary_avg <= 50000))
        elif s == '5':
            rs = rs.filter(and_(job.salary_avg > 50000, job.salary_avg <= 80000))
        elif s == '6':
            rs = rs.filter(and_(job.salary_avg > 80000, job.salary_avg <= 100000))
        else :
            rs = rs.filter(job.salary_avg > 100000)

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
        # print(tools)
        clauses = []
        
        for i in tools:
            if i == 'Java' or i == 'C' or i == 'R':
                a = job.tools.like("%|" + i + "|%")
            else:
                a = job.tools.like("%" + i + "%")
            clauses.append(a)
        rs = rs.filter(or_(*clauses))

    print(rs)
    res = rs.all()
    temp = []
    for x in res:
        temp.append(x.to_json())
    return temp
    # query4 = db.select(table_office.columns.job_title, table_office.columns.tools).where(table_office.c.tools== "python" or table_office.c.tools like "%sss%")
    # proxy = connection.execute(query4)
    # results = proxy.fetchall()
    # print(results, end="\n" + ("-" * 80) + "\n")

def selCom(req):
    rs = session.query(job)
    if req['companyName'] != '':
        com = req['companyName']
        rs = rs.filter(job.company_name.like("%" + com + "%"))

    res = rs.all()
    temp = []
    for x in res:
        temp.append(x.to_json())
    return temp

def selBtn(req):
    rs = session.query(job)

    # 新鮮人、無經驗可
    if req['condition'] == 'exp':
        rs = rs.filter(job.work_experience.like("%0-1%"))

    # 管理職
    if req['condition'] == 'manage':
        rs = rs.filter(job.responsibility != '0')

    # 五萬以上
    if req['condition'] == 'salary':
        rs = rs.filter(job.Predicted >= 50000)

    # 外商
    if req['condition'] == 'foreign':
        rs = rs.filter(job.Foreign == 1)

    # 轉職
    if req['condition'] == 'change':
        exp = ['3-5', '5-10', '10']
        clauses = []
        
        for i in exp:
            a = job.work_experience.like("%" + i + "%")
            clauses.append(a)

        rs = rs.filter(or_(*clauses))

    # 轉職
    if req['condition'] == 'science':
        science = ['其他自然科學相關', '一般數學相關', '數理統計相關', '應用數學相關', '資訊工程相關', '其他數學及電算機科學相關']
        clauses = []
        
        for i in science:
            a = job.department_requirements.like("%" + i + "%")
            clauses.append(a)

        rs = rs.filter(or_(*clauses))


    print(rs)
    res = rs.all()
    temp = []
    for x in res:
        temp.append(x.to_json())
    return temp

def pos():
    p = set()
    rs = session.query(job.position).all()
    for i in rs:
        for j in i:
            p.add(j)
    print(p)

def optimized_random(count):
    query = session.query(job)
    rowCount = int(query.count())
    randomRow = query.offset(int(rowCount*random.random())).limit(count).all()

    temp = []
    for x in randomRow:
        temp.append(x.to_json())
    return temp