import MeCab
import numpy as np
from gensim.models import word2vec

tagger = MeCab.Tagger('')
tagger.parse('')
model = word2vec.Word2Vec.load("demo.model")

# テキストのベクトルを計算
def get_vector(text):
    sum_vec = np.zeros(200)
    word_count = 0
    node = tagger.parseToNode(text)
    while node:
        fields = node.feature.split(",")
        # 名詞、動詞、形容詞に限定
        if fields[0] == '名詞' or fields[0] == '動詞' or fields[0] == '形容詞':
            sum_vec += model.wv[node.surface]
            word_count += 1
        node = node.next

    return sum_vec / word_count

# cos類似度を計算
def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

if __name__ == "__main__":
    v1 = get_vector('あいうえお')
    #v2 = get_vector('早急に対処いたします')
    #v3 = get_vector('検討しております')

    #print(cos_sim(v1, v2))
    #print(cos_sim(v1, v3))