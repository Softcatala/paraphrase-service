import logging


class Similarity:

    def _preprocess_sentence(self, sentence):
        # Convert to lowercase, remove punctuation, and strip leading/trailing spaces
        sentence = sentence.lower()
        sentence = "".join(
            [char for char in sentence if char.isalnum() or char.isspace()]
        )
        return sentence.strip()

    def _levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def _levenshtein_similarity(self, sentence1, sentence2):
        # Preprocess sentences
        sentence1 = self._preprocess_sentence(sentence1)
        sentence2 = self._preprocess_sentence(sentence2)

        # Compute Levenshtein distance
        lev_distance = self._levenshtein_distance(sentence1, sentence2)

        # Compute similarity as (1 - normalized distance)
        max_len = max(len(sentence1), len(sentence2))
        similarity = 1 - (lev_distance / max_len)
        return similarity

    def are_sentences_almost_identical(self, sentence1, sentence2, threshold=0.95):
        similarity = self._levenshtein_similarity(sentence1, sentence2)
        result = similarity >= threshold
        if result:
            logging.debug(f"Similarity: {similarity} {sentence1}")
            logging.debug(f"Similarity: {similarity} {sentence2}")

        return result
