import pytest
import jax.numpy as jnp

from dmff import NeighborList
from dmff.utils import regularize_pairs, pair_buffer_scales


class TestNeighborList:
    
    @pytest.fixture(scope="class", name='nblist')
    def test_nblist_init(self):
        positions = jnp.array([
            [12.434,   3.404,   1.540],
            [13.030,   2.664,   1.322],
            [12.312,   3.814,   0.660],
            [14.216,   1.424,   1.103],
            [14.246,   1.144,   2.054],
            [15.155,   1.542,   0.910]
        ])
        box = jnp.array([31.289,   31.289,   31.289])
        r_cutoff = 4.0
        nbobj = NeighborList(box, r_cutoff)
        nbobj.allocate(positions)
        yield nbobj
        
    def test_update(self, nblist):

        positions = jnp.array([
            [12.434,   3.404,   1.540],
            [13.030,   2.664,   1.322],
            [12.312,   3.814,   0.660],
            [14.216,   1.424,   1.103],
            [14.246,   1.144,   2.054],
            [15.155,   1.542,   0.910]
        ])   
        nblist.update(positions)
        
    def test_pairs(self, nblist):
        
        pairs = nblist.pairs
        assert pairs.shape == (18, 2)
        
    def test_pair_mask(self, nblist):
        
        pair, mask = nblist.pair_mask
        assert mask.shape == (18, )
        
    def test_dr(self, nblist):
        
        dr = nblist.dr
        assert dr.shape == (18, 3)
        
    def test_distance(self, nblist):
        
        assert nblist.distance.shape == (18, )
    
    def test_regularize_pairs(self, nblist):
        pairs = nblist.pairs
        reg_pairs = regularize_pairs(pairs)
        buf_scales = pair_buffer_scales(reg_pairs)
        nbufs = buf_scales.shape[0] - jnp.sum(buf_scales)
        assert reg_pairs.shape == (18, 2)
        assert buf_scales.shape == (18, )
        assert nbufs == 3
        assert jnp.sum(reg_pairs[:, 0] > reg_pairs[:, 1]) == nbufs
        
