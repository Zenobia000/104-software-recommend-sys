from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
import os
import sql

import ast


app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager(app)

datalist={
		"dep": [
			"綜合教育相關", "普通科目教育相關", "專業科目教育相關", "學前教育相關", "其他教育相關", "美術學相關", "雕塑藝術相關", "美術工藝相關", "音樂學器相關", "戲劇舞蹈相關", "電影藝術相關", "室內藝術相關", "藝術商業設計", "其他藝術相關", "本國語文相關", "英美語文相關", "日文相關科系", "其他外國語文相關", "語言學相關", "歷史學相關", "人類學相關", "哲學相關", "其他人文學相關", "經濟學相關", "政治學相關", "社會學相關", "民族學相關", "心理學相關", "地理學相關", "區域研究相關", "其他經社心理相關", "法律相關科系", "一般商業學類", "文書管理相關", "會計學相關", "統計學相關", "資訊管理相關", "企業管理相關", "工業管理相關", "人力資源相關", "市場行銷相關", "國際貿易相關", "財稅金融相關", "銀行保險相關", "公共行政相關", "其他商業及管理相關", "生物學相關", "化學相關", "地質學相關", "物理學相關", "氣象學相關", "海洋學相關", "其他自然科學相關", "一般數學相關", "數理統計相關", "應用數學相關", "資訊工程相關", "其他數學及電算機科學相關", "公共衛生相關", "醫學系相關", "中醫學系", "復健醫學相關", "護理助產相關", "醫學技術及檢驗相關", "牙醫學相關", "藥學相關", "醫藥工程相關", "醫務管理相關", "獸醫相關", "其他醫藥衛生相關", "電機電子維護相關", "金屬加工相關", "機械維護相關", "木工相關", "冷凍空調相關", "印刷相關", "汽車汽修相關", "其他工業技藝相關", "測量工程相關", "工業設計相關", "化學工程相關", "材料工程相關", "土木工程相關", "環境工程相關", "河海或船舶工程相關", "電機電子工程相關", "工業工程相關", "礦冶工程相關", "機械工程相關", "航太工程相關", "農業工程相關", "紡織工程相關", "核子工程相關", "光電工程相關", "其他工程相關", "建築相關", "景觀設計相關", "都巿規劃相關", "其他建築及都市規劃學類", "農業相關", "畜牧相關", "園藝相關", "植物保護相關", "農業經濟相關", "食品科學相關", "水土保持相關", "農業化學相關", "林業相關", "漁業相關", "其他農林漁牧相關", "綜合家政相關", "食品營養相關", "兒童保育相關", "服裝設計相關", "美容美髮相關", "其他家政相關", "運輸管理相關", "航空相關", "航海相關", "航運管理相關", "通信學類", "其他運輸通信相關", "儀容服務學類", "餐旅服務相關", "觀光事務相關", "其他觀光服務相關", "新聞學相關", "廣播電視相關", "公共關係相關", "大眾傳播學相關", "圖書管理相關", "文物傳播相關", "其他大眾傳播相關", "普通科", "警政相關", "軍事相關", "體育相關", "其他相關科系"
		],
        "pos":[
            '軟體設計工程師', '網路安全分析師', '電子商務技術主管', 'BIOS工程師', '演算法開發工程師', '軟體專案主管', 'MES工程師', 'MIS_網管主管', 'MIS程式設計師', '資訊設備管制人員', '網路管理工程師', '資訊助理人員', '通訊軟體工程師', 
            '系統維護_操作人員', '韌體設計工程師', '其他資訊專業人員', 'Internet程式設計師', '電玩程式設計師', '資料庫管理人員', '系統分析師'
        ]
	}


class User(UserMixin):  
    """  
 設置一： 只是假裝一下，所以單純的繼承一下而以 如果我們希望可以做更多判斷，
 如is_administrator也可以從這邊來加入 
 """
    
    pass 


@login_manager.user_loader  
def user_loader(email):  
    """  
 設置二： 透過這邊的設置讓flask_login可以隨時取到目前的使用者id   
 :param email:官網此例將email當id使用，賦值給予user.id    
 """   
    user = User()  
    user.id = email  
    return user


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] != "":  
        #  實作User類別  
        user = User()  
        #  設置id就是email  
        user.id = request.form['username']  
        #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。  
        login_user(user)  
        #  登入成功，轉址  
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    recommend = sql.optimized_random(6)
    if current_user.is_active:
        return render_template('index.html', uname = current_user.id, df = datalist, recommend = recommend)
    else:
        return render_template('index.html', df = datalist, recommend = recommend)

@app.route('/index')
def home():
    if current_user.is_active:
        return render_template('index.html', uname = current_user.id)
    return redirect(url_for('index'))

@app.route('/job-search', methods=['POST'])
def search():
    print(request.form)
    joblist = []
    recommend = sql.optimized_random(10)
    if request.form != '':
        if request.form.get('find'):
            if request.form['find'] == 'job':
                # print(request.form)
                joblist = sql.selJob(request.form)
                # print(joblist)

            elif request.form['find'] == 'com':
                joblist = sql.selCom(request.form)

        else:
            joblist = sql.selBtn(request.form)

    if current_user.is_active:
        return render_template('job-search.html', uname = current_user.id, joblist = joblist, df = datalist, recommend = recommend)
    return render_template('job-search.html', joblist = joblist, df = datalist, recommend = recommend)

@app.route('/job-detail', methods=['GET','POST'])
def jobdetail():
    jobdt = []
    if request.form != '':
        print(request.form)
        jobdt = request.form['jobdt']
        # 轉dict
        jobdt = ast.literal_eval(jobdt)
        # print(type(jobdt))

    if current_user.is_active:
        return render_template('job-detail.html',uname = current_user.id, jobdt = jobdt)
    return render_template('job-detail.html', jobdt = jobdt)

@app.route('/team')
def team():
    if current_user.is_active:
        return render_template('team.html',uname = current_user.id)
    return render_template('team.html')

@app.route('/stat')
def stat():
    if current_user.is_active:
        return render_template('stat.html',uname = current_user.id)
    return render_template('stat.html')

@app.route('/model')
def model():
    if current_user.is_active:
        return render_template('model.html',uname = current_user.id)
    return render_template('model.html')



if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)