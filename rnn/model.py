import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F

'''
An RNN feeds into an embedding to encode for an RNN unit to process, then a linear layer to decode into a next word in generation
'''
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, model_type="gru", n_layers=1):
        super(RNN, self).__init__()
        self.model = model_type.lower()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers

        self.encoder = nn.Embedding(input_size, hidden_size)
        if self.model == "gru":
            self.rnn = nn.GRU(hidden_size, hidden_size, n_layers)
        elif self.model == "lstm":
            self.rnn = nn.LSTM(hidden_size, hidden_size, n_layers)
        self.decoder = nn.Linear(hidden_size, output_size)

    def forward(self, input, hidden):
        batch_size = input.size(0)
        encoded = self.encoder(input)
        output, hidden = self.rnn(encoded.view(1, batch_size, -1), hidden)
        output = self.decoder(output.view(batch_size, -1))
        return output, hidden
    
    '''
    The forward pass requires a hidden matrix as a parameter to learn when generating text.
    We start by initializing this matrix to zeros
    '''
    def init_hidden(self, batch_size, device):
        if self.model == "lstm":
            return (Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size)).to(device),
                    Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size)).to(device))
        return Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size)).to(device)
