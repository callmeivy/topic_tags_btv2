#coding=UTF-8
'''
Updated on 6 June,2017
北京台新闻推荐部分
@author: Ivy
为LDA准备reuters.tokens、tokens.txt、list_of_lists.txt、reuters.titles：
tokens文档在root_directory_lda目录下
reuters.titles在root_directory_lda目录下
list_of_lists在/usr/jincan目录下
'''
import os
import os.path
import jieba
import MySQLdb
from sys import path
path.append('tools/')
path.append('/usr/local/lib/python2.7/site-packages/lda/tests/')
path.append(path[0]+'/tools')
from collections import Counter
from json import JSONDecoder
import sys
import shutil
import time
import math
import string
import nltk
from nltk.corpus import stopwords
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
root_directory = 'D:\\tmp'
root_directory_lda = 'C:\Python27\Lib\site-packages\lda\\tests'
title_box = list()
import re
import json
import cPickle
import lda
import datetime
from collections import defaultdict
import numpy as np
from nltk.corpus import stopwords
import textmining
import jieba.posseg as pseg
import MainProgram

def corpus_to_list():
    # stopwords
    dicFile = open('stopwords.txt','r')
    stopwords = dicFile.readlines()
    stopwordList = []
    stopwordList.append(' ')
    for stopword in stopwords:
        temp = stopword.strip().replace('\r\n', '').decode('utf8')
        stopwordList.append(temp)
    dicFile.close()
    valid = ['ns', 'vn','n','nz','eng','nr','nrt']
    # channel = ["CCTV5"]
    # channel = ["CCTV","CCTV-阿语","CCTV1","CCTV10","CCTV11","CCTV12","CCTV13","CCTV14","CCTV15","CCTV2","CCTV3",\
    #            "CCTV4","CCTV5","CCTV6","CCTV7","CCTV9","QINGXUANZE","WEIBO","WEIXIN","zgdsb","ZHONGGUODIANSHIBAO",\
    #            "中国电视报","央视","央视专区","央视科技","测试"]
    # channel = ["CCTV2","WEIBO", "WEIXIN"]
    channel = ["CCTV5"]
    sqlConn = MySQLdb.connect(host='192.168.168.105', user='root', passwd='', db='cctv', charset='utf8')
    sqlcursor = sqlConn.cursor()
    tdm = textmining.TermDocumentMatrix()
    delset = string.punctuation
    a = list()
    for one_type in channel:
        one_type_text = list()
        print one_type
        word_box = list()
        word_nominal = dict()
        # id标识，剩余的做测试;数据中有许多“测试”用的，过滤掉;根据id每个类别取90%作为训练集，剩余的是测试集
        # sqlcursor.execute(
        #     '''SELECT count(*) from q_test where channel =  "%s" and length(content) >0 and ti NOT REGEXP '测试|test';''' % (one_type))
        # total = list(sqlcursor.fetchone())[0]
        # base_number_id_index = int(total*0.9)
        # 像CCTV2,新闻特别多，就写0.06吧
        # base_number_id_index = int(total * 0.06)
        # sqlcursor.execute('''SELECT id from q_test where channel =  "%s" and length(content) >0 and ti NOT REGEXP '测试|test';''' % (one_type))
        # id = str(list(sqlcursor.fetchall())).replace("(", "")
        # id = id.replace("[", "")
        # id = id.replace("L", "")
        # id = id.replace("]", "")
        # id = sorted(map(eval, id.replace(",)", "").split(",")))
        # base_number_id_end = id[base_number_id_index*3]
        # base_number_id_end_2 = id[base_number_id_index * 4]
        # id标识，剩余的做测试;数据中有许多“测试”用的，过滤掉
        # sqlcursor.execute('''SELECT ti,content from q_test where channel =  "%s" and id >= "%s" and length(content) >0 and ti NOT REGEXP '测试|test';''' % (one_type, base_number_id_end))
        # sqlcursor.execute('''SELECT ti,content from q_test where channel =  "%s" and id < "%s" and id > "%s" and length(content) >0 and ti NOT REGEXP '测试|test' limit 2;''' %(one_type, base_number_id_end_2,base_number_id_end))
        # sqlcursor.execute('''SELECT ti,content from q_test where channel =  "%s" and id > "%s" and length(content) >0 and ti NOT REGEXP '测试|test' limit 2;''' %(one_type, 85076))
        # sqlcursor.execute('''SELECT ti,content from q_test where channel =  "%s" and length(content) >0 and ti NOT REGEXP '测试|test';''' %(one_type))
        # 含网址的内容删去
        sqlcursor.execute('''SELECT ti,content from q_test where channel =  "%s" and length(content) >0 and length(ti) > 0 and content NOT REGEXP 'http://|测试|test' and ti NOT REGEXP '测试|test';''' %(one_type))
        traindata = list(sqlcursor.fetchall())
        ind = 0
        print "doc number:",len(traindata)
        all_docs_to_lists = list()
        allDoc_coma_join_lists = list()
        title_box =list()
        tdms = list()
        for PubTitle,Storyline in traindata:
            word_box_single = list()
            if PubTitle not in title_box:
                ind += 1
                title_box.append(PubTitle)
                full_text = str(Storyline) + str(PubTitle)
                one_type_text.append(full_text)
                # full_text = full_text.replace("\n", "")
                # full_text = full_text.translate(None, delset)
                # full_text = jieba.cut(full_text, cut_all=False)
                full_text = pseg.cut(full_text)
                for i in full_text:
                    if i.word not in stopwordList:
                        # if len(i) == 0:
                        #     print 'kkk',i
                        if len(i.word) > 1:
                            # if (i != "test") and (i != "title") and (i != "content") and (i != "description") and (i != "time") and (len(i) != 8):
                                # if chara in valid:
                            if i.flag in valid:
                                word_box.append(i.word)
                                word_nominal[i.word]=i.flag
                                word_box_single.append(i.word)
                word_box_str = ','.join(word_box_single)
                all_docs_to_lists.append(word_box_single)
                allDoc_coma_join_lists.append(word_box_str)

        print '总共多少篇', ind, len(title_box)
        # 以下准备reuters.titles
        title_file = open(root_directory_lda+'/reuters.titles', 'w+')
        mark3 = 0
        # docs_total = ind

        if len(title_box) ==0:
            # print("{} (top topic: {})".format(doc_topic[i].argmax(), titles[i]))
            print ("{} (category has NO news.)".format(one_type))
            continue
        for one_title in title_box:
            mark3 += 1
            if mark3 != len(title_box):
                title_file.write("%s\n" % str(one_title).encode('utf-8'))
            else:
                title_file.write("%s" % str(one_title).encode('utf-8'))
        title_file.close()
        print 'reuters.titles is ready-----------------------------------------------------------'

        # 以下准备tokens
        # 只留更有意义的词，像动词形容词啥的都删去了
        ffile = open(root_directory_lda + '/reuters.tokens', 'w+')
        docs_key_words = MainProgram.key_word_priority(one_type_text)
        count = 0
        sum = 0
        count_invalid = 0
        for i in range(0, len(docs_key_words)):
            sum += len(docs_key_words[i])
        word_already = list()
        for i in range(0, len(docs_key_words)):
            for word in docs_key_words[i]:
                count += 1
                nominal = word_nominal.get(word)
                if nominal not in valid:
                    # count += 1
                    # print word, nominal
                    continue
                # list最后一个元素才不换行，定位list最后元素就行
                if count == sum:
                    ffile.write("%s" % word.encode('utf-8'))
                else:
                    if word not in word_already:
                        ffile.write("%s\n" % word.encode('utf-8'))
                        word_already.append(word)
        ffile.close()
        print 'reuters.tokens is ready-----------------------------------------------------------'


        list_of_lists_file = open(root_directory+'/list_of_lists.txt', 'w+')
        mark = 0
        print 'len(allDoc_coma_join_lists)',len(allDoc_coma_join_lists)
        for one in allDoc_coma_join_lists:
            mark += 1
            if mark != ind:
                list_of_lists_file.write("%s\n" % one.encode('utf-8'))
            else:
                list_of_lists_file.write("%s" % one.encode('utf-8'))
        list_of_lists_file.close()
        print "mark",mark
        print "list_of_lists.txt is ready"

        execfile('docToMatrix.py')
        execfile('formal_matrix_title.py')
        excuteldamodel(mysqlhostIP='192.168.168.105', how_many_topics = 7, how_many_iteration=100, how_many_topic_words = 30,catcat = one_type,
                       dbname='cctv', )

def excuteldamodel(mysqlhostIP, how_many_topics, how_many_iteration, how_many_topic_words,catcat,mysqlUserName = 'root', mysqlPassword = '', dbname = 'cctv'):
    # valid = ['NN', 'NNS', 'NNP', 'NNPS']
    X = lda.datasets.load_reuters()
    vocab = lda.datasets.load_reuters_vocab()
    titles = lda.datasets.load_reuters_titles()
    title_no = dict()
    vv=0
    # 将文章标题与序号存成字典
    for i in range(len(titles)):
        title_no[i] = titles[i]
    createTime = datetime.datetime.now()
    model = lda.LDA(n_topics = how_many_topics, n_iter = how_many_iteration, random_state = 1)
    model.fit(X)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works
    mysqlconn = MySQLdb.connect(host=mysqlhostIP, user=mysqlUserName, passwd=mysqlPassword, db = dbname, charset='utf8')
    mysqlcursor = mysqlconn.cursor()
    mysqltopic = 'topic_attri'
    mysqlcursor.execute('''CREATE TABLE IF NOT EXISTS top_topic_trend_week(
            pk bigint NOT NULL PRIMARY KEY AUTO_INCREMENT, category VARCHAR(50), topic_id VARCHAR(200), core_vector\
             varchar(250), key_words VARCHAR(500), news_under_topic text, period varchar(20), created_date datetime) charset=utf8''')
    # mysqlcursor.execute('''CREATE TABLE IF NOT EXISTS topic_populaity_v2(
    #         pk bigint NOT NULL PRIMARY KEY AUTO_INCREMENT, topic varchar(50), key_words VARCHAR(50), date DATE, popularity bigint(20), rank bigint(20), pic VARCHAR(250),\
    #          created_date datetime, topic_id VARCHAR(250), program_id varchar(50)) charset=utf8''')
    # 添加索引
    # mysqlcursor.execute('''ALTER TABLE top_topic_trend_summary ADD INDEX index_name_soo( `key_words`, `pk`, `topic_id` )''')
# 以下是各个主题下新闻的列表
    title_topic = defaultdict(list)
    doc_topic = model.doc_topic_
    def isValid(position, rate):
        topicRate = doc_topic[position]
        valid = False
        for i in range(len(topicRate)):
            if topicRate[i] > rate:
                valid = True
                break
        return valid

    count_c = 0
    for i in range(len(titles)):
        # 如果阈值过高，有可能发生某个topic下新闻条数为0的情况
        # 0.7以上，根据最高概率来；0.7以下（未完成)，用户手动判断
        if isValid(i, 0.7):
            count_c += 1
            title_topic[doc_topic[i].argmax()].append(titles[i])
        # print("{} (top topic: {})".format(doc_topic[i].argmax(),titles[i]))
    tempInsert_topic_title = list()
    # title_box = list()
    already_title = list()
    print "heyhey", count_c
    doc_topic_probability = model.fit_transform(X)
    max_title_index = doc_topic_probability.argmax(axis=0)
    doc_topic_again = list(model.fit_transform(X))
    thefile = open(('values_week %s.txt' %(catcat)), 'w+')
    thefile.write("LDA有效比例(主题概率分布显著)为 %s：其中划入主题范围的新闻数为%s,总新闻数为%s\n"% (round(float(count_c)/float(len(titles)),2),count_c,len(titles)))
    for ii in doc_topic_again:
        thefile.write("%s\n" % str(ii).encode('utf-8'))
    thefile.close()
    tempInsert = list()
    topic_dict = dict()
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-how_many_topic_words:-1]
        bag_of_words = ' '.join(topic_words)
        topic_dict[i] = (str(bag_of_words))
        # print "hhah", i, topic_dist
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-how_many_topic_words:-1]
        # print "ssss",type(topic_words)
        # print topic_words
        # words = pseg.cut("我爱北京天安门")
        # for w in words:
        #     print w.word, w.flag
        # bag_of_words = ' '.join(topic_words)
        # topic_dict[i] = (str(bag_of_words))
        # topic,最能代表该topic的文章代码
        number = max_title_index[i]
        title_utmost = title_no[number]
        # category
        tempInsert.append(catcat)
        # topic number
        tempInsert.append(i)
        tempInsert.append(str(title_utmost))
        # key_words,bag_of_words
        word_list = list()
        # tokens = nltk.word_tokenize(bag_of_words)
        # tags = nltk.pos_tag(tokens)
        # 词袋
        # for word, flag in tags:
        #     if flag in valid:
        #         print word,flag
        #         word_list.append(word)
        # bag_of_words = ' '.join(word_list)
        tempInsert.append(str(bag_of_words))
        # 文章的date
        # 该topic所含的新闻MID
        for k, v in title_topic.items():
            if k ==i:
                news_under_topic = ";".join(v)
                tempInsert.append(news_under_topic)
        # 数据插入时间段
        tempInsert.append('no_time_period')
        # 数据插入时间
        tempInsert.append(createTime)
        mysqlcursor.execute("insert into top_topic_trend_week(category,topic_id, core_vector, key_words, news_under_topic, period, created_date) values (%s, %s, %s, %s, %s, %s, %s)", tempInsert)
        tempInsert = list()
        mysqlconn.commit()
    mysqlconn.close()

if __name__=='__main__':
    result = corpus_to_list()