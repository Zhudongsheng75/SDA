import random

affirm_verb = ['不能不', '不会不', '必须', '不得不', '应该', '应当', '可能', '也许']
head_list = ['不得不说，', '不得不承认，', '不可否认，', '毋庸置疑，', '显而易见，', '诚然，']
affirm_adj = ["极度", "非常", "很", "尤其", "特别", "极其", "真正地", "显著地"]


def aug_verb(parsed_sentence, aug_word):
    tokens = [str(_) for _ in parsed_sentence]
    deps = [_.dep_ for _ in parsed_sentence]
    pos = [_.pos_ for _ in parsed_sentence]

    for i, dep in enumerate(deps):
        if dep == "ROOT":
            if pos[i][0] == "V":
                tokens[i] = aug_word + tokens[i]
                break
    else:
        tokens = [random.choice(head_list)] + tokens

    return "".join(tokens)


def aug_adj(parsed_sentence, aug_word):
    tokens = [str(_) for _ in parsed_sentence]
    poses = [_.pos_ for _ in parsed_sentence]

    for i, tag in enumerate(poses):
        if tag == "ADJ":
            tokens[i] = aug_word + tokens[i]
            break
    else:
        tokens = [random.choice(head_list)] + tokens

    return "".join(tokens)


def aug_mv(parsed_sentence):
    raw = "".join([str(_) for _ in parsed_sentence])

    aug_methods = [aug_verb, aug_adj]
    aug_words = [affirm_verb, affirm_adj]
    p = random.choice([0, 1])

    augmented = aug_methods[p](parsed_sentence, random.choice(aug_words[p]))
    if raw == augmented:
        augmented = aug_methods[1-p](parsed_sentence, random.choice(aug_words[1-p]))

    return augmented
