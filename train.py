import os
import argparse
import datetime
import six
import math
import pickle

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
from torchvision import datasets
from torchvision import transforms
from torch.autograd import Variable
from torch.nn.parameter import Parameter

# from tqdm import tqdm
import numpy as np


from models import LSTM
import util 

model = LSTM(1, 64)
model.cuda()
loss_function = F.mse_loss #nn.NLLLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)


data = pickle.load(open('data.dat', 'rb'))
Xd, yd = util.create_batches(data, batch_length=100)

# train on one stock

split = 0.8
print(Xd.shape)
X = Variable(torch.Tensor(Xd[0,:int(len(Xd[0]) * split),:])).cuda()
y = Variable(torch.Tensor(yd[0,:int(len(Xd[0]) * split),:])).cuda()
# X = Variable(torch.Tensor(Xd[0,:,:])).cuda()
# y = Variable(torch.Tensor(yd[0,:,:])).cuda()

Xtest = Variable(torch.Tensor(Xd[0,int(len(Xd[0]) * split):,:])).cuda()
ytest = Variable(torch.Tensor(yd[0,int(len(Xd[0]) * split):,:])).cuda()


#print('X', X.size())
#print('y', y.size())

#sys.exit()

# See what the scores are before training
# Note that element i,j of the output is the score for tag j for word i.
# Here we don't need to train, so the code is wrapped in torch.no_grad()
epochs = 400
for epoch in range(epochs):  # again, normally you would NOT do 300 epochs, it is toy data
    # Step 1. Remember that Pytorch accumulates gradients.
    # We need to clear them out before each instance
    model.zero_grad()

    # Also, we need to clear out the hidden state of the LSTM,
    # detaching it from its history on the last instance.
    #model.hidden = model.init_hidden()

    # Step 2. Get our inputs ready for the network, that is, turn them into
    # Tensors of word indices.
    # sentence_in = prepare_sequence(sentence, word_to_ix)
    # targets = prepare_sequence(tags, tag_to_ix)

    # Step 3. Run our forward pass.
    results = model(X)

    # Step 4. Compute the loss, gradients, and update the parameters by
    #  calling optimizer.step()
    loss = loss_function(results, y)
    loss.backward()
    optimizer.step()

    print(epoch, loss)

    with torch.no_grad():

        results = model(Xtest)
        loss = loss_function(results, ytest)

        print(loss)

# PATH = 'model1.model'
# torch.save(model.state_dict(), PATH)

# model = LSTM(1, 100)
# model.load_state_dict(torch.load(PATH))

