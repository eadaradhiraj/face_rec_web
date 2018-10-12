import pickle
import face_recognition

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
present = []
c = []


def predict(X_img_path, knn_clf=None, model_path=None, DIST_THRESH=0.6):
    """
    Recognizes faces in given image using a trained KNN classifier
    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object.
                    If not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled knn classifier.
                        If not specified, model_save_path must be knn_clf.
    :param DIST_THRESH: (optional) distance threshold for face classification.
                        The larger it is, the more chance of mis-classifying
                        an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces
             in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'unknown' will be returned.
    """

    if knn_clf is None and model_path is None:
        raise Exception(
            "must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(
        X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <=
                   DIST_THRESH for i in range(len(X_face_locations))]

    # Predict classes and remove classifications
    # that aren't within the threshold
    return [
        {'name': pred, 'dims': loc} if rec else ("unknown", loc)
        for pred, loc, rec in
        zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)
    ]


if __name__ == '__main__':
    recs = predict(X_img_path='static/data/test/captured_image.jpg',
                   model_path="static/data/knn_model.sav")
    print(recs)
