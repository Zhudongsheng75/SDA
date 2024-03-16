import random

neg_words = ['不', '不是', '没有', '没']
neg_templates = ["无法理解的是，", "令人惊讶的是，", "令人大跌眼镜的是，", "绝对不可能，",
                 "不可理喻的是，", "这不应该，", "这不可能，", "这不会，"]
special_words = ["是", "能", "应该", "可能", "会", "必须"]


def aug_dn(parsed_sentence):
    tokens = [str(_) for _ in parsed_sentence]
    deps = [_.dep_ for _ in parsed_sentence]
    tags = [_.tag_ for _ in parsed_sentence]
    pos = [_.pos_ for _ in parsed_sentence]

    flag = 0

    for index, token in enumerate(tokens):
        if token in neg_words:
            del tokens[index], deps[index], tags[index]
            flag += 1

    for index, dep in enumerate(deps):
        if flag == 2:
            break

        if dep == "aux" or dep == "auxpass":
            tokens[index] = "不" + tokens[index]
            flag += 1

        elif dep == "ROOT":
            if tokens[index] in special_words:
                tokens[index] = "不" + tokens[index]
                flag += 1
            elif pos[index][0] == "V":
                tokens[index] = "不" + tokens[index]
                flag += 1
            else:
                continue

    if flag == 1:
        tokens = [random.choice(neg_templates)] + tokens

    return "".join(tokens)
