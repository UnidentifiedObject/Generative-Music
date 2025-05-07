import pretty_midi

def save_midi_from_notes(note_sequence, output_path, instrument_name='Acoustic Grand Piano'):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program(instrument_name))

    start_time = 0
    duration = 0.5

    for note_name in note_sequence:
        # Here, 'note_name' is already the MIDI pitch (an integer)
        pitch = note_name  # No need for `pretty_midi.note_name_to_number()`
        note = pretty_midi.Note(velocity=100, pitch=pitch, start=start_time, end=start_time + duration)
        instrument.notes.append(note)
        start_time += duration

    midi.instruments.append(instrument)
    midi.write(output_path)
