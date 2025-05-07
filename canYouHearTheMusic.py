import pretty_midi
import os
from extract_notes import extract_note_sequence
from prepare_data import prepare_sequences  # Import the data preparation function
from train_model import train_music_model  # Import the model training function

# Path to your MIDI files
MIDI_FOLDER = 'midi_files'

# List all MIDI files in the folder
midi_files = [f for f in os.listdir(MIDI_FOLDER) if f.endswith('.mid') or f.endswith('.midi')]

if not midi_files:
    print("No MIDI files found in the 'midi_files/' folder.")
    exit()

# Loop through all MIDI files and process them
all_notes = []
for midi_file in midi_files:
    midi_path = os.path.join(MIDI_FOLDER, midi_file)
    print(f"\nProcessing {midi_file}...")

    # Load the MIDI file and extract notes
    try:
        notes = extract_note_sequence(midi_path)  # Extract notes from each file
        all_notes.extend(notes)  # Add the extracted notes from this file to the list
        print(f"Loaded '{midi_file}' successfully!\n")
    except Exception as e:
        print(f"Error loading MIDI file '{midi_file}': {e}")
        continue  # Skip to next file if there's an error

# Prepare data sequences for training
sequence_length = 50
X, Y, pitch_to_int, int_to_pitch = prepare_sequences(all_notes, sequence_length)

print(f"Prepared {len(X)} sequences for training.")


train_music_model(X, Y, pitch_to_int, int_to_pitch)  # Train the model on the prepared data

