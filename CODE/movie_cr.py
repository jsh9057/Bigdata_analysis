import urllib.request
from datetime import timedelta
import datetime
import re
from bs4 import BeautifulSoup
from math import ceil
import csv
from pandas import Series,DataFrame
import pandas as pd
from  urllib.parse import quote
import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt
import numpy
import time
import konply


from xml.etree.ElementTree import parse



######### naver 영화 평점 관련주소 #################################################
url1 = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code='
url2 = '&type=after&onlyActualPointYn=N&order=newest&page='

######### code_info 저장 path ####################################################
code_info_save = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Name_Code/code_name_info"
code_info_2017 = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Name_Code/code_name_info_2017"
code_info_2016 = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Name_Code/code_name_info_2016"
code_info_2015 = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Name_Code/code_name_info_2015"


######### naver영화 검색 관련 주소 ##################################################
code_info_url1 ="https://movie.naver.com/movie/search/result.nhn?query="
code_info_url2 ="&section=all&ie=utf8"


## 영화코드 추출 (URL 입력 - > 영화코드 추출)
def getCode(URL):
    code_st = re.match('[0-9]+',URL)
    print(code_st)
    code = re.search('[0-9]',code_st).group()
    return (code)



# 영화 리뷰 추출(영화 code 입력 시 리뷰페이지 평점,리뷰,날짜 얻어옴)
def getReviewResult(CODE,opendate,year,name):
    ##C:\Users\Jeong\Desktop\ENP_PROJECT\DATA###
    namebf = name
    for n in namebf :
        if n==':':
            n='_'
    f=open("C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Review/"+namebf+"_review__"+CODE+"___"+year+".csv","w",encoding="cp949",newline='')
    field_name_list = ['index','time','score','reple','1st_week','2st_week','3st_week']
    writer = csv.DictWriter(f,fieldnames=field_name_list)
    writer.writeheader()
    page = int(1)



    ######################### count 는 총 페이지 수를 의미  #############################
    ######################### count 구하는 부분 ########################################
    URL = url1 +CODE + url2 + str(1)
    try:
        open_ = urllib.request.urlopen(URL)
        html = open_.read().decode('utf-8')
        soup = BeautifulSoup(html,'html.parser')
        count = soup.find('strong',class_='total').find_all('em')[1].get_text()
        count = int(count.replace(",",""))
        page=ceil(count/10)
        URL = url1 +CODE + url2 + str(page)
    except:
        return
##################################################################################

    not_Last_state = False
    print("Please Waiting..")
    index = 0
    start_date = datetime.datetime.strptime(opendate,"%Y-%m-%d")
    while page :
        URL = url1 +CODE + url2 + str(page)
        open_ = urllib.request.urlopen(URL)
        html = open_.read().decode('utf-8')
        soup = BeautifulSoup(html,'html.parser')
        score_result = soup.find('div',class_='score_result')
        lis = score_result.find_all('li')
        lis.reverse()
        print("now page " + str(page))
        for li in lis:
            page = int(page)
            reple = li.find('div',class_='score_reple').find('p').get_text()
            score = li.find('div',class_='star_score').find('em').get_text()


          #  print(li)
            try:
                children = li.find('div',class_='score_reple').find('dl').find('dt').find_all('em')[1].get_text()
            except:
                print(name+" 의 "+ str(page)+ " 페이지 오류")
                break
            try:
              #  print(children)
                time = str(children)
                time_s = time[0:10]
                time_y = time_s[0:4]
                time_m = time_s[5:7]
                time_d = time_s[8:10]
                date_time = time_y+"-"+time_m+"-"+time_d
                date_time = datetime.datetime.strptime(date_time,"%Y-%m-%d")
                if(date_time - start_date) <= timedelta(days = 6):
                    index += 1
                    writer.writerow({'index':index,"time":time_s,'score':score,"reple":reple,"1st_week":1,"2st_week":0,"3st_week":0})

                elif (date_time - start_date) <= timedelta(days=13):
                    index += 1
                    writer.writerow({'index':index,"time":time_s,'score':score,"reple":reple,"1st_week":0,"2st_week":1,"3st_week":0})

                elif (date_time - start_date) <= timedelta(days=20):
                    index += 1
                    writer.writerow({'index':index,"time":time_s,'score':score,"reple":reple,"1st_week":0,"2st_week":0,"3st_week":1})
                else:
                    print("들어옴")
                    Last_state = True
                    return print("끝!")
                #f.write('작성시간 : '+time_s+'\n')
                #f.write('영화평점 : '+score+'\n')
                #f.write('리뷰내용 : '+reple+'\n\n')
            except:
                print("댓글오류 다음댓글로갑니다")
        page -= 1
        if not_Last_state:
            print("not_last_state = false")
            break
    #except:
    #    return print(name+" 다시 해야됩니다")
    print("FINISH !!")
    f.close()


#C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Name_Code/code_name_info
# https://movie.naver.com/movie/search/result.nhn?query=%ED%83%9D%EC%8B%9C%EC%9A%B4%EC%A0%84%EC%82%AC&section=all&ie=utf8

def name_to_code_save_csv(csv_file_name,year,namelist,codelist,opendatelist):

    ################# csv 파일에서 이름 추출 #################################################
    df = pd.read_csv(csv_file_name,encoding='cp949')
    df.reset_index(drop=True)
    for i in range(30):
        namelist.append(df.__getitem__('name')[i])
        opendatelist.append(df.__getitem__('opendate')[i])

    print(opendatelist)
    print(namelist)

    for element in namelist:
        URL = code_info_url1 + quote(element) + code_info_url2
        open_ = urllib.request.urlopen(URL)
        html = open_.read()
        soup = BeautifulSoup(html,'html.parser')
        link = soup.find('ul',class_='search_list_1').find('a',href=True)
        res = link['href']
        code = re.findall('\d+',res)[0]
        codelist.append(code)


    ################## csv 파일에서 추출된 이름을 기반으로 영화 이름과 code를 매치 시켜줌 ##########
    ################## 새로운 파일 code_name_info_'year'.csv 생성                  ###########

    with open (code_info_save+"_"+year+".csv",'w',encoding='cp949',newline='')as writer_csv:
        field_name_list = ["ranking","name","code","opendate"]
        writer = csv.DictWriter(writer_csv,fieldnames=field_name_list)
        writer.writeheader()
        ranking = 1
        for name in namelist:
            writer.writerow({"ranking":ranking,"name":name,"code":codelist[ranking-1],"opendate":opendatelist[ranking-1]})
            ranking +=1

    return









#C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Ranking/boxofficelist_2017_ko.csv

def data1():
    s = datetime.datetime.now()
    print("시작합니다. 현재시간 : "+str(s))

    ###############2017#######################################################################################################
    namelist_2017=[]
    codelist_2017=[]
    opendatelist_2017=[]
    l2017 = 17

   # name_to_code_save_csv("C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Ranking/boxofficelist_2017_ko.csv","2017",namelist_2017
           #                                ,codelist_2017,opendatelist_2017)
   # getReviewResult("155256","2017-06-08","2017","악녀")
   # for code in codelist_2017:
     #   getReviewResult(codelist_2017[l2017],opendatelist_2017[l2017],"2017",namelist_2017[l2017])
    #    l2017+=1
    #    if l2017 == 29:
    #        break
    #getReviewResult("85579","2017-12-20","2017")
    ##########################################################################################################################

    ###############2016#######################################################################################################

    #namelist_2016=[]
    #codelist_2016=[]
    #opendatelist_2016=[]
    #l2016 = 15
    #name_to_code_save_csv("C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Ranking/boxofficelist_2016_ko.csv","2016",namelist_2016
     #                                      ,codelist_2016,opendatelist_2016)


    getReviewResult("167108","2016-02-24","2016","귀향")

   # for code in codelist_2016:
   #     if l2016 == 30:
   #         break
   #     getReviewResult(codelist_2016[l2016],opendatelist_2016[l2016],"2016",namelist_2016[l2016])
   #     l2016+=1
    #e=datetime.datetime.now()
    #return print("끝났습니다. 소요된시간 : "+str(e-s))
    ##########################################################################################################################

    ###############2015#######################################################################################################
   # namelist_2015=[]
   # codelist_2015=[]
   # opendatelist_2015=[]
   # l2015 = 0
   # name_to_code_save_csv("C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Ranking/boxofficelist_2015_ko.csv","2015",namelist_2015
   #                                        ,codelist_2015,opendatelist_2015)
   # l2015 = 13
    #for code in codelist_2015:
     #   if l2015 == 30:
     #       break
     #   getReviewResult(codelist_2015[l2015],opendatelist_2015[l2015],"2015",namelist_2015[l2015])
     #   l2015+=1

    #getReviewResult("123596","2015-02-11","2015","조선명탐정 _ 사라진 놉의 딸")
    #getReviewResult("124201","2015-09-24","2015","탐정 _ 더 비기닝")

    ###########################################################################################################################

    e=datetime.datetime.now()
    print("끝났습니다. 소요된시간 : "+str(e-s))


    return





def get_request_url(url):
    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')

    except Exception as e:
        print(e)
        print("[%s] Error for URL: %s" %(datetime.datetime.now(),url))
        return None


def getBoxoffice_Viewr(name, opendate_str, year):
    opendate_dt = datetime.datetime.strptime(opendate_str,"%Y-%m-%d")
    week1_dt = opendate_dt+timedelta(days=6)
    week2_dt = opendate_dt+timedelta(days=13)
    week3_dt = opendate_dt+timedelta(days=20)

    week1_str = str (week1_dt)[:10]
    week2_str = str (week2_dt)[:10]
    week3_str = str (week3_dt)[:10]
    week1_str = week1_str[0:4]+week1_str[5:7]+week1_str[8:10]
    week2_str = week2_str[0:4]+week2_str[5:7]+week2_str[8:10]
    week3_str = week3_str[0:4]+week3_str[5:7]+week3_str[8:10]


#http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.xml?key=b6223c60d25b4c7508f62556cfb8b4f8&targetDt=20150805
    base_url= "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.xml?"
    key = "key=b6223c60d25b4c7508f62556cfb8b4f8"
    targetDt_w1 = "&targetDt="+str(week1_str)
    targetDt_w2 = "&targetDt="+str(week2_str)
    targetDt_w3 = "&targetDt="+str(week3_str)
    multiMovieYn = "&multiMovieYn=N"
    repNationCd = "&repNationCd=K"


    url_w1 = base_url + key + targetDt_w1+multiMovieYn+repNationCd
    url_w2 = base_url + key + targetDt_w2+multiMovieYn+repNationCd
    url_w3 = base_url + key + targetDt_w3+multiMovieYn+repNationCd


    if name=="님아, 그 강을 건너지 마오":
        url_w1 = base_url+ key + targetDt_w1 + repNationCd
        url_w2 = base_url+ key + targetDt_w2 + repNationCd
        url_w3 = base_url+ key + targetDt_w3 + repNationCd

    retData_w1 = get_request_url(url_w1)
    week1_redata = ET.fromstring(retData_w1)

    retData_w2 = get_request_url(url_w2)
    week2_redata = ET.fromstring(retData_w2)

    retData_w3 = get_request_url(url_w3)
    week3_redata = ET.fromstring(retData_w3)


    audiAcc_w1 = 0
    audiAcc_w2 = 0
    audiAcc_w3 = 0

    for child in week1_redata.findall('weeklyBoxOfficeList')[0].findall('weeklyBoxOffice'):
        movieNm= child.find('movieNm').text
        if movieNm == name :
            audiAcc	= child.find('audiAcc').text
            audiAcc = int(audiAcc)
            audiAcc_w1 = audiAcc
            break



    for child in week2_redata.findall('weeklyBoxOfficeList')[0].findall('weeklyBoxOffice'):
        movieNm= child.find('movieNm').text
        if movieNm == name :
            audiAcc	= child.find('audiAcc').text
            audiAcc = int(audiAcc)
            audiAcc_w2 = audiAcc - audiAcc_w1
            break



    for child in week3_redata.findall('weeklyBoxOfficeList')[0].findall('weeklyBoxOffice'):
        movieNm= child.find('movieNm').text
        print(movieNm)
        if movieNm == name :
            audiAcc	= child.find('audiAcc').text
            audiAcc = int(audiAcc)
            audiAcc_w3 = audiAcc - audiAcc_w2 - audiAcc_w1
            break



    with open(code_info_save+"_"+year+".csv",mode='r') as csvinput:
        with open(code_info_save+"_"+year+"_w.csv",'a',encoding='cp949',newline='')as csvouput:
            writer = csv.writer(csvouput)

            for row in csv.reader(csvinput):
                if row[1]== name :
                    writer.writerow(row+[audiAcc_w1]+[audiAcc_w2]+[audiAcc_w3])
                    return

def get_namelsit_opendatelist(namelist,opendatelist,year):
    df = pd.read_csv(code_info_save+"_"+year+".csv",encoding='cp949')
    df.reset_index(drop=True)
    for i in range(30):
            namelist.append(df.__getitem__('name')[i])
            opendatelist.append(df.__getitem__('opendate')[i])
    return

def data2():
  #  namelist_2017 = []
  #  opendatelist_2017 = []
  #  get_namelsit_opendatelist(namelist_2017,opendatelist_2017,"2017")
  #  count = 0
  #  for i in namelist_2017 :
   #     getBoxoffice_Viewr(i,opendatelist_2017[count])
   #     count+=1

   # return

 #   namelist_2016 = []
 #   opendatelist_2016 = []
 #   get_namelsit_opendatelist(namelist_2016,opendatelist_2016,"2016")
 #   count = 0
 #   for i in namelist_2016 :
 #       if count == 29:
#            break
#        if count == 13:
#            count = 14
#        getBoxoffice_Viewr(namelist_2016[count],opendatelist_2016[count],"2016")
#        count+=1


#    namelist_2015 = []
#    opendatelist_2015 = []
#    get_namelsit_opendatelist(namelist_2015,opendatelist_2015,"2015")
#    count = 0
#    for i in namelist_2015 :
#        getBoxoffice_Viewr(i,opendatelist_2015[count],"2015")
#        count+=1
#    return
#    getBoxoffice_Viewr("님아, 그 강을 건너지 마오","2014-11-27","2015")
    return


def get_star_rating (week):
    path_dir = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Review_"
    file_list = os.listdir(path_dir)
    file_list.sort()
    score = 0
    count = 0
    print(file_list)
    for file in file_list:
        df = pd.read_csv(path_dir+"/"+file,encoding='cp949',engine="python", error_bad_lines=False)
        for i in range(len(df.index)):
            if 1 == int(df.__getitem__(str(week)+'st_week')[i]):
                score = score + int(df.__getitem__('score')[i])
                count +=1
    return score / count



def get_numberofviewer (week):
    path_dir = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Name_Code"
    file_list = os.listdir(path_dir)
    file_list.sort()
    viewer_num = 0
    count = 0
    print(file_list)
    for file in file_list:
        df = pd.read_csv(path_dir+"/"+file,encoding='cp949',engine="python", error_bad_lines=False)
        if str(file) == "code_name_info_2016_w.csv":
            for i in range(28):
                viewer_num = viewer_num + int(df.__getitem__("week"+str(week)+"_num")[i])
                count+=1
        else:
            for i in range(29):
                viewer_num = viewer_num + int(df.__getitem__("week"+str(week)+"_num")[i])
                count+=1

    return viewer_num / count

def get_movie_star_rating (moviename,week):
    path_dir = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Review_"
    score = 0
    count = 0
    df = pd.read_csv(path_dir+"/"+moviename,encoding='cp949',engine="python", error_bad_lines=False)
    for i in range(len(df.index)):
        if 1 == int(df.__getitem__(str(week)+'st_week')[i]):
            score = score + int(df.__getitem__('score')[i])
            count +=1
    return score / count


def get_movie_viewer (moviname,week):
    path_dir = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Name_Code"
    df = pd.read_csv(path_dir+"/code_name_info_2017_w.csv",encoding='cp949',engine='python',error_bad_lines=False)
    no_name = 0
    for i in range(len(df.index)):
        if moviname == str(df.__getitem__("name")[i]):
            no_name = 0
            return int(df.__getitem__('week'+str(week)+"_num")[i])
        else:
            no_name = 1

    if no_name == 1 :
        df = pd.read_csv(path_dir+"/code_name_info_2016_w.csv",encoding='cp949',engine='python',error_bad_lines=False)
        no_name = 0
        for i in range(len(df.index)):
            if moviname == str(df.__getitem__("name")[i]):
                no_name = 0
                return int(df.__getitem__('week'+str(week)+"_num")[i])
            else:
                no_name = 1

    if no_name == 1 :
        df = pd.read_csv(path_dir+"/code_name_info_2015_w.csv",encoding='cp949',engine='python',error_bad_lines=False)
        no_name = 0
        for i in range(len(df.index)):
            if moviname == str(df.__getitem__("name")[i]):
                no_name = 0
                return int(df.__getitem__('week'+str(week)+"_num")[i])
            else:
                no_name = 1


def analysis():
    s = datetime.datetime.now()
    print("그래프를 그립니다ㅎㅎ 현재시간 : "+str(s))
    # week1_viewer = [4089391, 881679, 1768957, 3156859, 8083281, 3500982, 852500, 4548698, 3795042, 645363, 4281603, 6080649, 1732683, 955705, 2191691, 2249423, 1105601, 2995981, 805874, 3617655, 3589426, 1530102, 1176749, 240881, 995152, 1416160, 3835359, 1383739, 3550324, 620489, 4341321, 5441619, 5441619, 616614, 1049283, 6049842, 1842240, 3673466, 6643738, 2206565, 1803032, 1282366, 8412834, 846266, 1390849, 1315483, 3590519, 780607, 2063878, 952655, 798187, 2202170, 670999, 944457, 8539495, 1091745, 3137421, 1649352, 927060, 1599073, 6572526, 3232441, 1553055, 908986, 5245554, 1493047, 1121885, 793068, 1887218, 3151668, 1974264, 743111, 1223640, 3906404, 2004744, 1205804, 7937810, 5085521, 1002336, 1334084, 3113648, 2214824, 989152, 1142194, 856294, 2160082, 4220742]
    # week2_viewer = [1697568, 133421, 312265, 857434, 966019, 947691, 97063, 1142173, 2477348, 48925, 3471300, 385344, 306271, 75791, 438042, 257092, 247958, 726463, 186593, 157024, 1361416, 321321, 391073, 816526, 148293, 297776, 1155996, 179911, 1282364, 302073, 1297730, 1076481, 1076481, 232430, 90252, 854163, 369975, 1293726, 2400249, 302902, 203330, 170001, 1629987, 62005, 400245, 49470, 1980480, 61675, 409721, 149222, 27896, 512666, 75693, 185770, 2962892, 500101, 573998, 1220250, 200439, 442548, 2401205, 1463341, 248642, 74718, 984565, 119671, 164919, 207009, 379706, 526688, 405275, 92593, 199453, 927720, 407983, 177631, 2415174, 1195025, 195861, 23304, 822265, 460910, 122706, 55675, 83048, 525417, 2157289]
    # week3_viewer = [881337, 67656, 85699, 336450, 416529, 449159, 19387, 612984, 989485, 13027, 1935900, 88427, 64812, 13722, 186796, 52807, 31636, 270130, 59092, 51544, 1007509, 138074, 155168, 1342947, 23814, 39918, 280286, 27233, 473633, 113964, 744936, 513122, 513122, 94545, 13245, 388431, 126656, 877865, 1770109, 66103, 37298, 33467, 749498, 10552, 200275, 6168, 442034, 7914, 149259, 22260, 1890, 249661, 10230, 61360, 1341828, 101369, 344806, 271584, 65389, 107300, 1677311, 888993, 77313, 76399, 532116, 18502, 17935, 79827, 114237, 154542, 112850, 9959, 43674, 543177, 158253, 40606, 1015448, 662369, 39700, 2568, 465917, 174400, 15906, 5662, 14864, 243806, 706607]
    # week1_star_rating = [9.299, 7.54, 7.407, 8.447, 8.35, 8.606, 8.031, 7.627, 8.605, 9.026, 9.264, 5.03, 8.315, 7.706, 8.13, 7.232, 8.434, 8.027, 7.672, 7.971, 9.058, 9.124, 9.084, 9.782, 8.934, 8.056, 8.194, 7.451, 8.682, 9.574, 8.769, 8.129, 8.973, 8.569, 8.418, 8.051, 9.377, 9.21, 8.428, 7.996, 7.893, 7.959, 5.091, 7.557, 6.292, 8.029, 7.056, 7.976, 8.344, 6.762, 7.937, 9.126, 7.863, 8.209, 5.721, 7.32, 6.22, 9.392, 7.458, 8.191, 9.011, 9.161, 6.937, 8.708, 8.119, 8.067, 6.911, 8.99, 8.594, 7.911, 8.126, 8.461, 7.52, 8.812, 8.733, 8.031, 9.131, 8.496, 8.554, 7.865, 8.568, 7.892, 7.806, 6.744, 7.539, 8.601, 8.053]
    # week2_star_rating = [9.303, 6.322, 6.903, 8.589, 7.845, 8.309, 7.364, 7.75, 8.564, 8.803, 9.025, 5.868, 8.109, 7.502, 8.138, 7.362, 8.395, 7.842, 7.32, 8.134, 8.994, 9.046, 9.006, 9.655, 8.814, 8.286, 8.126, 7.692, 8.815, 9.465, 8.52, 8.274, 8.897, 8.329, 8.406, 8.091, 9.209, 9.093, 7.939, 7.799, 6.383, 8.136, 6.374, 7.62, 6.971, 8.195, 7.619, 7.518, 8.12, 6.092, 7.611, 9.245, 7.017, 7.749, 5.33, 7.248, 6.093, 9.368, 6.923, 7.853, 9.028, 9.142, 7.196, 8.264, 8.196, 8.18, 6.352, 8.767, 8.482, 7.505, 8.097, 8.164, 6.905, 8.623, 8.65, 8.037, 9.115, 8.461, 8.479, 6.694, 8.483, 7.793, 6.412, 5.657, 7.181, 8.453, 8.195]
    # week3_star_rating = [9.274, 6.293, 7.163, 8.609, 7.767, 8.376, 6.45, 7.563, 8.409, 8.637, 9.084, 6.238, 8.222, 6.897, 8.413, 8.456, 8.106, 7.514, 7.316, 8.174, 9.026, 8.928, 8.979, 9.432, 8.629, 8.161, 8.271, 7.641, 8.056, 9.355, 8.571, 8.259, 8.8, 8.358, 8.497, 8.02, 9.241, 9.096, 7.098, 7.774, 7.116, 8.301, 7.45, 7.668, 6.369, 8.228, 5.971, 7.907, 8.315, 5.837, 7.85, 9.192, 7.366, 7.769, 6.628, 7.067, 6.3, 9.304, 6.914, 7.947, 9.049, 9.117, 6.863, 8.45, 8.277, 7.341, 6.466, 8.899, 8.629, 7.619, 8.235, 8.339, 6.626, 8.543, 8.735, 7.863, 9.141, 8.287, 8.55, 7.176, 8.58, 7.581, 6.791, 5.791, 7.439, 8.506, 7.974]
    week1_viewer= []
    week2_viewer= []
    week3_viewer= []
    week1_star_rating=[]
    week2_star_rating=[]
    week3_star_rating=[]

    ############################ 전체 영화별 각주차 평점 ####################################
    #
    # path_dir = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Review_"
    # file_list = os.listdir(path_dir)
    # file_list.sort()

    # week1_star_rating = []
    # week2_star_rating = []
    # week3_star_rating = []

    # file_list.remove(file_list[13])
    # print(file_list)
    #
    # for file in file_list:
    #     week1_star_rating.append(round(get_movie_star_rating(file,week=1),3))
    #     week2_star_rating.append(round(get_movie_star_rating(file,week=2),3))
    #     week3_star_rating.append(round(get_movie_star_rating(file,week=3),3))
    #
    #######################################################################################

    ############################ 비흥행 영화 각주차 평점 ######################################
    # file_list = ["불한당 나쁜 놈들의 세상_review__154112___2017.csv","고산자, 대동여지도_review__133129___2016.csv","좋아해줘_review__136893___2016.csv"
    #              ,"스플릿_review__146512___2016.csv","국가대표 2_review__141824___2016.csv","미쓰 와이프_review__129406___2015.csv","허삼관_review__112268___2015.csv"
    #              ,"님아, 그 강을 건너지 마오_review__130013___2015.csv","살인의뢰_review__122916___2015.csv","손님_review__122984___2015.csv","기술자들_review__117790___2015.csv"]
    #
    # for file in file_list:
    #      week1_star_rating.append(round(get_movie_star_rating(file,week=1),3))
    #      week2_star_rating.append(round(get_movie_star_rating(file,week=2),3))
    #      week3_star_rating.append(round(get_movie_star_rating(file,week=3),3))
    #
    # print("star rating 1 2 3")
    # print(week1_star_rating)
    # print(week2_star_rating)
    # print(week3_star_rating)

    #######################################################################################
    ############################# 흥행 영화 각주차 평점 #######################################

    path_dir = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Review_"
    file_list = ["더 킹_review__144314___2017.csv","청년경찰_review__153652___2017.csv","군함도_review__146506___2017.csv","범죄도시_review__161242___2017.csv",
                 "공조_review__142384___2017.csv","신과함께-죄와 벌_review__85579___2017.csv","택시운전사_review__146469___2017.csv","부산행_review__130966___2016.csv",
                 "검사외전_review__130903___2016.csv","밀정_review__137952___2016.csv","터널_review__141104___2016.csv",
                 "인천상륙작전_review__142822___2016.csv","럭키_review__140695___2016.csv","곡성_review__121051___2016.csv","덕혜옹주_review__94767___2016.csv",
                 "베테랑_review__115977___2015.csv","암살_review__121048___2015.csv","국제시장_review__102875___2015.csv","내부자들_review__121788___2015.csv",
                 "사도_review__121922___2015.csv","연평해전_review__102272___2015.csv","검은 사제들_review__120157___2015.csv","히말라야_review__100647___2015.csv"]
    file_list.sort()
    for file in file_list:
         week1_star_rating.append(round(get_movie_star_rating(file,week=1),3))
         week2_star_rating.append(round(get_movie_star_rating(file,week=2),3))
         week3_star_rating.append(round(get_movie_star_rating(file,week=3),3))

    print(week1_star_rating)
    print(week2_star_rating)
    print(week3_star_rating)
    ########################################################################################
    ########################### 영화별 각주차 입장객 #########################################
    # path_dir = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Name_Code"
    # info_file_list = os.listdir(path_dir)
    # data_list = []

    # week1_viewer = []
    # week2_viewer = []
    # week3_viewer = []

    # for file in info_file_list:
    #     df = pd.read_csv(path_dir+"/"+file,encoding='cp949',engine="python", error_bad_lines=False)
    #     for i in df.index :
    #         if 'nan' == str(df.__getitem__("name")[i]):
    #             print("_")
    #         else:
    #             data_list.append(df.__getitem__("name")[i])
    #
    #
    # data_list.sort()
    #
    # data_list.remove(data_list[13])
    # for moviename in data_list:
    #     week1_viewer.append(round(get_movie_viewer(moviename,1),3))
    #     week2_viewer.append(round(get_movie_viewer(moviename,2),3))
    #     week3_viewer.append(round(get_movie_viewer(moviename,3),3))
    #######################################################################################

    ########################### 비흥행 각주차 입장객 #########################################
    # data_list = ['불한당: 나쁜 놈들의 세상','고산자, 대동여지도','좋아해줘','스플릿','국가대표 2','미쓰 와이프','허삼관','님아, 그 강을 건너지 마오','살인의뢰','손님','기술자들']
    # for moviename in data_list:
    #      week1_viewer.append(round(get_movie_viewer(moviename,1),3))
    #      week2_viewer.append(round(get_movie_viewer(moviename,2),3))
    #      week3_viewer.append(round(get_movie_viewer(moviename,3),3))
    #
    # print("number of viewer 1 2 3")
    # print(week1_viewer)
    # print(week2_viewer)
    # print(week3_viewer)

    ########################################################################################

    ############################# 흥행 각주차 입장객 ##########################################
    data_list = ["택시운전사","신과함께-죄와 벌","공조","범죄도시","군함도","청년경찰","더 킹",
                 "부산행","검사외전","밀정","터널","인천상륙작전","럭키","곡성","덕혜옹주",
                 "베테랑","암살","국제시장","내부자들","사도","연평해전","검은 사제들","히말라야"]

    data_list.sort()

    for moviename in data_list:
         week1_viewer.append(round(get_movie_viewer(moviename,1),3))
         week2_viewer.append(round(get_movie_viewer(moviename,2),3))
         week3_viewer.append(round(get_movie_viewer(moviename,3),3))

    print("number of viewer 1 2 3")
    print(week1_viewer)
    print(week2_viewer)
    print(week3_viewer)

    ########################################################################################


    e=datetime.datetime.now()
    print("끝났습니다. 소요된시간 : "+str(e-s))
    # print("비흥행")
    # draw_table(week1_viewer,week2_viewer,week3_viewer,week1_star_rating,week2_star_rating,week3_star_rating)
    # draw_graph(week1_viewer,week2_viewer,week3_viewer,week1_star_rating,week2_star_rating,week3_star_rating)

    print("흥행")
    draw_table(week1_viewer,week2_viewer,week3_viewer,week1_star_rating,week2_star_rating,week3_star_rating)
    draw_graph(week1_viewer,week2_viewer,week3_viewer,week1_star_rating,week2_star_rating,week3_star_rating)
    #
    # print("전체")
    # week1_viewer = [4089391, 881679, 1768957, 3156859, 8083281, 3500982, 852500, 4548698, 3795042, 645363, 4281603, 6080649, 1732683, 955705, 2191691, 2249423, 1105601, 2995981, 805874, 3617655, 3589426, 1530102, 1176749, 240881, 995152, 1416160, 3835359, 1383739, 3550324, 620489, 4341321, 5441619, 5441619, 616614, 1049283, 6049842, 1842240, 3673466, 6643738, 2206565, 1803032, 1282366, 8412834, 846266, 1390849, 1315483, 3590519, 780607, 2063878, 952655, 798187, 2202170, 670999, 944457, 8539495, 1091745, 3137421, 1649352, 927060, 1599073, 6572526, 3232441, 1553055, 908986, 5245554, 1493047, 1121885, 793068, 1887218, 3151668, 1974264, 743111, 1223640, 3906404, 2004744, 1205804, 7937810, 5085521, 1002336, 1334084, 3113648, 2214824, 989152, 1142194, 856294, 2160082, 4220742]
    # week2_viewer = [1697568, 133421, 312265, 857434, 966019, 947691, 97063, 1142173, 2477348, 48925, 3471300, 385344, 306271, 75791, 438042, 257092, 247958, 726463, 186593, 157024, 1361416, 321321, 391073, 816526, 148293, 297776, 1155996, 179911, 1282364, 302073, 1297730, 1076481, 1076481, 232430, 90252, 854163, 369975, 1293726, 2400249, 302902, 203330, 170001, 1629987, 62005, 400245, 49470, 1980480, 61675, 409721, 149222, 27896, 512666, 75693, 185770, 2962892, 500101, 573998, 1220250, 200439, 442548, 2401205, 1463341, 248642, 74718, 984565, 119671, 164919, 207009, 379706, 526688, 405275, 92593, 199453, 927720, 407983, 177631, 2415174, 1195025, 195861, 23304, 822265, 460910, 122706, 55675, 83048, 525417, 2157289]
    # week3_viewer = [881337, 67656, 85699, 336450, 416529, 449159, 19387, 612984, 989485, 13027, 1935900, 88427, 64812, 13722, 186796, 52807, 31636, 270130, 59092, 51544, 1007509, 138074, 155168, 1342947, 23814, 39918, 280286, 27233, 473633, 113964, 744936, 513122, 513122, 94545, 13245, 388431, 126656, 877865, 1770109, 66103, 37298, 33467, 749498, 10552, 200275, 6168, 442034, 7914, 149259, 22260, 1890, 249661, 10230, 61360, 1341828, 101369, 344806, 271584, 65389, 107300, 1677311, 888993, 77313, 76399, 532116, 18502, 17935, 79827, 114237, 154542, 112850, 9959, 43674, 543177, 158253, 40606, 1015448, 662369, 39700, 2568, 465917, 174400, 15906, 5662, 14864, 243806, 706607]
    # week1_star_rating = [9.299, 7.54, 7.407, 8.447, 8.35, 8.606, 8.031, 7.627, 8.605, 9.026, 9.264, 5.03, 8.315, 7.706, 8.13, 7.232, 8.434, 8.027, 7.672, 7.971, 9.058, 9.124, 9.084, 9.782, 8.934, 8.056, 8.194, 7.451, 8.682, 9.574, 8.769, 8.129, 8.973, 8.569, 8.418, 8.051, 9.377, 9.21, 8.428, 7.996, 7.893, 7.959, 5.091, 7.557, 6.292, 8.029, 7.056, 7.976, 8.344, 6.762, 7.937, 9.126, 7.863, 8.209, 5.721, 7.32, 6.22, 9.392, 7.458, 8.191, 9.011, 9.161, 6.937, 8.708, 8.119, 8.067, 6.911, 8.99, 8.594, 7.911, 8.126, 8.461, 7.52, 8.812, 8.733, 8.031, 9.131, 8.496, 8.554, 7.865, 8.568, 7.892, 7.806, 6.744, 7.539, 8.601, 8.053]
    # week2_star_rating = [9.303, 6.322, 6.903, 8.589, 7.845, 8.309, 7.364, 7.75, 8.564, 8.803, 9.025, 5.868, 8.109, 7.502, 8.138, 7.362, 8.395, 7.842, 7.32, 8.134, 8.994, 9.046, 9.006, 9.655, 8.814, 8.286, 8.126, 7.692, 8.815, 9.465, 8.52, 8.274, 8.897, 8.329, 8.406, 8.091, 9.209, 9.093, 7.939, 7.799, 6.383, 8.136, 6.374, 7.62, 6.971, 8.195, 7.619, 7.518, 8.12, 6.092, 7.611, 9.245, 7.017, 7.749, 5.33, 7.248, 6.093, 9.368, 6.923, 7.853, 9.028, 9.142, 7.196, 8.264, 8.196, 8.18, 6.352, 8.767, 8.482, 7.505, 8.097, 8.164, 6.905, 8.623, 8.65, 8.037, 9.115, 8.461, 8.479, 6.694, 8.483, 7.793, 6.412, 5.657, 7.181, 8.453, 8.195]
    # week3_star_rating = [9.274, 6.293, 7.163, 8.609, 7.767, 8.376, 6.45, 7.563, 8.409, 8.637, 9.084, 6.238, 8.222, 6.897, 8.413, 8.456, 8.106, 7.514, 7.316, 8.174, 9.026, 8.928, 8.979, 9.432, 8.629, 8.161, 8.271, 7.641, 8.056, 9.355, 8.571, 8.259, 8.8, 8.358, 8.497, 8.02, 9.241, 9.096, 7.098, 7.774, 7.116, 8.301, 7.45, 7.668, 6.369, 8.228, 5.971, 7.907, 8.315, 5.837, 7.85, 9.192, 7.366, 7.769, 6.628, 7.067, 6.3, 9.304, 6.914, 7.947, 9.049, 9.117, 6.863, 8.45, 8.277, 7.341, 6.466, 8.899, 8.629, 7.619, 8.235, 8.339, 6.626, 8.543, 8.735, 7.863, 9.141, 8.287, 8.55, 7.176, 8.58, 7.581, 6.791, 5.791, 7.439, 8.506, 7.974]
    # draw_table(week1_viewer,week2_viewer,week3_viewer,week1_star_rating,week2_star_rating,week3_star_rating)
    # draw_graph(week1_viewer,week2_viewer,week3_viewer,week1_star_rating,week2_star_rating,week3_star_rating)
    return

def correlation (viewer, star_rating):
    index = len(viewer)
    print(index)
    mean_1v = numpy.mean(viewer)
    mean_1s = numpy.mean(star_rating)

    aver = numpy.ones(index)

    avg_1v = aver * mean_1v
    avg_1s = aver * mean_1s

    sss = (viewer-avg_1v)*(star_rating-avg_1s)
    sssS = sum(sss)

    ppp = numpy.std(viewer)*numpy.std(star_rating)
    cor = sssS/(index*ppp)

    return cor

def draw_graph(week1_viewer,week2_viewer,week3_viewer,week1_star_rating,week2_star_rating,week3_star_rating):
    f = plt.figure()
    f.subplots_adjust(left=0.030, bottom=0.070, right=0.990, top=0.960, wspace=0.250, hspace=0.4)
    w1_w1 = f.add_subplot(3,3,1)
    w1_w2 = f.add_subplot(3,3,4)
    w2_w2 = f.add_subplot(3,3,5)
    w1_w3 = f.add_subplot(3,3,7)
    w2_w3 = f.add_subplot(3,3,8)
    w3_w3 = f.add_subplot(3,3,9)


    w1_w1.set_xlabel("1st Week Star rationg")
    w1_w1.set_ylabel("1st Week Viewer num")
    w1_w1.scatter(week1_star_rating,week1_viewer)

    w1_w2.set_xlabel("1st Week Star rationg")
    w1_w2.set_ylabel("2st Week Viewer num")
    w1_w2.scatter(week1_star_rating,week2_viewer)

    w2_w2.set_xlabel("2st Week Star rationg")
    w2_w2.set_ylabel("2st Week Viewer num")
    w2_w2.scatter(week2_star_rating,week2_viewer)

    w1_w3.set_xlabel("1st Week Star rationg")
    w1_w3.set_ylabel("3st Week Viewer num")
    w1_w3.scatter(week1_star_rating,week3_viewer)

    w2_w3.set_xlabel("2st Week Star rationg")
    w2_w3.set_ylabel("3st Week Viewer num")
    w2_w3.scatter(week2_star_rating,week3_viewer)

    w3_w3.set_xlabel("3st Week Star rationg")
    w3_w3.set_ylabel("3st Week Viewer num")
    w3_w3.scatter(week3_star_rating,week3_viewer)

    plt.show()
    return

def draw_table(week1_viewer,week2_viewer,week3_viewer,week1_star_rating,week2_star_rating,week3_star_rating):
    w1_w1_c = correlation(week1_viewer,week1_star_rating)
    w2_w1_c = correlation(week2_viewer,week1_star_rating)
    w2_w2_c = correlation(week2_viewer,week2_star_rating)
    w3_w1_c = correlation(week3_viewer,week1_star_rating)
    w3_w2_c = correlation(week3_viewer,week2_star_rating)
    w3_w3_c = correlation(week3_viewer,week3_star_rating)

    data = {'week1 star rating':[w1_w1_c,w2_w1_c,w3_w1_c],
            'week2 star rating':['Nan',w2_w2_c,w3_w2_c],
            'week3 star rating':['Nan','Nan',w3_w3_c]}


    corrdf = DataFrame(data,columns=['week1 star rating','week2 star rating','week3 star rating'],
                       index=['week1 numberof viewer','week2 numberof viewer','week3 numberof viewer'])
    print(corrdf)
    return

    #print("택시운전사 2주차 별점평균 : " +str(get_movie_star_rating("택시운전사_review__146469___2017",week=2)))
    #print("택시운전사 3주차 별점평균 : " +str(get_movie_star_rating("택시운전사_review__146469___2017",week=3)))

    #print("1주차 별점 평균 : "+str(get_star_rating(week=1)))
    #print("2주차 별점 평균 : "+str(get_star_rating(week=2)))
    #print("3주차 별점 평균 : "+str(get_star_rating(week=3)))

    #print("2주차 입장객 평균 : "+str(get_numberofviewer(week=2)))
    #print("3주차 입장객 평균 : "+str(get_numberofviewer(week=3)))

    e=datetime.datetime.now()

def postiv_negativ():
    return

def postiv() :
    review_path = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Review_"
    postiv_path = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Postiv"
    review_list = os.listdir(review_path)
    review_list.sort()

   # filenames =

    return

if __name__ == '__main__':
    #data1()    # 데이터 1차 수집 전처리
    #data2()    # 데이터 2차 수집 전처리
    #analysis()

