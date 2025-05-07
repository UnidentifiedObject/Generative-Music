# Generate_and_save_music.py
# This file generates the music
import pickle
import random
from generate_music import generate_music
from create_midi import save_midi_from_notes  # You'll create this next
from extract_notes import extract_note_sequence
import os

# Load mappings
with open('models/pitch_to_int.pkl', 'rb') as f:
    pitch_to_int = pickle.load(f)

with open('models/int_to_pitch.pkl', 'rb') as f:
    int_to_pitch = pickle.load(f)


# Load seed notes from all MIDI files in the 'midi_files' directory
midi_folder = 'midi_files'
seed_notes = []

for filename in os.listdir(midi_folder):
    if filename.lower().endswith('.mid'):
        file_path = os.path.join(midi_folder, filename)
        notes = extract_note_sequence(file_path)
        seed_notes.extend(notes)

sequence_length = 50
start_index = random.randint(0, len(seed_notes) - sequence_length - 1)
seed_sequence = seed_notes[start_index:start_index + sequence_length]

# Check the format of the seed sequence (first 10 notes)

model_path = 'models/music_model.h5'

# Generate new music
generated_notes = generate_music(
    model_path=model_path,
    seed_sequence=seed_sequence,
    int_to_pitch=int_to_pitch,
    pitch_to_int=pitch_to_int,
    num_notes=100
)


# Generate a unique filename in the "outputMusic" folder
def get_unique_filename(base_name='generated_music', extension='.mid', folder='outputMusic'):
    # Ensure the output folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Check existing files and create a unique name
    i = 1
    while os.path.exists(f"{folder}/{base_name}{i}{extension}"):
        i += 1
    return f"{folder}/{base_name}{i}{extension}"


# Save generated notes to a MIDI file in the "outputMusic" folder
output_path = get_unique_filename('generated_music', '.mid')
save_midi_from_notes(generated_notes, output_path=output_path)

print(f"Generated music saved as '{output_path}'")
