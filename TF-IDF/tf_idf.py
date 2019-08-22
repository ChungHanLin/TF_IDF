from ckip import CkipSegmenter
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
    dictionary = {}     # 暫時
    # 開檔讀取已存取 dictionary 檔案

    # with open("news/dictionary.txt", "rb") as file:
    #    dictionary = pickle.load(file)

    # 記錄向量結果
    corpus = []         # 暫時
    # 開檔讀取已存取 corpus 檔案

    # with open("news/corpus.txt", "rb") as file:
    #    corpus = pickle.load(file)

    # 記錄每個詞在不同文檔出現數
    wordInFileNum = {}  # 暫時

    # with open("news/wordInFileNum.txt", "rb") as file:
    #    wordInFileNum = pickle.load(file)


    '''
        運用向量化方式記錄每個詞在文檔中的出現次數，記錄方式如下：
        [[(0, 1), (1, 3), (4, 5), ...], [(0, 2), (2, 8), (7, 9), ...], ...]
        表示第一個文本 id 為 0 的詞出現 1 次，id 為 1 的出現 3 次。同樣 id 為 0 的詞彙出現在文本 2 出現了 2 次。
        依此類推，最後再將對照組進入 list['文本_num'] 進行餘弦相似度對比，可得出相似度結果。 
    '''

    # 屆時會讀取所有新聞內容
    # 文本內容 1
    text1 = "今夏成為自由球員的林書豪，至今還沒找到新東家，據傳可能將會赴陸發展，而大陸知名籃球記者宋翔今天就在微博中爆料，" \
            "表示林書豪很有可能加盟CBA北京首鋼，「北京首鋼隊無限接近林書豪。」上季林書豪原先效力老鷹，但在季中被交易到暴龍，" \
            "儘管一度擔任先發控衛，卻因為適應不良沒有打出好表現，逐漸失去教練信任並且掉出輪換陣容，到了季後賽更只有垃圾時間才有出場機會，" \
            "狀況相當慘淡。儘管隨隊奪下冠軍，但林書豪在暴龍卻沒有太多亮眼數據，導致今夏成為自由球員，卻沒有球隊願意簽下。" \
            "今年等待時間是林書豪最漫長的一次，先前他來台分享時還落下男兒淚，認為自己遭到NBA放棄，雖然還在尋求NBA機會，" \
            "但也表示未來肯定會赴CBA打球，也因此傳出多隊已和林書豪接洽商討。" \
            "而《北京青年報》記者宋翔今就在微博上爆料，「北京首鋼無限接近林書豪。」，" \
            "宋翔在微博上表示，林書豪加盟北京有幾點原因，第一就是林書豪想到CBA打球，第二北京在談判時非常真誠因此打動了林書豪，" \
            "第三則是北京市大城市，更是聯盟強隊，「雙方已經無限接近簽約，雖然還未落筆簽字，但是預計很快會簽約。」"

    # 文本內容 2
    text2 = "林書豪今年夏天苦等不到NBA機會，讓他在上個月的台灣行活動中一度淚崩坦言「感覺被NBA放棄」，" \
            "而他的下一步如今也被中國媒體爆料，傳出他即將加盟CBA北京首鋼隊。" \
            "根據中國《北京青年報》記者宋翔報導，「北京首鋼隊無限接近簽約林書豪。雙方近期談地比較順利，達成了簽約意向。但還未最終落筆」。" \
            "宋翔進一步指出：「這次促成林書豪加盟的幾點原因是：第一林書豪想要CBA打球，這一點十分重要。" \
            "第二北京首鋼隊在談判中十分真誠，這也打動了林書豪。第三是北京是個大城市，北京首鋼隊是聯盟的強隊。" \
            "然而《虎撲體育》指出，林書豪團隊對此強調，「目前未與任何CBA球隊達成簽約意向」。" \
            "林書豪上賽季跟隨暴龍奪下職業生涯首座NBA冠軍後，今年夏天在NBA自由市場乏人問津，" \
            "讓他忍不住在佈道會中淚崩表示：「感覺被NBA放棄了。」隨著影片被美媒大肆報導，不少球員也紛紛力挺林書豪，" \
            "不過至今仍沒有任何NBA球隊有意簽下他的消息。"

    # 單一文章斷詞結果
    segments = []
    text_num = 0    # 讀取文檔數
    wordCount = 0   # 單一文章詞彙數量

    while text_num < 2:
        segmenter = CkipSegmenter()
        if text_num == 0:
            segments = segmenter.seg(text1)
        else:
            segments = segmenter.seg(text2)

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

        # 存入新 corpus 中時，應先進行相似度對比
        calculate_TF_IDF(tmp_corpus, wordCount, wordInFileNum, len(corpus))
        # 將暫存向量記錄值存入 corpus 中存放
        for tmp_value in tmp_corpus:
            corpus[text_num].append((tmp_value, tmp_corpus[tmp_value]))

        text_num += 1

    corpus[1].sort(key=sortByKey)
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


def calculate_TF_IDF(corpus, corpusCnt, wordInFileNum, fileNum):
    TF_IDF = {}
    for pointer in corpus:
        TF = corpus[pointer] / corpusCnt
        IDF = math.log(fileNum / wordInFileNum[pointer])
        TF_IDF[pointer] = TF * IDF

    print(TF_IDF)
    print(wordInFileNum)


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