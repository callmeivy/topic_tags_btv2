#coding=UTF-8
#Importing necessary libraries
import math
import re
from textblob import TextBlob as tb
import jieba
import jieba.posseg as pseg
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
path = "customize_dict.txt"
jieba.load_userdict(path)
valid = ['ns', 'vn','n','nz','eng','nr','nrt']
# stopwords
dicFile = open('stopwords.txt', 'r')
stopwords = dicFile.readlines()
stopwordList = []
stopwordList.append(' ')
for stopword in stopwords:
    temp = stopword.strip().replace('\r\n', '').decode('utf8')
    stopwordList.append(temp)
dicFile.close()

#Function to compute Term Frequency(TF = no. of times word present in passage/no. of words)
def tf(word, passage, passagelen):
    return (float)(passage.words.count(word)) / passagelen

#Function to compute the number of passages a word is present in
def n_containing(word, commentList):
    return sum(1 for passage in commentList if word in passage)

#Function to compute inverse document frequency (IDF = log_e(Total number of documents / Number of documents with term t in it)
def idf(word, commentList):
    return math.log(len(commentList) / (float)(1 + n_containing(word, commentList)))

#Function to compute tf idf
def tfidf(word, passage, commentList):
    passagelen = (float)(len(passage.words))
    return round(tf(word, passage, passagelen) * idf(word, commentList),5)

def preprocessing(commentFull):
    tokens = list()

    # tokens = filter(lambda word: not word in stopwordList,jieba.cut(commentFull))
    # tokens = filter(lambda word: not word in stopwordList,pseg.cut(commentFull))
    token = pseg.cut(commentFull)
    good_tags = set(['n', 'ns', 'nz', 'nr', 'nrt', 'nt', 'x'])
    for i in token:
        if len(i.word) >1:
            if i.flag in good_tags:
                if i.word not in stopwordList:
                    # print i.word,i.flag
                    tokens.append(i.word)
    processedComment = ' '
    return processedComment.join(tokens)

#Function to run TF IDF algorithm
# completeComment is dict, topNumber is the number of key words
# completeComment是一个主题内的所有文章
def runmytfidf(completeComment, topNumber):
    print "topNumber1111",topNumber
    commentList = []

    # textblob为了使用text.word.count
    for i in range(0,len(completeComment)):
        commentList.append(tb(preprocessing(completeComment[i])))

    returnList=[]
    #Obtaing the Top Key words for all the passages
    for i, passage in enumerate(commentList):
        scores = {word: tfidf(word, passage, commentList) for word in passage.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        topWords=[]
        print "len(sorted_words)",len(sorted_words)
        # for word, score in sorted_words[:topNumber]:
        for word, score in sorted_words:
            if len(word) >1:
                # print word,len(word)
                topWords.append(word)
        returnList.append(topWords)
    return returnList

# completeComment是一个主题内的所有文章
def tf_idf_self(completeComment,topNoOfComments):
    # print completeComment[0]
    # print completeComment[1]
    # print completeComment[2]
    # word_candidate = list()
    commentList = list()
    # 文本切词后的结果，词之间以空格隔开
    for i in range(0,len(completeComment)):
        commentList.append(tb(preprocessing(completeComment[i])))
    commentList2 = list()
    for one in commentList:
        commentList2.append(str(one))
    # for i in range(0, len(completeComment)):
    #     token = pseg.cut(completeComment[i])
    #     for i in token:
    #         if len(i.word) > 1:
    #             if i.flag in valid:
    #                 if i.word not in stopwordList:
    #                     word_candidate.append(i.word)
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(vectorizer.fit_transform(commentList2))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    print type(weight)
    tf_idf_word_docs =list()
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        word_weight = dict()
        tf_idf_word_doc = list()
        sorted_word_weight = list()
        # print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
        for j in range(len(word)):
            # print word[j], weight[i][j]
            word_weight[word[j]] = weight[i][j]
        sorted_word_weight = sorted(word_weight.items(), key=lambda x: x[1], reverse=True)
        # print type(sorted_word_weight)
        for w,score in sorted_word_weight:
            # if w in word_candidate:
            #     print "hehe",w
            tf_idf_word_doc.append(w)
        tf_idf_word_docs.append(tf_idf_word_doc[:topNoOfComments])
    return tf_idf_word_docs



if __name__ == '__main__':
    corpus = ["两年的筹划准备 十余稿的剧本修改 大半年的拍摄和后期制作 近千人的努力付出 &middot;&middot;&middot;&middot;&middot;&middot;     电影《谁是球王》终于要在明天走进院线，与观众见面了。选择在8月3日这天上映，是借用数字的中文谐音“不散”，也表达了这部电影的愿望：友情不散、爱情不散、青春不散、足球不散。  央视首部体育IP电影——头顶这样的光环，让电影《谁是球王》从一开始就备受关注，也引起了不小的争议。众所周知，这部电影是央视建台以来，首次基于自创栏目品牌策划制作的电影项目。一部“小制作”牵动了“大话题”。电影《谁是球王》的推出，不仅对于“谁是球王”这一品牌，对于中央电视台、中国体育产业乃至中国电影产业来说，都有不一样的意义。  下面让我们一起来盘点一下推荐这部电影的6大理由： 1.揭秘同名电视节目中的真实工作状态 2.推广草根足球文化，激励每个人实现自己的足球梦 3.小清新&amp;充满诚意 4.讲述民间草根足球自己的故事 5.充满青春和热血 6.老少皆宜、适合全家人观看  当然，最最重要的是......可以在电影院“偶遇”明星！北京的小伙伴们有福气啦，每场观影之后，多名主演以及央视著名主持人都会举办主创见面会，零距离接触偶像的机会，还等什么呢？  最后，送你们终极版预告，提前过把瘾。 8月3日，射中笑点，不见不（8）散（3）！","在火箭队老板亚历山大将火箭队出售以后，据悉，目前篮网队老板米哈伊尔&middot;普罗霍罗夫也已经准备出售篮网队了。据消息人士透露，由于未能出售掉球队的少量股份，普罗霍罗夫现在计划卖掉球队的控股权。普罗霍罗夫希望分两部分卖掉篮网。首先，52岁的普罗霍罗夫希望先卖掉球队的少量股份，然后给予买家三年的时间来买下整支球队。除此之外，由于亚历山大以22亿美元的价格出售了火箭队，普罗霍罗夫希望得到一份接近20亿美元的报价。","北京时间9月11日消息，火箭名宿麦迪正式入选名人堂之后，多为NBA球星都对麦迪变表达了祝贺，包括麦迪的火箭队友姚明。今天前湖人球星科比也发推特向正式入选奈史密斯篮球名人堂的麦迪表达了祝贺。科比发文写到：“你实至名归，Tmac。你在比赛的每个方面都是一头猛兽，我希望你的孩子了解并欣赏他们的爸爸在赛场上是多么的冷酷。”昨天科比就在推特上转发了一段麦迪进入名人堂的视频，今天又公开给予麦迪如此高的评价，这也看出了科比对这位宿敌和老友的支持和欣赏之情。如今后乔丹时代的联盟代表人物艾弗森、麦迪都相继进入名人堂，相信不久之后科比也将享受这一荣誉。看到麦迪入选名人堂的消息，不少球迷也都纷纷感叹：“时间已经到了科比叫做名宿，麦迪成为名人堂传奇球星的时候了。”"]  # 第四类文本的切词结果
    tf_idf_self(corpus,4)
