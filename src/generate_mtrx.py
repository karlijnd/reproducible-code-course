import json
import os
import pickle
import random
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
import tqdm
from scipy import sparse
from sklearn.model_selection import train_test_split

dataset_location = 'data/raw/LFM-1b/LFM-1b_LEs.txt'
gender_location = 'data/raw/lfm-gender.json'

def split(test_size, artists_gender, dataset_location):
    '''
    5 subsets are made from the original artist gender file.
    Testset size is set to be 20% of the full dataset by default.
    '''
    artists_catalog = {}
    artists_users = {}
    last_user = None
    fan_data_play = []
    fan_row_train = []
    fan_col_train = []
    fan_test_data = []
    test_data = []
    data_train = []
    row_train = []
    col_train = []
    fan_user_ids = []
    fan_item_ids = []
    fan_items_dict = {}
    fan_users_dict = {}
    counts_dict = {}
    user_pos = {}

    count = 0
    for line in tqdm.tqdm(open(dataset_location)):
        # Make new entry for each artist in catalog, if gender is available
        hists = line.strip().split('\t')
        user_pos[hists[0]] = count
        if hists[1] in artists_gender:
            # Gender is available for this particular artist
            if hists[1] not in artists_catalog:
                artists_catalog[hists[1]] = set()
            artists_catalog[hists[1]].add(hists[3])
            if hists[1] not in artists_users:
                artists_users[hists[1]] = set()
            artists_users[hists[1]].add(hists[0])
        count += 1

    count = 0
    for line in tqdm.tqdm(open(dataset_location)):
        hists = line.strip().split('\t')
        if hists[0] not in counts_dict:
            counts_dict[hists[0]] = {}
        if hists[1] not in counts_dict[hists[0]]:
            counts_dict[hists[0]][hists[1]] = {'t': 0}
        counts_dict[hists[0]][hists[1]]['t'] += 1
        last_user = hists[0]

        if user_pos[last_user] == count:
            counts = counts_dict[last_user]
            artist_fan = []
            for a in counts.keys():
                if  (a not in artists_gender) or len(artists_users[a]) < 30:
                    continue
                total_tracks_listen = counts[a]['t']
                artist_fan.append((a, total_tracks_listen))
            if len(artist_fan) <= 10:
                count +=1
                del counts_dict[last_user]
                continue
            del counts_dict[last_user]

            artist_fan_dict = {a:1 for a in artist_fan}
            if last_user in fan_users_dict:
                print ("PROBLEM!!!!")
            fan_users_dict[last_user] = len(fan_user_ids)
            fan_user_ids.append(last_user)
            random.shuffle(artist_fan)
            split = round(len(artist_fan)*test_size)
            train_u = artist_fan[split:]
            test_u = artist_fan[:split]

            for item, play in train_u:
                if item not in fan_items_dict:
                    fan_items_dict[item] = len(fan_item_ids)
                    fan_item_ids.append(item)
                fan_col_train.append(fan_items_dict[item])
                fan_row_train.append(fan_users_dict[last_user])
                fan_data_play.append(play)
            fan_test_u = []
            for item, play in test_u:
                if item not in fan_items_dict:
                    fan_items_dict[item] = len(fan_item_ids)
                    fan_item_ids.append(item)
                fan_test_u.append((fan_items_dict[item], play))
            fan_test_data.append(fan_test_u)
        count += 1
    return fan_data_play, fan_row_train, fan_col_train, fan_test_data, fan_items_dict, fan_users_dict

if __name__== "__main__":

    # Make sure there is an output folder
    Path("data/processed/").mkdir(parents=True, exist_ok=True)

    artists_gender = json.load(open(gender_location))
    fan_data_play, fan_row_train, fan_col_train, fan_test_data, fan_items_dict, fan_users_dict= split(0.2, artists_gender, dataset_location)

    # TODO the commands below are not working due to the artificially small dataset used for the course's purposes
    #fan_train_play = sparse.coo_matrix((fan_data_play, (fan_row_train, fan_col_train)), dtype=np.float32)
    #print("TRAIN USERS", fan_train_play.shape)
    #sparse.save_npz(os.path.join('data', 'processed', 'rain_data_playcount.npz'), fan_train_play)
    pickle.dump(fan_test_data, open(os.path.join('data', 'processed', 'test_data.pkl'), 'wb'))
    pickle.dump(fan_items_dict, open(os.path.join('data','processed', 'items_dict.pkl'), 'wb'))
    pickle.dump(fan_users_dict, open(os.path.join('data','processed', 'users_dict.pkl'), 'wb'))
