# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import numpy as np
    
class Oscillator(nn.Module):
    
    def __init__(self):
        super(Oscillator, self).__init__()
        self.apply(self.init_parameters)
    
    def init_parameters(self, m):
        pass

    def forward(self, x):
        pass
    
class HarmonicOscilattors(Oscillator):
    
    def __init__(self, sample_rate, block_size):
        super(Oscillator, self).__init__()
        self.apply(self.init_parameters)
        self.upsample = nn.Upsample(scale_factor = block_size, mode="linear")
        self.sample_rate = sample_rate
    
    def init_parameters(self, m):
        pass
    
    def forward(self, z):
        # Retrieve synth parameters
        amp, alpha, f0 = z
        # Upsample parameters
        f0          = self.upsample(f0.transpose(1,2)).squeeze(1) / self.sample_rate
        amp         = self.upsample(amp.transpose(1,2)).squeeze(1)
        alpha       = self.upsample(alpha.transpose(1,2)).transpose(1,2)
        # Generate phase
        phi = torch.zeros(f0.shape).to(f0.device)
        for i in np.arange(1,phi.shape[-1]):
            phi[:,i] = 2 * np.pi * f0[:,i] + phi[:,i-1]
        phi = phi.unsqueeze(-1).expand(alpha.shape)
        # Filtering above Nyquist
        antia_alias = (self.k * f0.unsqueeze(-1) < .5).float()
        # Generate the output signal
        y =  amp * torch.sum(antia_alias * alpha * torch.sin(self.k * phi), -1)
        return y