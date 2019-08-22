'''
    先爬取資料庫中，數份新聞內容建立辭典與記錄該詞於其他檔案出現數量
'''

import mysql.connector
from ckip import CkipSegmenter
import pickle
import chardet

def connect_db():
    mydb = mysql.connector.connect(
        host="mysql.cs.ccu.edu.tw",
        user="lcha105u",
        passwd="Aa19980620",
        database="lcha105u_newsDB"
    )
    return mydb

def create_dict(generateNum):
    db = connect_db()
    cursor = db.cursor()

    # 先暫時用 東森新聞 作為語料庫建立
    query = " SELECT news_content" \
            " FROM udn_table" \
            " LIMIT 50";

    cursor.execute(query)
    results = cursor.fetchall()

    dictionary = {}
    corpus = []
    wordInFileNum = {}
    segments = []
    stopWords = []
    text_num = 0  # 讀取文檔數
    wordCount = 0  # 單一文章詞彙數量

    with open('news/stopWord.txt', 'r', encoding='UTF-8') as file:
        for data in file.readlines():
            data = data.strip()
            stopWords.append(data)

    for single_content in results:
        #single_content[0].encode('utf-8')
        segmenter = CkipSegmenter()
        segments = segmenter.seg(single_content[0])

        # 記錄該文檔向量化結果
        corpus.append([])

        # 暫時統計該文檔結果
        tmp_corpus = {}

        # 將新詞輸入 dict && 記錄 資料表
        for k in list(filter(lambda a: a not in stopWords and a != '\n', segments.tok)):
            if text_num == 0 and wordCount == 0:
                dictionary[k] = 1
                wordInFileNum[dictionary[k]] = 1
                tmp_corpus[dictionary[k]] = 1
            elif k in dictionary:
                if dictionary[k] in tmp_corpus:
                    tmp_corpus[dictionary[k]] += 1
                else:
                    tmp_corpus[dictionary[k]] = 1
                    wordInFileNum[dictionary[k]] += 1
            else:
                dictionary[k] = len(dictionary) + 1
                tmp_corpus[dictionary[k]] = 1
                wordInFileNum[dictionary[k]] = 1

            wordCount = wordCount + 1


        # 將暫存向量記錄值存入 corpus 中存放
        for tmp_value in tmp_corpus:
            corpus[text_num].append((tmp_value, tmp_corpus[tmp_value]))
        corpus[text_num].sort(key=sortByKey)
        text_num += 1


        storeLatestData(dictionary, corpus, wordInFileNum)


# 根據向量 key 值進行排序
def sortByKey(elem):
    return elem[0]


# 將新的 dictionary, corpus 與 wordInFileNum 存成檔案
def storeLatestData(dictionary, corpus, wordInFileNum):

    with open("news/dictionary.txt", "wb") as file:
        pickle.dump(dictionary, file)

    with open("news/corpus.txt", "wb") as file:
        pickle.dump(corpus, file)

    with open("news/wordInFileNum.txt", "wb") as file:
        pickle.dump(wordInFileNum, file)

if __name__ == "__main__":
    # 欲生成資料數
    generateNum = 100
    create_dict(generateNum)