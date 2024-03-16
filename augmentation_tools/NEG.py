import random

neg_words = ["no", "not", "n't"]
neg_templates = ["It isn't that", "The fact is not that", "It is not true that", "It is not the truth that", 
                 "Not that", "There is no way that", "There is no chance that", "It is impossible that", "It can't be that"]
special_words = ["am", "is", "was", "are", "were", "can", "could", "will",
                 "would", "shall", "should", "may", "must", "might"]


def aug_neg(parsed_sentence):
    tokens = [str(_) for _ in parsed_sentence]
    deps = [_.dep_ for _ in parsed_sentence]
    tags = [_.tag_ for _ in parsed_sentence]
    lemmas = [_.lemma_ for _ in parsed_sentence]

    for index, dep in enumerate(deps):
        
        if tokens[index] in neg_words:
            del tokens[index], deps[index], tags[index], lemmas[index]
            break

        elif dep == "aux" or dep == "auxpass":
            tokens[index] += " not"
            break

        elif dep == "ROOT":
            if tokens[index].lower() in special_words:
                tokens[index] += " not"
            elif tags[index] == "VBP":
                tokens[index] = "do not " + lemmas[index]
            elif tags[index] == "VBZ":
                tokens[index] = "does not " + lemmas[index]
            elif tags[index] == "VBD":
                tokens[index] = "did not " + lemmas[index]
            else:
                tokens = ["no"] + tokens
            break

    else:
        tokens = [random.choice(neg_templates)] + tokens

    return " ".join(tokens)
