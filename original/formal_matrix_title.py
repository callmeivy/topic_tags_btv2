#coding=UTF-8
'''
Updated on 11 Jan,2016
Run in Hbase

Created on 12 Aug, 2015 and 13 Aug, 2015
@author: Ivy
为LDA准备reuters.ldac
3月26日补充，
reuters.ldac在root_directory_lda目录下
'''
import os
import os.path
import jieba
from collections import Counter
from json import JSONDecoder
import sys
import math
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
# root_directory = '/home/ctvit'
# root_directory = '/usr/local/lib/python2.7/site-packages/lda/tests'
root_directory = 'D:\\tmp'
# root_directory = '/tmp'
# Updated by Ivy, 2016.1.11
root_directory_lda = 'C:\Python27\Lib\site-packages\lda\\tests'
# root_directory_lda = '/usr/local/lib/python2.7/site-packages/lda/tests'
title_box = list()
import re
import json

# 生成term_document_matrix
def term_document_matrix_roy_1():
    thefile = open(root_directory_lda+'/reuters.ldac', 'w+')
    term_matrix = open(root_directory+'/part-00000.txt', 'r')
    reading_file_line = term_matrix.readlines()
    matrix_row_input = list()
    for line in reading_file_line:
        line = line.replace('[','')
        line = line.replace(']','')
        line = line.split(',')
        matrix_row_input.append(line)
    mark = 0
    print 'matrix rows',len(matrix_row_input)
    for row in matrix_row_input:
        mark += 1
        # print row,'haha'
        # break
        count = 0
        count_index = 0
        matrix_row = list()
        ele = ''
        for row_element in row:
            row_element = row_element.strip()
            count_index += 1
            if row_element != str('0'):
                ele = str(count_index-1)+":"+str(row_element)
                count += 1
                matrix_row.append(ele)
        matrix_row.insert(0,str(count))
        matrix_row = ','.join(matrix_row)
        matrix_row = matrix_row.replace(","," ")
        if str(count) == '0':
            matrix_row = '1 1:1'
        if mark != len(matrix_row_input):
            thefile.write("%s\n" % str(matrix_row).encode('utf-8'))
        else:
            thefile.write("%s" % str(matrix_row).encode('utf-8'))
    term_matrix.close()
    thefile.close()
    print 'reuters.ldac is ready'



if __name__=='__main__':
    term_document_matrix_roy_1()








