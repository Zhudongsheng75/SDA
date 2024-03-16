## 1. Instruction
This tool is the open-source code for the paper "[SDA: Simple Discrete Augmentation for Contrastive Sentence Representation Learning](https://arxiv.org/abs/2210.03963)".

Before using it, you need to install `SpaCy`, as well as `zh_core_web_md` and `en_core_web_sm` models. Otherwise, the program will not function properly.

## 2. Files
All the methods described in the paper are in the augmentation_tools folder.

In this context, "NEG" represents negative enhancement, while prefixes with "cn" denote Chinese enhancement. Other naming conventions are described in the paper.

`run_augmentation.py` is an example script for launching the augmentation process.
