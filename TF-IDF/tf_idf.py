import jieba
import pickle
import math

'''
    1. 從資料庫裡建立語料庫
    2. 建立語料庫 -> 最好可以儲存 (.txt)   V
    3. 計算該詞彙在其他文檔出現次數         V
    4. 排序最高幾個關鍵詞
    5. 關鍵詞間進行 餘弦相似度 對比
'''


def main():
    # 將 stopWord 文字檔內容組成 List
    stopWords = []

    with open('news/stopWord.txt', 'r', encoding='UTF-8') as file:
        for data in file.readlines():
            data = data.strip()
            stopWords.append(data)

    # 記錄 word 與 id 對照 -> 建立語料庫
    # dictionary = {} 為 dict 資料型態
    # 開檔讀取已存取 dictionary 檔案

    with open("news/dictionary.txt", "rb") as file:
        dictionary = pickle.load(file)

    # 記錄向量結果
    # corpus = [] 為 tuple 資料型態
    # 開檔讀取已存取 corpus 檔案

    with open("news/corpus.txt", "rb") as file:
        corpus = pickle.load(file)

    # 記錄每個詞在不同文檔出現數
    # wordInFileNum = {} 為 dict 資料型態

    with open("news/wordInFileNum.txt", "rb") as file:
        wordInFileNum = pickle.load(file)


    '''
        運用向量化方式記錄每個詞在文檔中的出現次數，記錄方式如下：
        [[(0, 1), (1, 3), (4, 5), ...], [(0, 2), (2, 8), (7, 9), ...], ...]
        表示第一個文本 id 為 0 的詞出現 1 次，id 為 1 的出現 3 次。同樣 id 為 0 的詞彙出現在文本 2 出現了 2 次。
        依此類推，最後再將對照組進入 list['文本_num'] 進行餘弦相似度對比，可得出相似度結果。 
    '''

    # 屆時會讀取所有新聞內容
    # 文本內容 1
    text1 = "2019年世界羽球錦標賽正在瑞士巴塞爾進行中，前世界球后戴資穎順利晉級16強，" \
            "22日則是要對上南韓金佳恩，最終戴資穎以直落二（24：22、24：22）擊敗金佳恩，" \
            "首局更是化解對手4個局點、第二局也化解2個局點，成功晉級8強。本屆大會第二種子戴資穎的戴資穎" \
            "首戰以直落二輕取印尼小將菲特里亞尼（Fitriani Fitriani）後，16強賽將要交手世界排名29的金佳恩，" \
            "持續奪牌之路邁進，只要能夠打進四強，積分就能超過山口茜，若能一舉奪冠更可以重返球后寶座。戴資穎和金佳恩過去未曾交手" \
            "。本次交手第一局雙方1平，金佳恩挑戰成功，戴資穎1：4落後，戴資穎回球不及，金佳恩挑後場，" \
            "戴資穎回擊出界6分落後，金佳恩、戴資穎都出現掛網，金佳恩發球出界，戴資穎勾對角連要3分，" \
            "金佳恩斜線進攻，戴資穎7：11落後。30拍來回後，金佳恩大對角攻擊，戴資穎搶網挑後場8：12，" \
            "金佳恩挑戰成功，戴資穎出界、反應不及6分落後，金佳恩連續掛網，戴資穎殺球追至15：18，金" \
            "佳恩挑戰失敗但先出現局點，戴資穎勾對角，加上金佳恩失誤，金佳恩挑戰失敗，戴資穎化解3個局點，" \
            "戴資穎卦網，讓金佳恩再出現局點，戴資穎假動作再化解，金佳恩突擊出界，雙方22平，戴資穎假動作、" \
            "金佳恩失誤，戴資穎共化解4個局點24：22搶下！第二局戴資穎突擊雙方2平，戴資穎掛網、出" \
            "界3：5、4：6落後，戴資穎直線殺球、網前點放追至6平，金佳恩lucky ball但下球掛網，雙方7平，" \
            "戴資穎翻網球反超，戴資穎近身殺球9：7，戴資穎掛網被追至9平，多拍來回戴資穎收力放對角11：9，金佳恩反應不及撲地。" \
            "戴資穎回球掛網，金佳恩挑後場出界，雙方比數緊咬在一分差，戴資穎大對角攻擊13：11，但戴資穎掛網，" \
            "金佳恩腳滑劈腿，讓戴資穎直線進攻拿分，戴資穎掛網被追至14：16落後，戴資穎直線殺球追至16平，金佳恩頻頻掛網" \
            "，讓戴資穎連拿5分反超19：16，但被追至19平，戴資穎判斷失誤被反超，戴資影小球再化解金佳恩局點，" \
            "金佳恩掛網，戴資穎追至21平，金佳恩接發失誤，戴資穎出現賽末點但也失誤。方22平，" \
            "金佳恩沒過網，金佳恩最後失誤，戴資穎第二局化解金佳恩2個局點，並以24：22直落二收下勝利，晉級8強。" \
            "戴資穎五度參加世錦賽，最佳成績都是在8強止步，不過隨著日本山口茜爆冷出局，戴資穎有很機會力拚冠軍。" \
            "順利擊敗金佳恩晉級8強，8強賽將交手印度頭號女單辛度（PUSARLA V. Sindhu）和美國華裔張蓓雯對決後的勝方。"

    # 文本內容 2
    text2 = "記者林辰彥／綜合報導台灣「羽球一姊」戴資穎23日在瑞士巴塞爾舉行的BWF世界羽球錦標賽女單16強賽中，" \
            "面對世界排名第29南韓的金佳恩，連2局打到「丟士」，以兩個24：22挺進8強。戴資穎下一戰若能繼續挺進，" \
            "將奪回失去的后座。21歲的金佳恩在21日賽後接受訪問時表示能與戴資穎對戰，已經是無上的光榮。" \
            "這是金佳恩第一次打進世錦賽。金佳恩目前排名第29，世界排名最高是26。金佳恩在首局就保持領先，" \
            "並以20：17取得3個局末點，戴資穎頂住壓力，追成20：20。戴資穎先取得21分，但是隨後被金佳恩連拿2分，" \
            "又拿到1次局點。幸好戴資穎頂住，以24：22拿下首局。戴資穎在第2局6：6之後拉開2到3分的領先，" \
            "又被金佳恩追成9：9，但是戴資穎以11：9帶進技術暫停。技術暫停之後，金佳恩打來沒有壓力的追成14：14，" \
            "並以16：14取的領先，戴資穎最後靠著精湛的球技，連下5分取得19：16。不料金佳恩佑蓮拿4分，取得20：19的局點，" \
            "戴資穎又把比分追平，兩人第2局又是打「丟士」。在21：21、22：22之後，戴資穎拿下2分，" \
            "以24：22拿下第2局，花了56分鐘拿下這場比賽勝利。"

    # 單一文章斷詞結果
    text_num = 0    # 讀取文檔數
    wordCount = 0   # 單一文章詞彙數量

    # 兩篇文章比對的 TF_IDF dictionary
    TF_IDF_1 = []
    TF_IDF_2 = []

    while text_num < 2:
        # 第一篇文章
        if text_num == 0:
            segments = jieba.cut(text1, cut_all=False)
        # 第二篇文章
        else:
            segments = jieba.cut(text2, cut_all=False)

        # 記錄該文檔向量化結果
        corpus.append([])

        # 暫時統計該文檔結果
        tmp_corpus = {}

        # 將新詞輸入 dict && 記錄 資料表
        for k in list(filter(lambda a: a not in stopWords and a != '\n', segments)):
            if k in dictionary:
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

        # 存入新 corpus 中時，應先進行相似度對比
        if text_num == 0:
            TF_IDF_1 = calculate_TF_IDF(tmp_corpus, wordCount, wordInFileNum, len(corpus), dictionary)
        else:
            TF_IDF_2 = calculate_TF_IDF(tmp_corpus, wordCount, wordInFileNum, len(corpus), dictionary)
        # 將暫存向量記錄值存入 corpus 中存放
        for tmp_value in tmp_corpus:
            corpus[text_num].append((tmp_value, tmp_corpus[tmp_value]))

        text_num += 1
    corpus[1].sort(key=sortByKey)
    print(corpus)
    print(calculate_Similarity(TF_IDF_1, TF_IDF_2))
    storeLatestData(dictionary, corpus, wordInFileNum)


# 根據向量 key 值進行排序
def sortByKey(elem):
    return elem[0]


def getCategoryIndex(category_str):
    category = {
        "國際" : 0,
        "社會" : 1,
        "體育" : 2,
        "生活" : 3,
        "娛樂" : 4,
        "文教" : 5,
        "科技" : 6,
        "政經" : 7,
        "環境" : 8,
        "法律" : 9
    }
    return category[category_str]


# 記錄 TF 數值，並存入資料庫
def calculate_TF_IDF(corpus, corpusCnt, wordInFileNum, fileNum, dictionary):
    TF_IDF = {}
    for pointer in corpus:
        TF = corpus[pointer] / corpusCnt
        IDF = math.log(fileNum / wordInFileNum[pointer])
        TF_IDF[pointer] = TF * IDF

    # 將 TF_IDF 結果 由大至小 排序
    TF_IDF = [(k, TF_IDF[k]) for k in sorted(TF_IDF, key=TF_IDF.get, reverse=True)]

    # 取值維度
    dimension = 100
    top_dimension_tfidf = []
    dimensionCnt = 0
    for index in TF_IDF:
        if dimensionCnt == dimension:
            break
        top_dimension_tfidf.append((index[0], index[1]))
        dimensionCnt += 1

    # for index in TF_IDF:
    #    print([number for number, id in dictionary.items() if id == index[0]], index[1])
    top_dimension_tfidf.sort()
    return top_dimension_tfidf


# 計算兩者的餘弦相似度
def calculate_Similarity(TF_IDF_1, TF_IDF_2):
    print(TF_IDF_1)
    print(TF_IDF_2)
    innerProductSum = 0
    index_1_powerSum = 0
    index_2_powerSum = 0
    index_1 = 0
    index_2 = 0
    dimension = 100
    while 1:
        if index_1 < dimension and index_2 < dimension:
            if TF_IDF_1[index_1][0] > TF_IDF_2[index_2][0]:
                index_2 += 1
            elif TF_IDF_1[index_1][0] == TF_IDF_2[index_2][0]:
                innerProductSum += (TF_IDF_1[index_1][1] * TF_IDF_2[index_2][1])
                index_1 += 1
                index_2 += 1
            else:
                index_1 += 1
        else:
            break

    for index in TF_IDF_1:
        index_1_powerSum += pow(index[1], 2)
    for index in TF_IDF_2:
        index_2_powerSum += pow(index[1], 2)

        similarity = innerProductSum / (math.sqrt(index_1_powerSum) * math.sqrt(index_2_powerSum))
    return abs(similarity)



# 將新的 dictionary, corpus 與 wordInFileNum 存成檔案
def storeLatestData(dictionary, corpus, wordInFileNum):

    with open("news/dictionary.txt", "wb") as file:
        pickle.dump(dictionary, file)

    with open("news/corpus.txt", "wb") as file:
        pickle.dump(corpus, file)

    with open("news/wordInFileNum.txt", "wb") as file:
        pickle.dump(wordInFileNum, file)


if __name__ == "__main__":
    main()