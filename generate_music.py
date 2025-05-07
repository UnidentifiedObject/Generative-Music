#generate_music
import numpy as np
import random
import pickle
from tensorflow.keras.models import load_model


def generate_music(model_path, seed_sequence, int_to_pitch, pitch_to_int, num_notes=100):
    model = load_model(model_path)
    vocab_size = len(pitch_to_int)

    # Print out the seed sequence to debug
    print("Seed sequence before filtering unknown notes:", seed_sequence)

    # Initialize pattern with the notes found in the seed sequence
    pattern = []
    for note in seed_sequence:
        # If the note's pitch is in pitch_to_int, use it; otherwise, print a warning and skip
        if note[0] in pitch_to_int:
            pattern.append(pitch_to_int[note[0]])
        else:
            print(f"Warning: Pitch {note[0]} not found in pitch_to_int dictionary, skipping note.")
            continue  # Skip the note if it's not found in the dictionary

    # Check if pattern is empty after filtering
    if len(pattern) == 0:
        raise ValueError("Seed sequence is empty after filtering unknown notes.")

    generated = []

    for _ in range(num_notes):
        # Reshape the input sequence for the model
        input_sequence = np.reshape(pattern, (1, len(pattern), 1))
        input_sequence = input_sequence / float(vocab_size)

        # Get model predictions
        prediction = model.predict(input_sequence, verbose=0)
        index = np.argmax(prediction)  # Get the most likely next note
        result = int_to_pitch[index]  # Convert index to pitch
        generated.append(result)

        # Add the predicted note to the pattern and update the sequence
        pattern.append(index)
        pattern = pattern[1:]

    return generated

