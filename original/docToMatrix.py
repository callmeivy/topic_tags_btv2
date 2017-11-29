#coding=UTF-8
'''
Updated on 6 June,2017
北京台新闻推荐部分

@author: Ivy

为LDA准备part-00000.txt,该文档在/usr/jincan下
'''
import os
import os.path
root_directory_lda = 'C:\Python27\Lib\site-packages\lda\\tests'
# root_directory_lda = '/usr/local/lib/python2.7/site-packages/lda/tests'
# docFile_reuters_tokens = open(root_directory_lda+'/tokens.txt','r')
docFile_reuters_tokens = open(root_directory_lda+'/reuters.tokens','r')
# docFile_reuters_tokens = open('C:\Users\Ivy\Desktop\myself\\tokens.txt','r')
tokenslist = docFile_reuters_tokens.readlines()
token_list = list()
for word in tokenslist:
    if len(word) > 0:
        token_list.append(word)
# token_list存储关键词，这是一个list,测试用的tokens一共350个，以为这矩阵的列数固定为350

# root_directory = '/home/ctvit'
# root_directory = '/usr/local/lib/python2.7/site-packages/lda/tests'
root_directory = 'D:\\tmp'
# root_directory = '/tmp'
docFile_list_of_lists = open(root_directory+'/list_of_lists.txt','r')
docIntolist = docFile_list_of_lists.readlines()

# 'E:\\hqtest'
if os.path.exists(r'/part-00000.txt'):
        os.path.remove(r'/part-00000.txt')
ori_matrix_file = open(root_directory+'/part-00000.txt', 'w+')
for single in docIntolist:
    # single_list代表着一篇文章所有的有意义词，这是一个list
    single_list = single.split(',')
    tokens_doc_times = list()
    for one_word in token_list:
        # 注意这里需要strip,否则count结果不正确
        one_word = one_word.strip()
        times = single_list.count(one_word)
        # print one_word,len(one_word),times
        tokens_doc_times.append(str(times))
    tokens_doc_times = ','.join(tokens_doc_times)
    ori_matrix_file.write("%s\n" % str(tokens_doc_times).encode('utf-8'))

ori_matrix_file.close()
docFile_reuters_tokens.close()
docFile_list_of_lists.close()
print 'docToMatrix.py is done!'