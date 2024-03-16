import json
import random
import argparse
from multiprocessing import Pool

import spacy
from tqdm import tqdm

from augmentation_tools import MV, PI, DN, NEG
from augmentation_tools import cn_mv, cn_dn, cn_pi, cn_neg

gen_positive = {
    'aa': MV.aug_mv,
    'pi': PI.aug_pi,
    'dn': DN.aug_dn,
    'cn_dn': cn_dn.aug_dn,
    'cn_aa': cn_mv.aug_mv,
    'cn_pi': cn_pi.aug_pi
}

gen_negative = {
    'neg': NEG.aug_neg,
    'cn_neg': cn_neg.aug_neg
}


def augmentation(sentence):
    sentence = sentence.strip()
    parsed_sentence = parser(sentence)
    if args.language == 'en':
        raw = " ".join([str(_) for _ in parsed_sentence])
    else:
        raw = "".join([str(_) for _ in parsed_sentence])

    pos = gen_positive[args.p](parsed_sentence)
    sentence_tuple = [raw, pos]

    if args.add_n:
        neg = gen_negative[args.n](parsed_sentence)
        sentence_tuple.append(neg)

    return sentence_tuple, int(raw == pos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default='cn', type=str, help="Choose either Chinese (cn) or English (en).")
    parser.add_argument('--p', default='cn_pi', type=str, help="Select the type of positive sample augmentation.")
    parser.add_argument('--n', default='cn_neg', type=str, help="Select the type of negative sample augmentation.")
    parser.add_argument('--add_n', default=True, type=bool, help="Does data augmentation include the negative?")
    args = parser.parse_args()

    if args.p not in gen_positive or args.n not in gen_negative:
        raise NotImplementedError

    random.seed(2023)
    if args.language == 'en':
        parser = spacy.load("en_core_web_sm")
    else:
        parser = spacy.load('zh_core_web_md')

    in_file = "corpus.txt"
    with open(in_file, "r", encoding="utf-8") as f:
        data = f.readlines()

    out_name = "_".join([args.p, args.n])
    out_file = f"{out_name}.txt"

    count = 0

    pool = Pool(4)
    with open(out_file, "w", encoding="utf-8") as f1:
        for i, result in enumerate(tqdm(pool.imap(augmentation, data))):
            f1.write(json.dumps(result[0], ensure_ascii=False) + "\n")
            count += result[1]
    pool.close()
    pool.join()

    print(f"augmented sentences: {len(data) - count}")
