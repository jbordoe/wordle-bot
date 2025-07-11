import torch
import torch.nn as nn
import torch.nn.functional as F

from lib.nn.wordle_encoder import WordleEncoder


class WordleGuesserModel(nn.Module):
    """
    A neural network model designed to predict the next best Wordle guess
    based on the current game state.
    """
    def __init__(
        self,
        letter_emb_dim: int = 8,
        state_emb_dim: int = 4,
        hidden_dim: int = 64
    ):
        """
        Initializes the WordleGuesser model.

        Parameters:
            letter_emb_dim (int): Dimension of the letter embedding.
            state_emb_dim (int): Dimension of the state embedding.
            hidden_dim (int): Dimension of the hidden layer in the feed-forward network.
        """
        super().__init__()
        # Embedding layer for letters (A-Z and padding for '_')
        # Maps these letters to vectors of size letter_emb_dim
        # Enables model to learn relationship between letters and their embeddings
        self.letter_emb = nn.Embedding(WordleEncoder.NUM_LETTERS + 1, letter_emb_dim)
        # Embedding layer for letter states (ABSENT, PRESENT, PLACED)
        # Maps these states to vectors of size state_emb_dim
        self.state_emb = nn.Embedding(len(WordleEncoder.STATE_TO_IDX), state_emb_dim)

        # Fully connected layers
        input_fc_dim = (letter_emb_dim + state_emb_dim) * WordleEncoder.SEQ_LEN
        self.fc1 = nn.Linear(input_fc_dim, hidden_dim)
        # Output layer predicts a score for each letter at each position
        self.fc_out = nn.Linear(
            hidden_dim,
            WordleEncoder.VOCAB_SIZE * WordleEncoder.SEQ_LEN
        )

    def forward(
            self,
            letter_idxs: torch.Tensor,
            state_idxs: torch.Tensor
    ) -> torch.Tensor:
        """
        Performs a forward pass through the model.

        Args:
            letter_idxs (torch.Tensor):
                Tensor of letter indices (batch_size, SEQ_LEN).
            state_idxs (torch.Tensor):
                Tensor of state indices (batch_size, SEQ_LEN).

        Returns:
            torch.Tensor: Logits for each possible letter at each position
                          (batch_size, SEQ_LEN, VOCAB_SIZE).
        """
        # Embed letter and state indices (i.e. convert them to vectors for processing)
        # Shape: (batch_size, SEQ_LEN, letter_emb_dim)
        letter_e = self.letter_emb(letter_idxs)
        # Shape: (batch_size, SEQ_LEN, state_emb_dim)
        state_e = self.state_emb(state_idxs)

        # Concatenate letter and state embeddings along the last dimension
        # Shape: (batch_size, SEQ_LEN, letter_emb_dim + state_emb_dim)
        x = torch.cat([letter_e, state_e], dim=-1)

        # Flatten the concatenated embeddings for the fully connected layer
        # Converts the tensor from 3D to 2D, i.e. flattens the sequence of embeddings
        # from (batch_size, SEQ_LEN, letter_emb_dim + state_emb_dim)
        # to (batch_size, SEQ_LEN * (letter_emb_dim + state_emb_dim))
        x = x.view(x.size(0), -1)

        # Pass through the first fully connected layer with ReLU activation
        # Shape: (batch_size, hidden_dim)
        x = F.relu(self.fc1(x))

        # Produce raw scores (logits) for each possible letter at each position
        # Shape: (batch_size, SEQ_LEN * VOCAB_SIZE)
        logits = self.fc_out(x)

        # Reshape logits to (batch_size, SEQ_LEN, VOCAB_SIZE)
        # for per-position classification
        return logits.view(-1, WordleEncoder.SEQ_LEN, WordleEncoder.VOCAB_SIZE)
