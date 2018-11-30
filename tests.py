import unittest
from itertools import combinations

from .features import LETTERS_DETERMINATION


class LetterDeterminationTestCase(unittest.TestCase):
    longMessage = False

    def test_letter_originality(self):
        for letter1, letter2 in combinations(LETTERS_DETERMINATION.keys(), 2):
            letter1_determination = LETTERS_DETERMINATION[letter1]
            letter2_determination = LETTERS_DETERMINATION[letter2]

            letter1_feature_names = letter1_determination.keys()
            letter2_feature_names = letter2_determination.keys()
            both_feature_names = letter1_feature_names & letter2_feature_names

            letter1_both_features = {i: letter1_determination[i] for i in both_feature_names}
            letter2_both_features = {i: letter2_determination[i] for i in both_feature_names}

            self.assertNotEqual(
                letter1_both_features,
                letter2_both_features,
                msg=f"'{letter1}' and '{letter2}' letters has similar both feature values"
            )
