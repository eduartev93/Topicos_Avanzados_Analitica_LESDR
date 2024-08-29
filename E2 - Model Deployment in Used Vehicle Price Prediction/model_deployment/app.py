
from flask import Flask
from flask_restx import Api, Resource, fields
from model_deployment.Model_Dev import predict_price # Importar la función predict_price desde model_dev

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Predecir el Precio de Coches API - GET',
    description='API para predecir el precio de coches'
)

ns = api.namespace('predict', description='Precio regresión')

# Definir los argumentos esperados
parser = api.parser()

parser.add_argument(
    'Mileage',
    type=float,
    required=True,
    help='Millas del auto',
    location='args')

parser.add_argument(
    'Year',
    type=int,
    required=True,
    help='Año del auto',
    location='args')

parser.add_argument(
    'State',
    type=str,
    required=True,
    help='Estado donde está registrado el auto',
    location='args')

parser.add_argument(
    'Model',
    type=str,
    required=True,
    help='Modelo del auto',
    location='args')

parser.add_argument(
    'Make',
    type=str,
    required=True,
    help='Marca del auto',
    location='args')

resource_fields = api.model('Resource', {
    'predicted_price': fields.Float,
    'predicted_price_std': fields.Float,
})

@ns.route('/')
class PredictPrice(Resource):
    @api.expect(parser)
    @api.marshal_with(resource_fields)
    def get(self):
        # Obtener los parámetros de la URL
        args = parser.parse_args()
        mileage = args['Mileage']
        year = args['Year']
        state = args['State']
        model_name = args['Model']
        make = args['Make']

        # Realizar la predicción
        predicted_price, predicted_price_std = predict_price(
            mileage=mileage, 
            year=year, 
            state=state, 
            model=model_name,  # Usar model_name en lugar de model
            make=make
        )

        return {
            "predicted_price": predicted_price,
            'predicted_price_std': predicted_price_std
        }, 200

if __name__ == '__main__':
    app.run(debug=True)
