import numpy as np
from .base import BaseScoreType


class NegativeLogLikelihood(BaseScoreType):
    def __init__(self, name='negative lof likelihood', precision=2,
                 n_columns=2):
        self.name = name
        self.precision = precision
        # n_columns = 2: binary classification
        self.n_columns = n_columns
        self.is_lower_the_better = True
        self.minimum = 0.0,
        self.maximum = float('inf')

    def score_function(self, ground_truths, predictions, valid_indexes=None):
        if valid_indexes is None:
            valid_indexes = slice(None, None, None)
        y_proba = predictions.y_pred[valid_indexes]
        y_true_proba = ground_truths.y_pred[valid_indexes]
        # Normalize rows
        y_proba_normalized = y_proba / np.sum(y_proba, axis=1, keepdims=True)
        # Kaggle's rule
        y_proba_normalized = np.maximum(y_proba_normalized, 10 ** -15)
        y_proba_normalized = np.minimum(y_proba_normalized, 1 - 10 ** -15)
        scores = - np.sum(np.log(y_proba_normalized) * y_true_proba, axis=1)
        score = np.mean(scores)
        return score
