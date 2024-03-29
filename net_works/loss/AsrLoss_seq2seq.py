import torch
from torch.nn import CTCLoss


class Seq2SeqLoss:
    def __init__(self, cfg):
        self.cfg = cfg
        self.loss_ctc = CTCLoss()
        self.loss_mse = torch.nn.MSELoss(reduction='sum')
        self.loss_ce = torch.nn.CrossEntropyLoss(reduction='sum')
        self.embedding = torch.nn.Embedding(self.cfg.TRAIN.CLASS_LENGTH, 10)

    def Loss_Call(self, pre, train_data, losstype='mse'):
        _, target, input_lengths, target_lengths = train_data
        target = target.contiguous().view(-1)  #
        pre = pre.view(-1, pre.shape[-1])
        loss = self.loss_ce(pre, target)  # 交叉熵
        loss = loss / self.cfg.TRAIN.BATCH_SIZE
        return loss, None
