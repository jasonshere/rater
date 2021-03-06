# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

import os
import sys

import torch
import torch.nn as nn
from sklearn.metrics import roc_auc_score
from torch.utils.data.dataset import TensorDataset

sys.path.append("..")
from rater.models.ctr.fm import FM
from rater.models.model import train_model
from rater.utils.logger import logger

logger.setLevel('INFO')
pwd_path = os.path.abspath(os.path.dirname(__file__))


def train(x_idx, x_value, label, features, out_type='binary'):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    X_idx_tensor = torch.LongTensor(x_idx).to(device)
    X_value_tensor = torch.Tensor(x_value).to(device)
    y_tensor = torch.Tensor(label).to(device)
    y_tensor = y_tensor.reshape(-1, 1)

    X = TensorDataset(X_idx_tensor, X_value_tensor, y_tensor)
    model = FM(feature_size=features.feature_size(), out_type=out_type).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    model_path = os.path.join(pwd_path, 'fm_model.pt')
    model, loss_history = train_model(model=model, model_path=model_path, dataset=X, loss_func=nn.BCELoss(),
                                      optimizer=optimizer, device=device, val_size=0.2, batch_size=32, epochs=10,
                                      shuffle=True)
    print(loss_history)
    del model


def predict(x_idx, x_value, features, out_type='binary'):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    X_idx_tensor = torch.LongTensor(x_idx).to(device)
    X_value_tensor = torch.Tensor(x_value).to(device)

    X = TensorDataset(X_idx_tensor, X_value_tensor)
    model = FM(feature_size=features.feature_size(), out_type=out_type).to(device)
    from rater.models.model import predict_model
    model_path = os.path.join(pwd_path, 'fm_model.pt')
    preds = predict_model(model=model, model_path=model_path, dataset=X, device=device)
    return preds


if __name__ == '__main__':
    # load criteo sample dataset
    from rater.datasets.criteo import Criteo

    dataset = Criteo(n_samples=-1)
    # from rater.datasets.movielens import Movielens
    # dataset = Movielens(n_samples=-1)
    features, X_idx, X_value, y, category_index, continuous_value = dataset.get_features()

    print("X_idx[0], X_value[0], y[0] :\n", X_idx[0], X_value[0], y[0])
    train(X_idx, X_value, y, features)

    pred_y = predict(X_idx[:100], X_value[:100], features)
    print("truth y:", y[:100], 'pred_y', pred_y)

    score = roc_auc_score(y[:100], pred_y)
    print('auc:', score)
