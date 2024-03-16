import random

punctuation = ['，', '。', '；', '！', '：', ',', '.', ';', '!', ':']
clause = ['acl', 'advcl', 'ccomp', 'csubj', 'csubjpass', 'relcl', 'xcomp']


def aug_subject(parsed_sentence):
    tokens = [str(_) for _ in parsed_sentence]
    deps = [_.dep_ for _ in parsed_sentence]

    if 'ROOT' in deps:
        root_index = deps.index("ROOT")
        x = [i for i in parsed_sentence[root_index].children]
        if x and x[0].dep_ in ['nsubj', 'nsubjpass']:
            children_list = [i for i in x[0].children]
            index_range = list(map(lambda x: tokens.index(str(x)), children_list)) + [tokens.index(str(x[0]))]
            imax, imin = max(index_range), min(index_range)

            p = random.random()
            if p < 0.5:
                tokens[imin] = "'" + tokens[imin]
                tokens[imax] = tokens[imax] + "'"
            else:
                tokens[imax] += "，"

    return "".join(tokens)


def aug_clause(parsed_sentence):
    tokens = [str(_) for _ in parsed_sentence]
    deps = [_.dep_ for _ in parsed_sentence]

    for dep in deps:
        if dep in clause:
            index = deps.index(dep)
            child = [i for i in parsed_sentence[index].children]
            if not child:
                break
            c = child[0]
            index = tokens.index(str(c))
            if index - 1 >= 0:
                tokens[index - 1] += "，"
                break

    return "".join(tokens)


def aug_tail(parsed_sentence):
    tokens = [str(_) for _ in parsed_sentence]

    q = random.choice([0, 1])
    if q:
        tokens = ["'"] + tokens + ["'"]
    else:
        if tokens[-1] in punctuation:
            tokens[-1] = random.choice(punctuation)
        else:
            tokens.append(random.choice(punctuation))

    return "".join(tokens)


def aug_pi(parsed_sentence):
    raw = " ".join([str(_) for _ in parsed_sentence])

    aug_methods = [aug_subject, aug_clause]
    p = random.choice([0, 1])

    augmented = aug_methods[p](parsed_sentence)
    if raw == augmented:
        augmented = aug_methods[1-p](parsed_sentence)

    if raw == augmented:
        augmented = aug_tail(parsed_sentence)

    return augmented
