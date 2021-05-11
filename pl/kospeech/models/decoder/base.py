# Copyright (c) 2021, Soohwan Kim. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch
import torch.nn as nn
from torch import Tensor
from typing import Optional


class DecoderInterface(nn.Module):
    def __init__(self):
        super(DecoderInterface, self).__init__()

    def count_parameters(self) -> int:
        """ Count parameters of encoder """
        return sum([p.numel for p in self.parameters()])

    def update_dropout(self, dropout_p: float) -> None:
        """ Update dropout probability of encoder """
        for name, child in self.named_children():
            if isinstance(child, nn.Dropout):
                child.p = dropout_p


class BaseDecoder(DecoderInterface):
    """ ASR Decoder Super Class for KoSpeech model implementation """
    def __init__(self):
        super(BaseDecoder, self).__init__()

    def forward(self, targets: Tensor, encoder_outputs: Tensor, **kwargs) -> Tensor:
        """
        Forward propagate a `encoder_outputs` for training.

        Args:
            targets (torch.LongTensr): A target sequence passed to decoder. `IntTensor` of size ``(batch, seq_length)``
            encoder_outputs (torch.FloatTensor): A output sequence of encoder. `FloatTensor` of size
                ``(batch, seq_length, dimension)``

        Returns:
            * predicted_log_probs (torch.FloatTensor): Log probability of model predictions.
        """
        raise NotImplementedError


class IncrementalDecoder(DecoderInterface):
    def __init__(self):
        super(IncrementalDecoder, self).__init__()

    def forward(
            self,
            encoder_outputs: Tensor = None,
            targets: Optional[Tensor] = None,
            encoder_output_lengths: Optional[Tensor] = None,
            teacher_forcing_ratio: float = 1.0,
    ) -> Tensor:
        raise NotImplementedError