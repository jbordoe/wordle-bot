import argparse
import logging
import os

import torch
import torch.nn as nn

from lib.nn.wordle_encoder import WordleEncoder
from lib.nn.wordle_guesser_model import WordleGuesserModel


def train_model(
    data_filepath: str,
    model_output_path: str,
    epochs: int = 200,
):
    with open(data_filepath, "r") as f:
        data = f.read().split("\n")
        train_data = [x.split(" -> ") for x in data if x]
        input_strs = [x[0] for x in train_data]
        target_strs = [x[1] for x in train_data]

    encoded_inputs = [WordleEncoder.encode_game_state(string) for string in input_strs]
    encoded_labels = [WordleEncoder.encode_label(word) for word in target_strs]

    letter_idxs = torch.tensor([[value for (value, _) in x] for x in encoded_inputs])
    state_idxs = torch.tensor([[state for (_, state) in x] for x in encoded_inputs])
    labels = torch.tensor(encoded_labels)

    model = WordleGuesserModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    # The loss function is cross-entropy.
    criterion = nn.CrossEntropyLoss()

    seq_len = WordleEncoder.SEQ_LEN
    for epoch in range(epochs):
        model.train()

        # Get the model's predictions for the current batch of inputs.
        # Dimensions: (batch_size, seq_len, vocab_size)
        # e.g. with 100 5-letter inputs (100, 5, 26)
        logits = model(letter_idxs, state_idxs)

        loss = sum(
            criterion(
                logits[:, i, :], # for each input, vocab_size predictions
                labels[:, i] # for each input, the seq_len correct labels
            )
            for i in range(seq_len)
        )
        # set model gradients to zero
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 20 == 0:
            logging.info(f"Epoch {epoch}, loss: {loss.item():.4f}")

    torch.save(model.state_dict(), model_output_path)
    logging.info(f"Model saved to {model_output_path}")

    # Predict
    model.eval()
    # with torch.no_grad():
    #     out_logits = model(letter_idxs, state_idxs)
    #     preds = out_logits.argmax(dim=-1)  # (B, 5)
    #     for i in range(len(input_strs)):
    #         pred_word = ''.join(chr(c + ord('A')) for c in preds[i])
    #         # print(f"{input_strs[i]} -> {pred_word} (target: {target_strs[i]})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a neural network for Wordle guessing."
    )
    parser.add_argument(
        "-d",
        "--data_path",
        type=str,
        required=True,
        help="Path to the training data file.",
    )
    parser.add_argument(
        "-o",
        "--output_model_path",
        type=str,
        default="models/wordle_guesser.pth",
        help="Path to save the trained model.",
    )
    parser.add_argument(
        "-e",
        "--epochs",
        type=int,
        default=200,
        help="Number of training epochs (default: 200).",
    )
    args = parser.parse_args()

    # Ensure the output directory exists
    import os
    os.makedirs(os.path.dirname(args.output_model_path), exist_ok=True)

    train_model(args.data_path, args.output_model_path, epochs=args.epochs)
