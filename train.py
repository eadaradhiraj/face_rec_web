import math
from sklearn import neighbors
import os
import pickle
import face_recognition
import re

directory = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(directory, 'static', 'data')
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
MODEL_PATH = os.path.join(DATA_DIR, 'knn_model.sav')


def image_files_in_folder(folder):
    return [os.path.join(folder, f)
            for f in os.listdir(folder)
            if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def train(train_dir=TRAIN_DIR,
          model_save_path=MODEL_PATH,
          n_neighbors=None, knn_algo='ball_tree', verbose=False):
    """
    Trains a k-nearest neighbors classifier for face recognition.
    :param train_dir: directory that contains a sub-directory for each
                        known person, with its name.
     (View in source code to see train_dir example tree structure)
     Structure:
        <train_dir>/
        ├── <person1>/
        │   ├── <somename1>.jpeg
        │   ├── <somename2>.jpeg
        │   ├── ...
        ├── <person2>/
        │   ├── <somename1>.jpeg
        │   └── <somename2>.jpeg
        └── ...
    :param n_neighbors: (optional) number of neighbors to weigh in
                        classification. Chosen automatically if not specified
    :param knn_algo: (optional) underlying data structure to support knn.
                    Default is ball_tree
    :param verbose: verbosity of training
    :return: returns knn classifier that was trained on the given data.
    """
    X = []
    y = []

    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in \
                image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people)
                # in a training image, skip the image.
                if verbose:
                    print(
                        "Image {} not suitable for training: {}"
                        .format(img_path, "Didn't find a face"
                                if len(
                                    face_bounding_boxes) < 1
                                else "Found more than one face")
                    )
            else:
                # Add face encoding for current image to the training set
                X.append(face_recognition.face_encodings(
                    image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(
        n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if (model_save_path is not None):
        with open('static/data/knn_model.sav', 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf


if __name__ == '__main__':
    train(train_dir='static/data/train',
          model_save_path='static/data/knn_model.sav')
