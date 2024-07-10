# Deception_Detection
A web framework designed to detect whether a person is telling the truth or lying using machine learning techniques using visual features on the Dolos dataset. Several models, including Long-Term Recurrent Convolutional Networks (LRCN), Random Forest (RF), K-Nearest Neighbor (KNN), and Support Vector Machines (SVMs), were compared for their performance in detecting deception. The evaluation included careful hyperparameter tuning and feature selection techniques on the manually annotated features within the MUMIN scheme of the Dolos dataset, employing the Multi-Task Learning LRCN model. A Graphical User Interface (GUI) has also been developed to integrate the Random Forest model for predicting deception, enhancing its practical applications.


## Features

- **Real-time Lie Detection**: Analyzes visual features to determine if a person is lying.
- **Machine Learning Integration**: Uses advanced machine learning algorithms for high accuracy.
- **User-Friendly Interface**: Easy to use and integrate with other systems.

## Important Note

Deception detection remains a highly complex field, and accurately identifying lies is still challenging. Therefore, this application is not intended for real-world scenarios at this stage. Nevertheless, it paves the way for more reliable outputs in the future, offering a promising direction for continued research and development.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- OpenCV
- TensorFlow or PyTorch
- Dolos Dataset
- Flask
- React


### Installation

1. Clone the repository:
   

2. Install the required packages:
    

3. Download the Dolos dataset from the [Dolos Website](https://rose1.ntu.edu.sg/dataset/DOLOS/) and place it in the `data` directory.

### Usage

1. **Run the Flask Server:**

    Navigate to the client directory and start the Flask development server:
    ```bash
    cd flask-server
    python server.py
    ```

2. **Run the React Client:**

    Navigate to the client directory and start the React development server:
    ```bash
    cd client
    npm start
    ```

3. Upload a video or use your webcam to start the lie detection process.
