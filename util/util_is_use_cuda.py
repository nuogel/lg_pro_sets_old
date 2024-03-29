import torch


def _is_use_cuda(GPU_NUM=0):
    use_cuda = False
    if GPU_NUM is not -1 and torch.cuda.is_available():
        use_cuda = True
    return use_cuda
