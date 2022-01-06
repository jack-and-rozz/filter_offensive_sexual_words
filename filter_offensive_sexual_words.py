# coding: utf-8
import re
import MeCab
ngwords_lists_root = 'inappropriate-words-ja'
ngwords_lists_path = [
    'Offensive.txt',
    'Sexual.txt',
    'Sexual_with_bopo.txt',
    'Sexual_with_mask.txt',
]
ngwords_lists_path = [ngwords_lists_root + '/' + p for p in ngwords_lists_path]

def get_ngword_match(text: str, tokenized_ngwords:set):
    res = []
    for ngword in tokenized_ngwords:
        m = re.search(ngword, text)
        if m:
            res.append((ngword, m.span()))
    return res

def read_words_list(paths: list, tokenizer) -> set:
    ngwords = set()
    for path in paths:
        for l in open(path):
            ngword = tokenizer.parse(l.strip()).strip()
            ngwords.add(ngword)
    return ngwords



def main():
    tokenizer = MeCab.Tagger('-Owakati')
    tokenized_ngwords = read_words_list(ngwords_lists_path, tokenizer)

    samples = [
        "もう何度言ったか知らんがPCR検査、本当これ受ける糞馬鹿野郎のせいでエンドレスだな",
        "可愛いAV女優もソープ嬢もたくさんいるのに性犯罪犯す男ってなんなの…？",
        "...話の流れと口で「めくら」「かたわ」みたいな放送禁止用語を飛ばしてたってのが分かった"
    ]
    for text in samples:
        tokenized_text = tokenizer.parse(text).strip()
        res = get_ngword_match(tokenized_text, tokenized_ngwords)
        print(text)
        print(tokenized_text)
        print(res)

if __name__ == "__main__":
    main()
