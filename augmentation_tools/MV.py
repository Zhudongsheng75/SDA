import random

be_verb = ["am", "is", "are", "was", "were", "be"]
aux_verb = ["can", "could", "will", "would", "shall", "should", "may", "might", "must", "dare"]
affirm_verb = ["must", "have to", "have no choice but", "cannot but", "can't avoid to", "can't help but", "should", "need to", "ought to"]
doubt_verb = ["can", "could", "will", "would", "shall", "may", "might"]
affirm_adj = ["extremely", "quite", "very", "particularly", "especially", "absolutely", "totally", "really", "remarkably"]
doubt_adj = ["pretty", "fairly", "rather", "somewhat", "not especially", "not particularly", "slightly", "a little"]


def aug_verb(parsed_sentence, aug_word):
    tokens = [str(_) for _ in parsed_sentence]
    deps = [_.dep_ for _ in parsed_sentence]
    tags = [_.tag_ for _ in parsed_sentence]
    lemmas = [_.lemma_ for _ in parsed_sentence]

    for i, dep in enumerate(deps):
        if dep == "aux" or dep == "auxpass":
            if tokens[i] in ["am", "are", "be"]:
                tokens[i] = aug_word + " be"
            elif tokens[i] == "is":
                tokens[i] = aug_word.replace("have", "has") + " be"
            elif tokens[i] in ["was", "were"]:
                tokens[i] = aug_word.replace("have", "had") + " be"
            break
        if dep == "ROOT":
            if tokens[i].lower() in be_verb:
                tokens[i] = aug_word + " be"
            elif tags[i] == "VBP":
                tokens[i] = aug_word + " " + lemmas[i]
            elif tags[i] == "VBZ":
                tokens[i] = aug_word.replace("have", "has") + " " + lemmas[i]
            elif tags[i] == "VBD":
                tokens[i] = aug_word.replace("have", "had") + " " + lemmas[i]
            break

    return " ".join(tokens)


def aug_adj(parsed_sentence, aug_word):
    tokens = [str(_) for _ in parsed_sentence]
    poses = [_.pos_ for _ in parsed_sentence]

    for i, tag in enumerate(poses):
        if tag == "ADJ":
            tokens[i] = aug_word + " " + tokens[i]

    return " ".join(tokens)


def aug_mv(parsed_sentence):
    raw = " ".join([str(_) for _ in parsed_sentence])

    aug_methods = [aug_verb, aug_adj]
    aug_words = [affirm_verb, affirm_adj]
    p = random.choice([0, 1])

    augmented = aug_methods[p](parsed_sentence, random.choice(aug_words[p]))
    if raw == augmented:
        augmented = aug_methods[1-p](parsed_sentence, random.choice(aug_words[1-p]))

    return augmented
