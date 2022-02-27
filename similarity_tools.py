from typing import List
from data_types import *
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_CHECK = 10
NO_MATCH = -1


def save_teams(teams: list, file_name: str):
    with open(file_name, 'wb') as f:
        pickle.dump(teams, f)


def find_jaccard(user1: dict, user2: dict):
    """
    Finds the Jaccard similarity between two given dictionaries
    """
    if len(user1) == 0 or len(user2) == 0:
        return 0
    items1 = set(user1.keys())
    items2 = set(user2.keys())

    return len(items1.intersection(items2)) / len(items1.union(items2))


def find_cosine(user1, user2):
    """
    Finds the cosine similarity between two given dictionaries
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
    Given a length, returns the average for the Jaccard similarity averaging
    """
    curr_jac = 0
    if len(user1.items) < length or len(user2.items) < length:
        return 0
    for i in range(length):
        curr_jac += find_jaccard(user1.items[i], user2.items[i])
    return curr_jac / length


def get_sim_cos(user1: Team, user2: Team, length: int = BASE_CHECK):
    """
    Given a length, returns the average for the cosine similarity averaging
    """
    curr_cos = 0
    if len(user1.items) < length or len(user2.items) < length:
        return 0
    for i in range(length):
        curr_cos += find_cosine(user1.items[i], user2.items[i])
    return curr_cos / length


def get_best_similar(curr_user: Team, users: List[Team], length: int = BASE_CHECK) -> [int]:
    """
    This function receives a list of processed_game_data from a single side and checks all the other users for their best matching
    :param length:
    :param curr_user: A team object to check for
    :param users: All the teams to check against
    :return: A tuple with one the best Jaccard and the second being the cosine similarity
    """
    rankings_jaccard = []
    rankings_cosine = []
    prob = 0
    for user2 in users:
        rankings_jaccard.append(get_sim_jac(curr_user, user2, length))
        rankings_cosine.append(get_sim_cos(curr_user, user2, length))

        # Checks for champion matching

        # if user2.champions == currUser.champions and user2.rivals == currUser.rivals:
        #     rankings_jaccard.append(getSimJac(currUser,user2,BASE_CHECK))
        #     rankings_cosine.append(getSimCos(currUser,user2,BASE_CHECK))
        #     prob += 1
        #     print(prob,rankings_jaccard[-1],rankings_cosine[-1])
        # else:
        #     rankings_jaccard.append(NO_MATCH)
        #     rankings_cosine.append(NO_MATCH)
    return np.argmax(rankings_jaccard), np.argmax(rankings_cosine)


def check_grand_bronze_sim_correlation():
    # with open('timelines_bronze.pkl', 'rb') as f:
    #     bronze_data = pickle.load(f)
    #
    # with open('timelines_grandmaster2.pkl', 'rb') as f:
    #     grand_data = pickle.load(f)
    #
    # tests = []
    # g_teams = []
    #
    # for match in bronze_data:
    #     temp_bronze_match = Match(match)
    #     if temp_bronze_match.valid_data:
    #         tests.append(Team(temp_bronze_match, 'A'))
    #         tests.append(Team(temp_bronze_match, 'B'))
    #
    # for match in grand_data:
    #     temp_grand_match = Match(match)
    #     if temp_grand_match.valid_data:
    #         g_teams.append(Team(temp_grand_match, 'A'))
    #         g_teams.append(Team(temp_grand_match, 'B'))
    #
    # save_teams(tests, "test_bronze_teams.pkl")
    # save_teams(g_teams, "grand_teams.pkl")

    with open('grand_teams.pkl', 'rb') as f:
        g_teams = pickle.load(f)

    with open('test_bronze_teams.pkl', 'rb') as f:
        tests = pickle.load(f)

    df = pd.DataFrame({'winner': [], 'jaccard_values': [], 'cosine_values': []})

    for i, test in enumerate(tests):
        best_grand_jaccard_index, best_grand_cosine_index = get_best_similar(test, g_teams)
        best_jaccard_full_sim = get_sim_jac(test, g_teams[best_grand_jaccard_index], min(len(test.items),
                                                                                       len(g_teams[
                                                                                               best_grand_jaccard_index].items)))
        best_cosine_full_sim = get_sim_cos(test, g_teams[best_grand_cosine_index], min(len(test.items),
                                                                                     len(g_teams[
                                                                                             best_grand_cosine_index].items)))

        df.loc[i] = [best_cosine_full_sim, best_jaccard_full_sim, test.winners]

    plt.hist(x=df['cosine_values'], y=df['winner'])
    plt.hist(x=df['jaccard_values'], y=df['winner'])
    plt.xlabel('values')
    plt.ylabel('winner')
    plt.show()


def check_grand_bronze_win_lose_correlation():
    with open('timelines_bronze.pkl', 'rb') as f:
        bronze_data = pickle.load(f)

    with open('timelines_grandmaster2.pkl', 'rb') as f:
        grand_data = pickle.load(f)

    tests = []
    g_teams = []

    for match in bronze_data:
        temp_bronze_match = Match(match)
        if temp_bronze_match.valid_data:
            tests.append(Team(temp_bronze_match, 'A'))
            tests.append(Team(temp_bronze_match, 'B'))

    for match in grand_data:
        temp_grand_match = Match(match)
        if temp_grand_match.valid_data:
            g_teams.append(Team(temp_grand_match, 'A'))
            g_teams.append(Team(temp_grand_match, 'B'))

    for test in tests:
        best_grand_jaccard_index, best_grand_cosine_index = get_best_similar(test, g_teams)
        # best_jaccard_5min_sim = get_sim_jac(test, g_teams[best_grand_jaccard_index])
        # best_cosine_5min_sim = get_sim_cos(test, g_teams[best_grand_cosine_index])
        best_jaccard_full_sim = get_sim_jac(test, g_teams[best_grand_jaccard_index], min(len(test.items),
                                                                                       len(g_teams[
                                                                                               best_grand_jaccard_index].items)))
        best_cosine_full_sim = get_sim_cos(test, g_teams[best_grand_cosine_index], min(len(test.items),
                                                                                     len(g_teams[
                                                                                             best_grand_cosine_index].items)))
# if test.winners == g_teams[best_grand_cosine_index].winners:
#     cosine_trues += 1
#     average_cosine_value_trues += best_cosine_full_sim
# else:
#     cosine_falses += 1
#     average_cosine_value_falses += best_cosine_full_sim
# if test.winners == g_teams[best_grand_jaccard_index].winners:
#     jaccard_trues += 1
#     average_jaccard_value_trues += best_jaccard_full_sim
# else:
#     jaccard_falses += 1
#     average_jaccard_value_falses += best_jaccard_full_sim

# print(f"similar to cosine? - {cosine_trues}. what was the full average prediction? - "
#       f"{average_cosine_value_trues/cosine_trues} cosine.")
# print(f"not similar to cosine? - {cosine_falses}. what was the full average prediction? - "
#       f"{average_cosine_value_falses/cosine_falses} cosine.")
# print(f"similar to jaccard? - {jaccard_trues}. what was the full average prediction? - "
#       f"{average_jaccard_value_trues/jaccard_trues} jaccard.")
# print(f"not similar to jaccard? - {jaccard_falses}. what was the full average prediction? - "
#       f"{average_jaccard_value_falses/jaccard_falses} jaccard.")

# print(f"first 5 minutes similarities: jaccard - {best_jaccard_5min_sim}, cosine - {best_cosine_5min_sim}")
# print(f"full time similarities: jaccard - {best_jaccard_full_sim}, cosine - {best_cosine_full_sim}")
# print(f"bronze won? {test.winners},\njaccard grand won? - {g_teams[best_grand_jaccard_index].winners},\n"
#       f"cosine grand "
#       f"won? - {g_teams[best_grand_cosine_index].winners}")

    # for test in tests:
    #     best_grand_jaccard_index, best_grand_cosine_index = get_best_similar(test, g_teams)
    #     # best_jaccard_5min_sim = get_sim_jac(test, g_teams[best_grand_jaccard_index])
    #     # best_cosine_5min_sim = get_sim_cos(test, g_teams[best_grand_cosine_index])
    #     best_jaccard_full_sim = get_sim_jac(test, g_teams[best_grand_jaccard_index], min(len(test.items),
    #                                                                                    len(g_teams[
    #                                                                                            best_grand_jaccard_index].items)))
    #     best_cosine_full_sim = get_sim_cos(test, g_teams[best_grand_cosine_index], min(len(test.items),
    #                                                                                  len(g_teams[
    #                                                                                          best_grand_cosine_index].items)))
        # if test.winners == g_teams[best_grand_cosine_index].winners:
        #     cosine_trues += 1
        #     average_cosine_value_trues += best_cosine_full_sim
        # else:
        #     cosine_falses += 1
        #     average_cosine_value_falses += best_cosine_full_sim
        # if test.winners == g_teams[best_grand_jaccard_index].winners:
        #     jaccard_trues += 1
        #     average_jaccard_value_trues += best_jaccard_full_sim
        # else:
        #     jaccard_falses += 1
        #     average_jaccard_value_falses += best_jaccard_full_sim

    # print(f"similar to cosine? - {cosine_trues}. what was the full average prediction? - "
    #       f"{average_cosine_value_trues/cosine_trues} cosine.")
    # print(f"not similar to cosine? - {cosine_falses}. what was the full average prediction? - "
    #       f"{average_cosine_value_falses/cosine_falses} cosine.")
    # print(f"similar to jaccard? - {jaccard_trues}. what was the full average prediction? - "
    #       f"{average_jaccard_value_trues/jaccard_trues} jaccard.")
    # print(f"not similar to jaccard? - {jaccard_falses}. what was the full average prediction? - "
    #       f"{average_jaccard_value_falses/jaccard_falses} jaccard.")

    # print(f"first 5 minutes similarities: jaccard - {best_jaccard_5min_sim}, cosine - {best_cosine_5min_sim}")
    # print(f"full time similarities: jaccard - {best_jaccard_full_sim}, cosine - {best_cosine_full_sim}")
    # print(f"bronze won? {test.winners},\njaccard grand won? - {g_teams[best_grand_jaccard_index].winners},\n"
    #       f"cosine grand "
    #       f"won? - {g_teams[best_grand_cosine_index].winners}")



if __name__ == '__main__':
    check_grand_bronze_sim_correlation()
    # check_grand_bronze_win_lose_correlation()
