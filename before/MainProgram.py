#coding=UTF-8
#Python Version: 2.7

#Importing necessary libraries
import collections
import re
import operator
#Importing necessary files
import Mytfidf
# import rake
import AKE
import collections
import MySQLdb


def get_one_topic_doc():
    sqlConn = MySQLdb.connect(host='192.168.168.105', user='root', passwd='', db='cctv', charset='utf8')
    sqlcursor = sqlConn.cursor()
    # sqlcursor.execute("ALTER TABLE q_test ADD INDEX index_name_many_2(content)")
    # channel = ["央视专区", "央视科技"]
    channel = ["cctv5"]
    for one_type in channel:
        print one_type
        # sqlcursor.execute(
        #     '''select news_under_topic from top_topic_trend_summary where period = 'no_time_period' and category = "%s";''' % (
        #     one_type.encode('utf-8')))
        # sqlcursor.execute(
        #     '''select news_under_topic from top_topic_trend_summary where period = 'no_time_period' and category = "%s" limit 1;''' % (
        #         one_type.encode('utf-8')))
        sqlcursor.execute('''select news_under_topic from top_topic_trend_summary where pk=142 limit 1;''' )
        summary_data = list(sqlcursor.fetchall())
        print 'topic number:',len(summary_data)
        topic_content = list()
        topic_dgree = dict()
        for topics in summary_data:

            titles = topics[0].split(';')
            # TOPIC中选择2篇文章
            # titles = topics[0].split(';')[:2]
            # print len(titles)
            for doc in titles:
                if "'" in doc:
                    doc = doc.replace("'", "\\'")
                sqlcursor.execute(
                    "select content from q_test where ti = '%s' and channel = '%s' limit 1" % (doc, one_type))
                # print "select Storyline from cctv_news_content where PubTitle = '%s' limit 1" %(doc,)
                Storyline = list(sqlcursor.fetchall())
                topic_content.append(Storyline[0][0])
        print "summary reading is done!"
    return topic_content

def key_word_priority(completeComment):
    # completeComment = ["中共中央总书记、国家主席、中央军委主席习近平当日给内蒙古自治区苏尼特右旗乌兰牧骑的队员们回信，勉励他们继续扎根基层、服务群众，努力创作更多接地气、传得开、留得下的优秀作品。","民间组织是推动经济社会发展、参与国际合作和全球治理的重要力量。建设丝绸之路沿线民间组织合作网络是加强沿线各国民间交流合作、促进民心相通的重要举措。希望与会代表以这次论坛为契机，共商推进民心相通大计，为增进各国人民相互理解和友谊、促进各国共同发展、推动构建人类命运共同体作出贡献！"]
    # completeComment = get_one_topic_doc()
    print "=========TFIDF=============TFIDF=============TFIDF===========TFIDF===================="
    print 'Obtaining top 50 words from TF IDF....\n'
    #getting top 50 comments from TF IDF algorithm (code written in Mytfidf.py)
    topNoOfComments = 20
    # tfidfresults = Mytfidf.runmytfidf(completeComment,topNoOfComments)
    tfidfresults = Mytfidf.tf_idf_self(completeComment,topNoOfComments)
    print "len(tfidfresults)",len(tfidfresults)
    # returnList of TF IDF: [[u'\u4f18\u79c0\u4f5c\u54c1', u'\u63a5\u5730\u6c14'
    # **********************************************************************************
    print "=========RAKE=============RAKE=============RAKE===========RAKE===================="
    #getting top 50 comments from RAKE (code in rake.py)
    # stop_words_path = "stopwords.txt"
    # topwordsRAKE = []
    # print 'Obtaining top 50 words from RAKE....\n'
    # minlenth = 5
    # mintimes = 1
    # maxnoofphrases = 5
    # for text in completeComment:
    #     # 换行符及空格删除
    #     text = text.replace('\n',"")
    #     text = text.replace(' ',"")
    #     keywords = rake.Rake(stop_words_path,minlenth,mintimes,maxnoofphrases).run(text)
    #     topwordsRAKE.append(keywords)
    print "=========textrank=============textrank=============textrank===========textrank===================="
    #getting top 50 comments from AKE (code in AKE.py)
    print 'obtaining top 50 words from running Automatic keyword Extraction - textrank '
    topwordsAKE=[]
    for text in completeComment:
        first_one = list()
        result = AKE.score_keyphrases_by_textrank(text,n_keywords=20)
        # print type(result)
        for couple in result:
            # print "couple[0]",couple[0]
            first_one.append(couple[0])
        topwordsAKE.append(first_one)
    # print "topwordsAKE",topwordsAKE
    # print "len(topwordsAKE)",len(topwordsAKE)


    #
    #Ensemble technique - Weighted majority voting
    #Higher weitage is given to top ranked words
    print 'Running Ensemble technique - Weighted majority voting'
    topwordsEnsemble = []
    docs_key_words = []
    for i in range(0,len(completeComment)):
        candidate_score = {}
        one_doc_key_words = []
        cadidateIDF = tfidfresults[i]
        # cadidateRAKE = topwordsRAKE[i]
        cadidateAKE = topwordsAKE[i]
        for candidate in cadidateIDF:
            candidate_score.setdefault(candidate, 0)
            candidate_score[candidate] = candidate_score[candidate] + (50 - cadidateIDF.index(candidate))
        # print "cadidateIDF",candidate_score
        # for candidate in cadidateRAKE:
        #     candidate_score.setdefault(candidate, 0)
        #     candidate_score[candidate] = candidate_score[candidate] + (50 - cadidateRAKE.index(candidate))

        for candidate in cadidateAKE:
            candidate_score.setdefault(candidate, 0)
            candidate_score[candidate] = candidate_score[candidate] + (50 - cadidateAKE.index(candidate))
        # 每篇文章取10个关键词
        sortedCandidates = sorted(candidate_score.iteritems(), key=operator.itemgetter(1), reverse=True)[:20]
        candidateList = []
        for i in range(0,len(sortedCandidates)):
            one_doc_key_words.append((sortedCandidates[i])[0])
        docs_key_words.append(one_doc_key_words)
    print "===================ALL DOCS RESULT==========================="
    # print len(docs_key_words)
    # for i in range(0,len(docs_key_words)):
        # for jj in docs_key_words[i]:
        #     print "第"+str(i+1)+"篇文章关键词：",jj
        # if len(docs_key_words[i]) < 20:
        #     print "第" + str(i + 1) + "篇文章关键词总量：", len(docs_key_words[i])
    return docs_key_words
    # c = collections.Counter(topic_key_words)
    # topic_words =  c.most_common(30)
    # for aa in topic_words:
    #     print aa[0],aa[1]


# if __name__=='__main__':
#     result = key_word_priority()