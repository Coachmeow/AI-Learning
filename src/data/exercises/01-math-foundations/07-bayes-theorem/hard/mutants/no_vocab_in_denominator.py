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
        words = [w for w in document.lower().split() if w in self.vocab]
        n_docs = sum(self.class_counts.values())
        s, V = self.smoothing, len(self.vocab)
        scores = {}
        for cls in self.class_counts:
            score = math.log(self.class_counts[cls] / n_docs)
            total = self.class_word_totals[cls]
            for w in words:
                score += math.log((self.word_counts[cls].get(w, 0) + s) / (total + s))
            scores[cls] = score
        return scores

    def predict_proba(self, document):
        scores = self.log_scores(document)
        m = max(scores.values())
        weights = {c: math.exp(v - m) for c, v in scores.items()}
        z = sum(weights.values())
        return {c: w / z for c, w in weights.items()}
