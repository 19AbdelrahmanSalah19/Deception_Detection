import os
import numpy as np
import cv2
import tensorflow as tf
import keras  # Importing Keras explicitly
from keras.models import load_model
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib


app = Flask(__name__)

CORS(app)


filename = 'random_forest_model.joblib'  # Use the same filename you used when saving the model

loaded_LRCN_model = joblib.load(filename)
#loaded_LRCN_model = load_model('Highest_LRCN_model__Date_Time_2024_04_18__19_54_17.h5')
CLASSES_LIST = ["truth", "lie"]
IMAGE_HEIGHT, IMAGE_WIDTH = 75, 75
SEQUENCE_LENGTH = 50
TEMP_DIR = 'temp_videos'

os.makedirs(TEMP_DIR, exist_ok=True)

#@app.route('/predict', methods=['POST'])
# Define a temporary directory to save the uploaded files

# Ensure the temporary directory exists

@app.route('/insertpredict', methods=['POST'])
def insertpredict():
    # Get the uploaded video file from the request
    if 'video' not in request.files:
        return jsonify({'error': 'No video file uploaded.'}), 400
    
    video_file = request.files['video']

    # Create a temporary file path for the uploaded video
    temp_file_path = os.path.join(TEMP_DIR, video_file.filename)
    
    # Save the uploaded video file temporarily
    video_file.save(temp_file_path)

    # Perform prediction using the model and the uploaded video file path
    result = predict_single_action(temp_file_path, SEQUENCE_LENGTH)

    # Delete the temporary file after prediction
    os.remove(temp_file_path)

    # Return the prediction result as JSON
    return jsonify(result)



@app.route('/capture_and_predict', methods=['POST'])
def capture_and_predict():
    video_file_path = 'output.mp4'
    # Capture video from webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return jsonify({'error': 'Failed to open the webcam.'})
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_file_path, fourcc, 50, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.putText(frame, 'Press q to quit', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            out.write(frame)
            cv2.imshow('output', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Perform prediction using the model
    result = predict_single_action(video_file_path, SEQUENCE_LENGTH)

    # Return the prediction result as JSON
    return result


def predict_single_action(video_file_path, SEQUENCE_LENGTH):
    '''
    This function performs single action recognition prediction on a video using the Random Forest model.
    
    Args:
    video_file_path: The path of the video file.
    SEQUENCE_LENGTH: The fixed number of frames of a video to be used as a sequence.
    '''

    # Initialize the VideoCapture object to read from the video file.
    video_reader = cv2.VideoCapture(video_file_path)

    # Get the width and height of the video.
    original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

    

    # Declare a list to store video frames we will extract.
    frames_list = []
    
    # Initialize a variable to store the predicted action being performed in the video.
    predicted_class_name = ''

    # Get the number of frames in the video.
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the interval after which frames will be added to the list.
    skip_frames_window = max(int(video_frames_count / SEQUENCE_LENGTH), 1)

    last_frame = None
    
    for frame_counter in range(SEQUENCE_LENGTH):
        if frame_counter < video_frames_count:
            video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

            success, frame = video_reader.read()

            if success:
                resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))

                normalized_frame = resized_frame / 255

                flattened_frame = normalized_frame.flatten()

                frames_list.append(flattened_frame)

                last_frame = normalized_frame
            else:
                break
        else:
            if last_frame is not None:
                frames_list.append(last_frame)
            else:
                break
            
        

    # Convert frames_list to a numpy array.
    frames_array = np.array(frames_list)
    frames_array = frames_array.reshape((1, frames_array.size))  # Reshape the array to (1, n_features) for Random Forest

    # Make predictions using Random Forest model
    predicted_labels_probabilities = loaded_LRCN_model.predict_proba(frames_array)[0]
    
    # Get the index of class with the highest probability.
    predicted_label = np.argmax(predicted_labels_probabilities)

    # Get the class name using the retrieved index.
    predicted_class_name = CLASSES_LIST[predicted_label]
    
    # Display the predicted action along with the prediction confidence.
    print(f'rfAction Predicted: {predicted_class_name}\nConfidence: {predicted_labels_probabilities[predicted_label]:.2f}')
        
    # Convert NumPy arrays and probabilities to native Python types
    predicted_labels_probabilities = predicted_labels_probabilities.astype(float).tolist()

    result = {
        'action': predicted_class_name,
        'confidence': float(predicted_labels_probabilities[predicted_label])
    }
    print('RESULT IS', result)
    # Release the VideoCapture object.
    video_reader.release()

    return result

if __name__ == '__main__':
    app.run(debug=True)

CORS(app, origins=['http://localhost:3000'])

#decoded_predictions = decode_predictions(predictions)

# Display the input video.
#VideoFileClip(input_video_file_path, audio=False, target_resolution=(300,None)).ipython_display()