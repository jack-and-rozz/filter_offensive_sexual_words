# coding: utf-8
import time, sys
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

def get_ngword_match(tokenized_text: str, tokenized_ngwords:set):
    res = []
    for ngword in tokenized_ngwords:
        m = re.search(ngword, tokenized_text)
        if m:
            res.append((ngword, m.span()))
    return res

def get_ngword_match_strict(tokenized_text: str, tokenized_ngwords:set):
    res = []
    tokenized_text = tokenized_text.split()
    for ngword in tokenized_ngwords:
        ngword = ngword.split()
        for i in range(len(tokenized_text) - len(ngword) + 1):
            if tokenized_text[i:i+len(ngword)] == ngword:
                res.append((ngword, (i, i+len(ngword))))
    return res


def read_words_list(paths: list, tokenizer) -> set:
    ngwords = set()
    for path in paths:
        for l in open(path):
            ngword = tokenizer.parse(l.strip()).strip()
            ngwords.add(ngword)
    return ngwords



def test(match_func, samples, tokenized_ngwords, tokenizer):
    for text in samples:
        tokenized_text = tokenizer.parse(text).strip()
        # res = get_ngword_match(tokenized_text, tokenized_ngwords)
        res = match_func(tokenized_text, tokenized_ngwords)
        print(text)
        print(tokenized_text)
        print(res)
    return res

def main():
    tokenizer = MeCab.Tagger('-Owakati')
    tokenized_ngwords = read_words_list(ngwords_lists_path, tokenizer)

    samples = [
        "もう何度言ったか知らんがPCR検査、本当これ受ける糞馬鹿野郎のせいでエンドレスだな",
        "可愛いAV女優もソープ嬢もたくさんいるのに性犯罪犯す男ってなんなの…？",
        "...話の流れと口で「めくら」「かたわ」みたいな放送禁止用語を飛ばしてたってのが分かった",
        "やりかたわかった"
    ]
    t = time.time()
    test(get_ngword_match, samples, tokenized_ngwords, tokenizer)
    print('get_ngword_match', time.time() - t, 'sec', file=sys.stderr)

    t = time.time()
    test(get_ngword_match_strict, samples, tokenized_ngwords, tokenizer)
    print('get_ngword_match_strict', time.time() - t, 'sec', file=sys.stderr)

if __name__ == "__main__":
    main()
