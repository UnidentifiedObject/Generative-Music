#train_model.py
import numpy as np
from keras.models import Sequential
from keras.models import load_model
from keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import pickle  # Added to save mappings
import os

def train_music_model(X, Y, pitch_to_int, int_to_pitch):
    """
    Train the music generation model with the given data.

    Args:
    - X: Input sequences (note sequences)
    - Y: Output sequences (next note prediction)
    - pitch_to_int: Mapping of pitch to integer
    - int_to_pitch: Reverse mapping of integer to pitch
    """
    if len(X) == 0 or len(Y) == 0:
        raise ValueError("Training data (X or Y) is empty!")

    # Reshape X for LSTM [samples, time steps, features]
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    X = X / float(len(pitch_to_int))  # Normalize input

    # One-hot encode the output labels
    Y = to_categorical(Y, num_classes=len(pitch_to_int))

    # Define the LSTM model
    model = Sequential()
    model.add(LSTM(512, input_shape=(X.shape[1], X.shape[2])))  # No need for 'time_major' argument
    model.add(Dropout(0.3))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(len(pitch_to_int), activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    # Ensure the models directory exists
    os.makedirs('models', exist_ok=True)

    # Train the model
    print("Training the model...")
    model.fit(X, Y, epochs=50, batch_size=64)

    # Save the trained model
    model.save('models/music_model.h5')
    print("Model training completed and saved as 'models/music_model.h5'.")

    # Save the pitch mappings for future use
    try:
        with open('models/pitch_to_int.pkl', 'wb') as f:
            pickle.dump(pitch_to_int, f)
        print("Saved 'models/pitch_to_int.pkl'.")
    except Exception as e:
        print(f"Error saving 'models/pitch_to_int.pkl': {e}")

    try:
        with open('models/int_to_pitch.pkl', 'wb') as f:
            pickle.dump(int_to_pitch, f)
        print("Saved 'models/int_to_pitch.pkl'.")
    except Exception as e:
        print(f"Error saving 'models/int_to_pitch.pkl': {e}")
