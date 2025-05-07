#prepare_data.py
import numpy as np
from extract_notes import extract_note_sequence


def prepare_sequences(notes, sequence_length=50):
    """
    Prepare sequences of notes for training.

    Args:
    - notes: List of extracted notes [(pitch, start_time, velocity), ...]
    - sequence_length: Length of the input sequence

    Returns:
    - X: Input data (sequences)
    - Y: Output data (next note)
    """
    pitch_values = sorted(set(note[0] for note in notes))  # Unique pitch values
    pitch_to_int = {pitch: number for number, pitch in enumerate(pitch_values)}  # Mapping from pitch to integer
    int_to_pitch = {number: pitch for pitch, number in pitch_to_int.items()}  # Reverse mapping

    # Normalize velocities (0 to 127)
    max_velocity = max(note[2] for note in notes)

    sequences = []
    targets = []

    # Create input-output pairs
    for i in range(len(notes) - sequence_length):
        seq_in = notes[i:i + sequence_length]
        seq_out = notes[i + sequence_length]

        # Convert notes to integers
        seq_in_int = [pitch_to_int[note[0]] for note in seq_in]
        seq_out_int = pitch_to_int[seq_out[0]]  # Output is the next note's pitch

        sequences.append(seq_in_int)
        targets.append(seq_out_int)

    # Reshape sequences for training
    X = np.array(sequences)
    Y = np.array(targets)

    return X, Y, pitch_to_int, int_to_pitch


# Example usage
if __name__ == "__main__":
    midi_file = 'midi_files/beethoven.mid'  # Your MIDI file
    notes = extract_note_sequence(midi_file)

    # Prepare the sequences and targets for training
    X, Y, pitch_to_int, int_to_pitch = prepare_sequences(notes, sequence_length=50)

    print(f"Prepared {len(X)} sequences for training.")
