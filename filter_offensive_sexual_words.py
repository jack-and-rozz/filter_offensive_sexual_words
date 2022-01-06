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

# deprecated
# def get_ngword_match(tokenized_text: str, tokenized_ngwords:set) -> list:
#     res = []
#     for ngword in tokenized_ngwords:
#         m = re.search(ngword, tokenized_text)
#         if m:
#             res.append((ngword, m.span()))
#     return res

def get_ngword_match_strict(tokenized_text: str, tokenized_ngwords:set) -> list:
    res = []
    tokenized_text = tokenized_text.split()
    for ngword in tokenized_ngwords:
        ngword = ngword.split()
        for i in range(len(tokenized_text) - len(ngword) + 1):
            if tokenized_text[i:i+len(ngword)] == ngword:
                res.append((ngword, range(i, i+len(ngword))))
    return res

get_ngword_match = get_ngword_match_strict


def read_words_list(paths: list, tokenizer) -> set:
    ngwords = set()
    for path in paths:
        for l in open(path):
            ngword = tokenizer.parse(l.strip()).strip()
            ngwords.add(ngword)
    return ngwords


def replace_ngwords_into_mask(tokenized_text, match_res, mask_char="*"):
    masked_text = tokenized_text.split()
    for _, match_range in match_res:
        masked_text = [
            ''.join([mask_char for _ in range(len(tok))])
            if i in match_range else tok
            for i, tok in enumerate(masked_text)]
    return masked_text



def test(match_func, samples, tokenized_ngwords, tokenizer):
    for text in samples:
        tokenized_text = tokenizer.parse(text).strip()
        # match_res = get_ngword_match(tokenized_text, tokenized_ngwords)
        match_res = match_func(tokenized_text, tokenized_ngwords)
        replaced_text = replace_ngwords_into_mask(tokenized_text, match_res)

        print('==================')
        print('original:', text)
        print('tokenized:', tokenized_text)
        print('match:', match_res)
        print('masked:', replaced_text)
        print('rejoined + retokenized:', tokenizer.parse(''.join(replaced_text)))
        
    return replaced_text

def main():
    tokenizer = MeCab.Tagger('-Owakati')
    tokenized_ngwords = read_words_list(ngwords_lists_path, tokenizer)

    samples = [
        "もう何度言ったか知らんがPCR検査、本当これ受ける糞馬鹿野郎のせいでエンドレスだな",
        "可愛いAV女優もソープ嬢もたくさんいるのに性犯罪犯す男ってなんなの…？",
        "...話の流れと口で「めくら」「かたわ」みたいな放送禁止用語を飛ばしてたってのが分かった",
        "やりかたわかった"
    ]

    # t = time.time()
    # test(get_ngword_match, samples, tokenized_ngwords, tokenizer)
    # print('get_ngword_match', time.time() - t, 'sec', file=sys.stderr)

    t = time.time()
    test(get_ngword_match_strict, samples, tokenized_ngwords, tokenizer)
    print('get_ngword_match_strict', time.time() - t, 'sec', file=sys.stderr)

if __name__ == "__main__":
    main()
