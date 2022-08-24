from typing import List
from collections import Counter

class MoodAppUser:
    POSSIBLE_KEYWORDS = [0, 1, 2, 3, 4, 5, 6]

    def __init__(self, id:int, inputs: List[int]) -> None:
        self.id = id
        self.document_set = inputs
        self.no_of_responses = len(inputs)
        self.keyword_frequencies = Counter(inputs)
        self.feature_vector = []
        self.generate_feature_vector() 

    def generate_missing_keyword_frequencies(self) -> None:
        """
        *   Helper function called in generate_feature_vector
        *   Assigns 0 to the 'keyword_frequencies' instance attribute for every keyword (i.e. response) that's not
        * part of the user's document set
        """
        for keyword in self.POSSIBLE_KEYWORDS:
            if keyword not in self.keyword_frequencies:
                self.keyword_frequencies[keyword] = 0
         
    def generate_feature_vector(self) -> None:
        """
        * called in __init__()
        * assigns feature vector to instance attribute `feature_vector` for the user
        Feature vector is implemented as a list of d-size, where d = len(KEYWORDS)
        - the indexes of this list from 0 up to and including d-1 are mapped to the possible responses from users
         (encoded) as integers
        - each value in the list is the proportion of the given response's frequency in the document set 
        """
        self.generate_missing_keyword_frequencies()
        for frequency in self.keyword_frequencies.values():
            self.feature_vector.append(round(frequency / self.no_of_responses, 4))    

# TODO : will want to define the 'generate_shares' method for each user. And essentially make the run object oriented.