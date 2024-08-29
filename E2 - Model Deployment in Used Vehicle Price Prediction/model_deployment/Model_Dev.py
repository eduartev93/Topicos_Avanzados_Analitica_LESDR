
import pandas as pd
import joblib
import sys
import os

def predict_price(mileage, year, state, model, make):
    # Cargar el modelo entrenado
    model = joblib.load(os.path.dirname(__file__) + '/best_model.pkl') 

    if model is None:
        raise ValueError("El modelo no se ha cargado correctamente.")
    
    # Crear un DataFrame con los datos de entrada
    input_data = pd.DataFrame([{
        'Mileage': mileage,
        'Year': year,
        'State': state,
        'Model': model,
        'Make': make
    }])
  
    # Realizar la prediccin
    predicted_price = model.predict(input_data)
    
    predicted_price_std = 1000  # Esto debe ser reemplazado por el c�lculo real de la desviaci�n est�ndar

    return predicted_price[0], predicted_price_std


if __name__ == "__main__":
    
    if len(sys.argv) < 6:
        print('Por favor ingresar todos los parametros : Mileage, Year, State, Model, Make')
        
    else:
        mileage = float(sys.argv[1])
        year = int(sys.argv[2])
        state = sys.argv[3]
        model = sys.argv[4]
        make = sys.argv[5]
        
        try:
            price, std_dev = predict_price(mileage, year, state, model, make)
        except Exception as e:
            print(f"Error al predecir: {str(e)}")
            raise
        
        print(f"Precio predecido: ${price:.2f}")
        print(f"Desviacion Standar aprox: ${std_dev:.2f}")
