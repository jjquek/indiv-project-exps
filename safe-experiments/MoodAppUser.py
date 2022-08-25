from typing import List, Dict, Union
from itertools import repeat
from collections import Counter
import random as r
import numpy as np
from nptyping import NDArray, Float
from secure_SAFE_utils import SharedPRNG

DocumentSet = Union[List[int], Dict[int, List[int]]] # NOTE -not sure if this is the best way to do it.

# NOTE - I really should have designed the class more carefully before coding it up.

class MoodAppUser:
    POSSIBLE_KEYWORDS = [0, 1, 2, 3, 4, 5, 6]
    D_Value = None # replace with some default value.
    shared_PRNG = None
    PRNG_seeded = False

    def __init__(self, id:int, inputs: List[int]) -> None:
        # initialized on instance construction
        self.id: int = id
        self.other_user_ids: List[int] = []
        self.document_set: DocumentSet = inputs
        self.keyword_frequencies = Counter(inputs)
        # NOTE - next time I'll wanna be clear about whether these all belong in the constructor. Arguably I should have separated giving each user an id and then assigning their document set
        self.feature_vector: NDArray[Float] = [] # List converted to NDArray
        self.generate_feature_vector()
        # initialized when protocol starts
        self.shares_to_send: Dict[int, NDArray[Float]] = {}
        self.Nth_share: NDArray[Float] = None
        self.shares_received: List[NDArray[Float]] = []
        self.obfuscated_feature_v: NDArray[Float] = None 
    
    @classmethod
    def set_D_value(cls, value_is_random: bool = False, shared_seed: int = None) -> None:
        """
        * sets the class attribute 'D_Value' for all instances (users) to use for a round of the safe Protocol

        * params with default args do only need to be changed if we want to start randomizing the D value each round.
        * 'value_is_random' flag determines whether the D value is to be generated in a randomized way. If so, the 'shared_seed' should be passed in. Once the PRNG has been seeded, then a new PRNG no longer needs to be selected and can just be generated afresh.
        """
        if not value_is_random:
            cls.D_Value = 100.0
            return
        
        assert shared_seed != None, "Shared seed needs to be passed in for randomized D value run"
        
        if cls.PRNG_seeded:
            cls.D_Value = cls.shared_PRNG.random()
            return
        
        cls.shared_PRNG = SharedPRNG(shared_seed)
        cls.PRNG_seeded = True
        cls.D_Value = cls.shared_PRNG.random()
            

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
        no_of_responses = len(self.document_set)
        for frequency in self.keyword_frequencies.values():
            self.feature_vector.append(frequency / no_of_responses)
        self.feature_vector = np.round(self.feature_vector, 4)

    def generate_shares_to_send(self, number_of_users: int,
                                  share_dimensionality: int) -> None:
        """
        * assigns a dictionary {id:share} to the instance attribute 'shares_to_send'

        * N-1 shares are uniformly drawn from an interval [-D_value, D_value]
        * Each share is a numpy array that is of size == share_dimensionality. For simplicity, a one-dimensional numpy array with k columns represents the k-dimensional share vector. Numpy arrays are more efficient than Python lists in this case.
        * These N-1 shares are for the other N-1 users.
        """
        self.other_user_ids = [id for id in range(number_of_users) if id != self.id]
        for other_user in self.other_user_ids:
            share_to_distribute = [round(r.uniform(-self.D_Value, self.D_Value), 4) 
                                      for _ in repeat(None, share_dimensionality)]
            share_to_distribute = np.array(share_to_distribute)
            self.shares_to_send[other_user] = share_to_distribute

    def calculate_Nth_share(self) -> None:
        """
        * assigns to the instance attribute 'Nth_share'

        * calculates the Nth_share by subtracting the sum of the N-1 shares drawn from the [-D, D] interval from their raw_feature vector
        """
        sum_of_shares_to_send = np.sum(list(self.shares_to_send.values()), axis = 0)
        self.Nth_share = np.subtract(self.feature_vector, sum_of_shares_to_send)  

    def get_share_for_user(self, user_id: int): # NOTE -> NDArray[Float] throws error for some reason 
        """
        * indexes the 'shares_to_send' instance attribute with the given user_id and returns the share_to_be_distributed
        """
        return self.shares_to_send[user_id]

    def receive_share(self, share) -> None: 
        """
        * appends to the 'share_received' instance attribute
        """
        self.shares_received.append(share)

    def generate_obfuscated_feature_v(self) -> None:
        """
        * assigns to the 'obfuscated_feature_v' instance attribute
        
        * uses the shares_received and the Nth share to do this.
        """
        sum_of_received_shares = np.sum(self.shares_received, axis = 0)
        self.obfuscated_feature_v = np.add(self.Nth_share, sum_of_received_shares)
        self.obfuscated_feature_v = np.round(self.obfuscated_feature_v, 4)