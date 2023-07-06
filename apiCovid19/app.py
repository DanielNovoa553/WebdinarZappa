from flask import Flask, jsonify, request
import requests
import datetime
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GHgsfvxhwdcXFty"#&/()=)'


def generate_token():
    time = datetime.datetime.utcnow()
    plus_time = datetime.timedelta(minutes=5)
    expiration_time_mexico = datetime.datetime.now() + plus_time
    print(f"plus_time: {plus_time}")
    expiration_time = time + plus_time
    print(f"expiration_time: {expiration_time_mexico}")
    payload = {'exp': expiration_time, 'iat': datetime.datetime.utcnow()}
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token, expiration_time_mexico


def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired.'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token.'}


@app.route('/login')
def login():
    token = generate_token()
    expiration_time_mexico = token[1].strftime("%d-%m-%Y %H:%M:%S")
    return jsonify({'token': token[0],
                    'message': 'Token generated successfully.',
                    'expiration_time': expiration_time_mexico})


@app.route('/get_covid_data')
def get_covid_data():
    global status
    try:
        token = request.args.get('token')
        if not token:
            return jsonify({'error': 'Token is missing.'})

        payload = verify_token(token)
        if 'error' in payload:
            return jsonify(payload)

        api_url = 'https://disease.sh/v3/covid-19/all'
        response = requests.get(api_url)
        data = response.json()
        print(data)

        if 'cases' not in data:
            return jsonify({'error': 'Data structure does not match expectations.'})

        # Create a dictionary with the data you want to display
        covid_data = {
            'casos': '{:,}'.format(data['cases']),
            'recuperados':'{:,}'.format(data['recovered']),
            'recuperadosHoy': '{:,}'.format(data['todayRecovered']),
            'activos': '{:,}'.format(data['active']),
            'fallecidos': '{:,}'.format(data['deaths']),
            'casosHoy': '{:,}'.format(data['todayCases']),
            'fallecidosHoy': '{:,}'.format(data['todayDeaths']),
            'casosActivos': '{:,}'.format(data['active']),
            'casosCríticos': '{:,}'.format(data['critical']),
            'casosPorMillón': '{:,}'.format(data['casesPerOneMillion']),
            'fallecidosPorMillón': '{:,}'.format(data['deathsPerOneMillion']),
            'totalPruebasPorMillón': '{:,}'.format(data['testsPerOneMillion']),
            'población': '{:,}'.format(data['population']),
            'activosPorMillón': '{:,}'.format(data['activePerOneMillion']),
            'recuperadosPorMillón': '{:,}'.format(data['recoveredPerOneMillion']),
            'críticosPorMillón': '{:,}'.format(data['criticalPerOneMillion']),
            'totalPruebas': '{:,}'.format(data['tests']),
            'paisesAfectados': '{:,}'.format(data['affectedCountries']),
        }
        status = True
        return jsonify({'Resume_Covid_19': covid_data,
                        'status': status,
                        'message': 'Resume data Covid 19 obtained successfully.'})

    except Exception as e:
        return jsonify({'Error to get Covid 19 data': str(e),
                        'status': False})


if __name__ == '__main__':
    app.run()
