#extract_codes
import pretty_midi


# Function to extract note sequences from a given MIDI file
def extract_note_sequence(midi_file):
    # Load MIDI file
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    notes = []  # To store the extracted note data

    # Loop through all instruments in the MIDI file
    for instrument in midi_data.instruments:
        if instrument.is_drum:  # Skip drums if you don't need them
            continue

        # Extract each note's pitch, start time, and velocity
        for note in instrument.notes:
            notes.append((note.pitch, note.start, note.velocity))  # Store note info

    return notes


# Example usage
if __name__ == "__main__":
    # Set path to your MIDI file
    midi_file = 'midi_files/beethoven.mid'  # Change this to your actual file
    notes = extract_note_sequence(midi_file)

    # Print the first 10 notes as a preview
    print(notes[:10])
