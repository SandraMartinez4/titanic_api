import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_and_save_model():
    """Entrena y guarda un modelo de Random Forest para predecir la supervivencia."""
    # Cargar los datos del Titanic (ajusta la ruta si es necesario)
    df = pd.read_csv('train.csv')

    # Preprocesamiento de datos
    df['Sex_encoded'] = df['Sex'].map({'male': 0, 'female': 1})

    # Seleccionar las características y el objetivo
    features = ['Pclass', 'Sex_encoded', 'Age', 'Fare']
    target = 'Survived'

    # Eliminar filas con valores nulos para las características
    df = df.dropna(subset=features)

    X = df[features]
    y = df[target]

    # Entrenar el modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Guardar el modelo entrenado en un archivo
    joblib.dump(model, 'titanic_model.pkl')
    print("Modelo entrenado y guardado como 'titanic_model.pkl'")

if __name__ == "__main__":
    train_and_save_model()