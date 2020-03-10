from collections import defaultdict
import math


class BigramKN():
    def __init__(self, start_token=True):
        self.n = 2
        self.c = defaultdict(int)
        self.count = defaultdict(lambda: defaultdict(lambda: 0))
        self.bigram_end_by = defaultdict(set)
        self.bigram_start_by = defaultdict(set)
        self.bigram_types = set()
        self.start_token = start_token

    def train(self, data):
        data = [item.split() for item in data.splitlines()]
        for line in data:
            self.train_on_line(line)
        
        self.compile()
    
    def train_on_line(self, line):
        if self.start_token:
            line = ["~"] + line
        for group in zip(*[line[i:] for i in range(self.n)]):
            first_word = group[0]
            last_word = group[1]

            self.c[first_word] += 1
            self.c[group] += 1
            self.count[first_word][last_word] += 1
            self.bigram_end_by[last_word].add(first_word)
            self.bigram_start_by[first_word].add(last_word)
            self.bigram_types.add(group)
            self.bigram_sum = {}
        self.c[last_word] += 1


    def compile(self):
        for item in self.bigram_end_by:
            self.bigram_end_by[item] = len(self.bigram_end_by[item])
            self.bigram_start_by[item] = len(self.bigram_start_by[item])
            self.bigram_sum[item] = sum(self.count[item].values())
        self.bigram_types = len(self.bigram_types)

    def p(self, bigram):
        bigram = tuple(bigram)
        first_word, last_word = bigram

        d = .75
        first_term = max(self.c[bigram] - d, 0) / self.bigram_sum[first_word]
        lam = d * self.bigram_start_by[first_word] / self.c[first_word]
        p_cont = self.bigram_end_by[last_word] / self.bigram_types
        return first_term + lam * p_cont

    def logp(self, bigram):
        return -math.log(self.p(bigram))
    
    def save(self, filename):
        import pickle
        with open(filename, "wb") as f:
            pickle.dump(self, f)
