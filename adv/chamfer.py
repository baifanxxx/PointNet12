import torch
import numpy as np

def chamfer_non_batch(p1, p2, channal_first = False, debug=False):
    '''
    Calculate Chamfer Distance between two point sets
    :param p1: size[1, N, D]
    :param p2: size[1, M, D]
    :param debug: whether need to output debug info
    :return: sum of Chamfer Distance of two point sets
    '''

    assert p1.size(0) == 1 and p2.size(0) == 1
    assert p1.size(2) == p2.size(2)

    if debug:
        print(p1[0][0])

    p1 = p1.repeat(p2.size(1), 1, 1)
    if debug:
        print('p1 size is {}'.format(p1.size()))

    p1 = p1.transpose(0, 1)
    if debug:
        print('p1 size is {}'.format(p1.size()))
        print(p1[0])

    p2 = p2.repeat(p1.size(0), 1, 1)
    if debug:
        print('p2 size is {}'.format(p2.size()))
        print(p2[0])

    dist = torch.add(p1, torch.neg(p2))
    if debug:
        print('dist size is {}'.format(dist.size()))
        print(dist[0])

    dist = torch.norm(dist, 2, dim=2)
    if debug:
        print('dist size is {}'.format(dist.size()))
        print(dist)

    dist = torch.min(dist, dim=1)[0]
    if debug:
        print('dist size is {}'.format(dist.size()))
        print(dist)

    dist = torch.sum(dist)
    if debug:
        print('-------')
        print(dist)

    return dist

def chamfer_batch(p1, p2, debug=False):
    '''
    Calculate Chamfer Distance between two point sets
    :param p1: size[B, N, D]
    :param p2: size[B, M, D]
    :param debug: whether need to output debug info
    :return: sum of all batches of Chamfer Distance of two point sets
    '''

    assert p1.size(0) == p2.size(0) and p1.size(2) == p2.size(2)

    p1 = p1.unsqueeze(1)
    p2 = p2.unsqueeze(1)
    if debug:print('unsqueeze', p1.size(), p2.size())

    p1 = p1.repeat(1, p2.size(2), 1, 1)
    if debug:print('repeat p1', p1.size())

    p1 = p1.transpose(1, 2)
    if debug:print('transpose p1', p1.size())

    p2 = p2.repeat(1, p1.size(1), 1, 1)
    if debug:print('repeat p2', p2.size())

    dist = torch.add(p1, torch.neg(p2))
    if debug:print('dist size is {}'.format(dist.size()))

    dist = torch.norm(dist, 2, dim=3)
    if debug:print('dist size is {}'.format(dist.size()))

    dist = torch.min(dist, dim=2)[0]
    if debug:print('dist size is {}'.format(dist.size()))

    dist = torch.sum(dist)
    if debug:print(dist)

    return dist

if __name__ == '__main__':
    p1 = torch.from_numpy(np.array([[[1., 2, 3], [4, 5, 6], [3, 5, 6], [5, 6, 7]],[[2., 2, 3], [3, 5, 6], [4, 5, 6], [8, 6, 7]]]))
    p2 = torch.from_numpy(np.array([[[3., 7, 8], [1, 4, 5]],[[3., 8, 8], [2, 4, 5]]]))

    # p1 size is torch.Size([2, 4, 3]), p2 size is torch.Size([2, 2, 3])
    print('p1 size is {}, p2 size is {}'.format(p1.size(), p2.size()))
    print(chamfer_batch(p1, p2, True))
    exit()

    p1_1 = torch.from_numpy(np.array([[[1., 2, 3], [4, 5, 6], [3, 5, 6], [5, 6, 7]]]))
    p1_2 = torch.from_numpy(np.array([[[2., 2, 3], [3, 5, 6], [4, 5, 6], [8, 6, 7]]]))

    p2_1 = torch.from_numpy(np.array([[[3., 7, 8], [1, 4, 5]]]))
    p2_2 = torch.from_numpy(np.array([[[3., 8, 8], [2, 4, 5]]]))

    print(torch.add(
        chamfer_non_batch(p1_1, p2_1),
        chamfer_non_batch(p1_2, p2_2))
    )
