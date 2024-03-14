import cv2
import numpy as np
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import tensorflow as tf


def get_volume_range():
    return 0.0, 1.0

# Function to set system volume
def set_system_volume(volume):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume_object = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume_object.SetMasterVolume(volume, None)


def preprocess_image(image):
    resized_image = cv2.resize(image, (224, 224))  
    normalized_image = resized_image / 255.0  
    return np.expand_dims(normalized_image, axis=0)  


def detect_thumb(frame, model):
    preprocessed_image = preprocess_image(frame)
    prediction = model.predict(preprocessed_image)
    if prediction[0][0] > 0.5:
        return "Thumbs up"
    else:
        return "Thumbs down"


def main():
    model = tf.keras.models.load_model('D:\\Random\\VolumeControl-main\\VolumeControl\\model\\full_model.weights.h5')  # Replace this with your model directory (the one used in main.py)

    cap = cv2.VideoCapture(0)
    min_vol, max_vol = get_volume_range()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gesture = detect_thumb(frame, model)
        print("Detected Gesture:", gesture)

        if gesture == "Thumbs up":
            volume = max_vol
        else:
            volume = min_vol

        set_system_volume(volume)

        cv2.imshow('Volume Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
