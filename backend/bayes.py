import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB, CategoricalNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

def naive_bayes_prediction(file_path, target_column, model_type='gaussian'):
    data = pd.read_csv(file_path)


    X = data.drop(columns=[target_column])
    y = data[target_column]

    encoders = {}
    for column in X.columns:
        if X[column].dtype == 'object':
            encoder = LabelEncoder()
            X[column] = encoder.fit_transform(X[column])
            encoders[column] = encoder
    
    if y.dtype == 'object':
        y_encoder = LabelEncoder()
        y = y_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    if model_type == 'gaussian':
        model = GaussianNB()
    elif model_type == 'multinomial':
        model = MultinomialNB()
    elif model_type == 'categorical':
        model = CategoricalNB()
    else:
        raise ValueError("Invalid model type. Choose from 'gaussian', 'multinomial', or 'categorical'.")

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    if y.dtype == 'object':
        y_pred = y_encoder.inverse_transform(y_pred)


# Change later
    if type(y.as_integer_ratio()):
        y_test = None
        int_ratio = []
        for i in int_ratio:
            for j in int_ratio:
                pass



    return {
        "accuracy": accuracy,
        "classification_report": report,
        "predictions": y_pred
    }

