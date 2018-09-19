from konlpy.tag import Twitter
from collections import Counter
import re
import os
import pandas as pd
def postiv_negativ():
    postiv()
    return

def postiv() :
    review_path = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Review_"
    postiv_path = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Postiv"
    review_list = os.listdir(review_path)
    review_list.sort()

    file = "C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/Review_/택시운전사_review__146469___2017.csv"
    post_message =""
    negat_message  =""
    df = pd.read_csv(file, encoding='cp949', engine='python', error_bad_lines=False)
    for i in range(len(df.index)):
        if  7 <= int(df.__getitem__("score")[i]):
            post_message= post_message + re.sub(r'[^\w]','',str(df.__getitem__("reple")[i]))+''
        elif 4 >= int(df.__getitem__("score")[i]):
            print("d")
            negat_message= negat_message + re.sub(r'[^\w]','',str(df.__getitem__("reple")[i]))+''
    print(negat_message[:500])
    nega_nlp = Twitter()
    nega_nous = nega_nlp.nouns(negat_message)
    nega_count =  Counter(nega_nous)
    po_tag_list = []
    po_co_list = []
    ne_tag_list = []
    ne_co_list = []
    for tags,counts in nega_count.most_common(50):
        if len(str(tags)) > 1:
            ne_tag_list.append(tags)
            ne_co_list.append(counts)
            print("%s : %d"%(tags,counts))
    post_nlp = Twitter()
    pos_nouns = post_nlp.nouns(post_message)
    pos_count = Counter(pos_nouns)

    print(ne_tag_list)

    for tags,counts in pos_count.most_common(50):
        if len(str(tags)) > 1:
            po_tag_list.append(tags)
            po_co_list.append(counts)
            print("%s : %d"%(tags,counts))
            
    post_nlp = Twitter()
    pos_nouns = post_nlp.nouns(post_message)
    pos_count = Counter(pos_nouns)
    
    for tags,counts in pos_count.most_common(50):
        if len(str(tags)) > 1:
            print("%s : %d"%(tags,counts))
    print("---------------------------------------------------------------")
    print("count 추출중")

    r_ne_list = []
    r_po_list = []
    for po in po_tag_list:
        if po not in ne_tag_list:
            r_po_list.append(po)
    for ne in ne_tag_list:
        if ne not in po_tag_list:
            r_ne_list.append(ne)
    
    print("ㄹㅇ 긍정")
    print(r_po_list)
    print("ㄹㅇ 부정")
    print(r_ne_list)
    return 
    #if "Adjective" in str(tags):



def test():
    pos_list = ['최고', '가슴', '한번', '꼭봐', '마음', '다시', '운전사', '생각', '우리', '실화', '시간', '역시', '그날', '지금', '전두환', '국민', '여운', '기자', '대한민국']
    neg_list = ['폭동', '미화', '감성', '그냥', '선동', '팔이', '정치', '소재', '별로', '억지', '노잼', '군인', '역사왜곡', '스토리', '한국영', '전라도', '좌파', '신파', '정도', '전형', '수준']
    pf = open("C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/diction/po_dic.txt","w")
    for dic in pos_list:
        data = dic + "\n"
        pf.write(data)
    nf = open("C:/Users/Jeong/Desktop/ENP_PROJECT/DATA/diction/ne_dic.txt","w")
    for dic in neg_list:
        data = dic + "\n"
        nf.write(data)
    return

if __name__ == '__main__':
    #data1()    # 데이터 1차 수집 전처리
    #data2()    # 데이터 2차 수집 전처리
    #analysis()
    #postiv_negativ() # 승훈이형 컴퓨터에서 작업 ㅠㅜㅜㅜ
    test()

