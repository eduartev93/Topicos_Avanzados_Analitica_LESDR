
import os
from flask import Flask, request
from flask_restx import Api, Resource, fields
import Model_Dev

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Predecir el Precio de Coches API - POST',
    description='API para predecir el precio de coches')

ns = api.namespace('predict', description='Precio regresión')

# Definir el modelo del cuerpo de la solicitud
input_model = api.model('InputModel', {
    'Mileage': fields.Float(required=True, description='Millas del auto'),
    'Year': fields.Integer(required=True, description='Año del auto'),
    'State': fields.String(required=True, description='Estado donde esta registrado el auto'),
    'Model': fields.String(required=True, description='Modelo del auto'),
    'Make': fields.String(required=True, description='Marca del auto')
})

resource_fields = api.model('Resource', {
    'predicted_price': fields.Float,
    'predicted_price_std': fields.Float,
})

@ns.route('/')
class PredictPrice(Resource):
    @api.expect(input_model)
    @api.marshal_with(resource_fields)
    def post(self):
        # Obtener los datos del cuerpo de la solicitud
        data = request.json
        
        # Verificar que todos los campos necesarios estén presentes
        if not all(key in data for key in ('Mileage', 'Year', 'State', 'Model', 'Make')):
            return {"message": "Missing fields in request body"}, 400

        # Extraer los valores
        mileage = data['Mileage']
        year = data['Year']
        state = data['State']
        model_name = data['Model']
        make = data['Make']
     
        # Realizar la predicción
        predicted_price,predicted_price_std = predict_price(mileage=mileage, year=year, state=state, model=model_name, make=make)

        return {
            'predicted_price': predicted_price,
            'predicted_price_std': predicted_price_std
        },200
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
