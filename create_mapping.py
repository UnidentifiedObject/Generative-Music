#create_mapping.py
import pretty_midi
import pickle
import os

def create_pitch_mappings(midi_folder='midi_files'):
    pitch_set = set()

    # Loop through all MIDI files in the folder
    for midi_file in os.listdir(midi_folder):
        if midi_file.endswith('.mid') or midi_file.endswith('.midi'):
            midi_path = os.path.join(midi_folder, midi_file)
            try:
                midi_data = pretty_midi.PrettyMIDI(midi_path)
                for instrument in midi_data.instruments:
                    for note in instrument.notes:
                        pitch_set.add(note.pitch)  # store integer pitch
            except Exception as e:
                print(f"Error processing {midi_file}: {e}")

    # Sort and map pitches to integers
    sorted_pitches = sorted(pitch_set)
    pitch_to_int = {pitch: idx for idx, pitch in enumerate(sorted_pitches)}
    int_to_pitch = {idx: pitch for pitch, idx in pitch_to_int.items()}

    # Save mappings
    os.makedirs('models', exist_ok=True)
    with open('models/pitch_to_int.pkl', 'wb') as f:
        pickle.dump(pitch_to_int, f)
    with open('models/int_to_pitch.pkl', 'wb') as f:
        pickle.dump(int_to_pitch, f)

    print(f"Saved {len(pitch_to_int)} pitch mappings to 'models/pitch_to_int.pkl' and 'int_to_pitch.pkl'.")

# Run it
if __name__ == '__main__':
    create_pitch_mappings()
