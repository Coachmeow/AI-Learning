import math
from collections import defaultdict


class NaiveBayes:
    def __init__(self, smoothing=1.0):
        self.smoothing = smoothing
        self.class_counts = defaultdict(int)
        self.word_counts = defaultdict(lambda: defaultdict(int))
        self.class_word_totals = defaultdict(int)
        self.vocab = set()

    def train(self, documents, labels):
        for doc, label in zip(documents, labels):
            self.class_counts[label] += 1
            for word in doc.lower().split():
                self.word_counts[label][word] += 1
                self.class_word_totals[label] += 1
                self.vocab.add(word)

    def log_scores(self, document):
        """{class: log P(class) + sum of log P(word | class)}, skipping words outside the vocabulary."""
        raise NotImplementedError

    def predict_proba(self, document):
        """{class: probability}, adding up to 1, computed stably from the log scores."""
        raise NotImplementedError
