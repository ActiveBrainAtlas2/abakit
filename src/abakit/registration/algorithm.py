"""Some registration-related algorithms."""
import numpy as np


def umeyama(src, dst, with_scaling=True):
    """The Umeyama algorithm to register landmarks with rigid transform.

    See the paper "Least-squares estimation of transformation parameters
    between two point patterns".
    """
    src = np.array(src)
    dst = np.array(dst)
    assert src.shape == dst.shape
    assert len(src.shape) == 2
    dim, n_pts = src.shape

    src_mean = np.mean(src, axis=1).reshape(-1, 1)
    dst_mean = np.mean(dst, axis=1).reshape(-1, 1)

    src_demean = src - src_mean
    dst_demean = dst - dst_mean

    u, s, vh = np.linalg.svd(dst_demean @ src_demean.T / n_pts)

    # deal with reflection
    e = np.ones(dim)
    if np.linalg.det(u) * np.linalg.det(vh) < 0:
        print("reflection detected")
        e[-1] = -1

    r = u @ np.diag(e) @ vh

    if with_scaling:
        src_var = (src_demean ** 2).sum(axis=0).mean()
        c = sum(s * e) / src_var
        r *= c

    t = dst_mean - r @ src_mean

    return r, t
