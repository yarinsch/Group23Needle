from typing import List
from data_types import *
import numpy as np

BASE_CHECK = 10  # the number of first minutes to use in the similarity calculations.
NO_MATCH = -1  # indications for no match found.


def find_jaccard(user1: dict, user2: dict):
    """
    Finds the Jaccard similarity between two given dictionaries (the similarity is performed on the keys)
    :param user1: dictionary
    :param user2: dictionary
    :return: the Jaccard similarity of the two dictionaries.
    """
    if len(user1) == 0 or len(user2) == 0:
        return 0
    items1 = set(user1.keys())
    items2 = set(user2.keys())
    return len(items1.intersection(items2)) / len(items1.union(items2))


def find_cosine(user1, user2):
    """
    Finds the cosine similarity between two given dictionaries (the similarity is performed on the values)
    :param user1: dictionary with numerical values.
    :param user2: dictionary with numerical values.
    :return: the cosine similarity of the two given dictionaries.
    """
    # If an item is not in user1 than their dot product will amount to zero anyways
    dot_prod = 0
    for item, rate in user1.items():
        if item in user2:
            dot_prod += rate * user2[item]
    size1 = 0
    for val in user1.values():
        size1 += val ** 2
    size2 = 0
    for val in user2.values():
        size2 += val ** 2
    if size1 * size2 == 0:
        return 0
    return dot_prod / ((size1 * size2) ** 0.5)


def get_sim_jac(user1: Team, user2: Team, length: int = BASE_CHECK):
    """
    Given a length, calculates the Jaccard similarities over the first #length values of the two given Teams and
    average the values to get a single Jaccard similarity value.
    :param user1: A Team
    :param user2: A Team
    :param length: the number of first minutes to calculate Jaccard with
    :return: the averaged Jaccard over the first #length minutes of the two given Teams.
    """
    curr_jac = 0
    if len(user1.items) < length or len(user2.items) < length:
        return 0
    for i in range(length):
        curr_jac += find_jaccard(user1.items[i], user2.items[i])
    return curr_jac / length


def get_sim_cos(user1: Team, user2: Team, length: int = BASE_CHECK):
    """
    Given a length, calculates the Cosine similarities over the first #length values of the two given Teams and
    average the values to get a single Cosine similarity value.
    :param user1: A Team
    :param user2: A Team
    :param length: the number of first minutes to calculate Jaccard with
    :return: the averaged Cosine over the first #length minutes of the two given Teams.
    """
    curr_cos = 0
    if len(user1.items) < length or len(user2.items) < length:
        return 0
    for i in range(length):
        curr_cos += find_cosine(user1.items[i], user2.items[i])
    return curr_cos / length


def get_best_similar(curr_user: Team, users: List[Team], length: int = BASE_CHECK) -> [int]:
    """
    Finds the Team in users with the best similarity (Jaccard and Cosine) to the curr_user Team over the first
    #length minutes.
    :param length: the number of first minutes to perform the similarities over.
    :param curr_user: A Team object
    :param users: All the teams to check against
    :return: A tuple with one the best Jaccard and the second being the best Cosine similarity
    """
    rankings_jaccard = []
    rankings_cosine = []
    for user2 in users:
        rankings_jaccard.append(get_sim_jac(curr_user, user2, length))
        rankings_cosine.append(get_sim_cos(curr_user, user2, length))
    return np.argmax(rankings_jaccard), np.argmax(rankings_cosine)