#!/usr/bin/env python3

import numpy as np
import csv
import scipy.sparse as sp
import pandas as pd
from implicit.bpr import BayesianPersonalizedRanking as bpr_rec
import utils.paths as paths
import logging
import pickle

'''
    Matrx.py takes fandom names and creates a sparse matrix of users who have
    given a fanwork kudos.

    Then trains a model using a Bayesian Personalized Ranking algorithm for
    implicit recommendations.

    Finally the model and lookup indices are saved as pkl objects (that can be
    then be pulled for the microservice to run inference on.)

    TODO:
        * Automate reading in all fanworks (vs. hardcoding)
        * add code to generate date sensitive models (place in sequential
            folders?)
'''


def create_logger():
    # Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(paths.model_log_path(), mode='w')
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def create_path_list():
    # Create paths for each fandom
    fandom1 = 'Star Wars: Rebels'
    fandom2 = 'Star Wars: The Clone Wars (2008) - All Media Types'

    kudo1 = paths.kudo_path(fandom1)
    kudo2 = paths.kudo_path(fandom2)

    meta1 = paths.meta_path(fandom1)
    meta2 = paths.meta_path(fandom2)

    # Will need this to read the files
    kudo_files = [kudo1, kudo2]
    meta_files = [meta1, meta2]

    return kudo_files, meta_files


def create_megaframe(kudo_files):
    # Create mega dataframe

    frames = []
    for path in kudo_files:
        frames.append(pd.read_csv(path))
    df = pd.concat(frames)
    return df


def create_empty_df(df):
    # Determine unique work and user sizes to make emtpy DF
    num_works = len(df['work_id'].unique())
    num_users = len(df['user'].unique())
    data = np.zeros((num_works, num_users))
    return data


def invert_indices(indices):
    # create inverted indices for reverse lookup
    inverted_indices = {'work_id': {}, 'user': {}}
    inverted_indices['work_id'] = {v: k for k, v in indices['work_id'].items()}
    inverted_indices['user'] = {v: k for k, v in indices['user'].items()}

    return inverted_indices


def create_sparse_matrix(data, kudo_files):
    # create indices for work_id and users
    indices = {'work_id': {}, 'user': {}}

    # then go through each line of csv files for values to set to 1
    for fandom in kudo_files:
        with open(fandom, newline='') as csvfile:
            interactions = csv.reader(csvfile, delimiter=',')
            next(interactions)
            for row in interactions:
                indices['work_id'].setdefault(row[0], len(indices['work_id']))
                indices['user'].setdefault(row[1], len(indices['user']))
                data[indices['work_id'][row[0]]][indices['user'][row[1]]] = 1
    return data, indices


def test_predictions(indices, inverted_indices, id):
    work_indice = indices['work_id'][id]
    num_to_return = 20

    # find related items
    related_BPR = modelBPR.similar_items(work_indice, num_to_return)
    for suggestion in related_BPR:
        work_id = inverted_indices['work_id'][suggestion[0]]
        print(f"http://www.archiveofourown.org/works/{work_id}")


def store_data(model, indices, meta_df):
    # Write out model and indices dictionary as pkl files
    # Write out lookup_table/meta_df as csv file
    # All three will be used for infererncing

    with open(paths.pickle_path(), 'wb') as m_out:
        pickle.dump(model, m_out)

    with open(paths.inidices_path(), 'wb') as i_out:
        pickle.dump(indices, i_out)

    smaller_df = meta_df[['work_id', 'title', 'author', 'rating']]
    smaller_df.to_csv(paths.lookup_table_path(), index=False)

    return


if __name__ == "__main__":
    logger = create_logger()
    kudo_list, meta_list = create_path_list()

    kudo_df = create_megaframe(kudo_list)
    meta_df = create_megaframe(meta_list)

    logger.info(f"Reading in kudos.")
    empty_df = create_empty_df(kudo_df)

    logger.info(f"Creating empty matrix.")
    data, indices = create_sparse_matrix(empty_df, kudo_list)
    logger.info(f" completed size: {data.shape}")

    # train the model on a sparse matrix of item/user/confidence weights
    logger.info(f"Training model")
    modelBPR = bpr_rec(factors=50, verify_negative_samples=True)
    modelBPR.fit(sp.csr_matrix(data))

    # test_predictions(indices, invert_indices(indices), '13484820')

    logger.info(f"Storing model for late inference.")
    store_data(modelBPR, indices, meta_df)

    logger.info(f"Model building and features engineering complete.")
