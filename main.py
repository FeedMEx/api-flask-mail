from flask import Flask, jsonify, request, render_template
from flask_mail import Mail, Message
from flask_cors import CORS
from validators import validar_email
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

CORS(app)

app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"), #correo
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD") #contraseña
))

mail = Mail(app)

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.json['name']
    email = request.json['email']
    message = request.json['message']

    if len(name) < 5:
        return jsonify({'msg': 'Escriba su nombre'})

    elif validar_email(email) == False:
        return jsonify({'msg': 'Correo incorrecto'})
    
    elif len(message) < 8:
        return jsonify({'msg':'Escriba su mensaje'})

    msg = Message('Mensaje desde tu pagina web', 
        sender = app.config['MAIL_USERNAME'],
        recipients = ['freddylo_@hotmail.com']
    )

    msg.html = render_template('email.html', data=[name, email, message])
    try:
        mail.send(msg)
    except ConnectionRefusedError:
        return jsonify({'msg': 'Connection refused error'})
    except:
        return jsonify({'msg': 'Unknown error'})

    return jsonify({'value': True,'msg': 'sent successfully'})


if __name__ == "__main__":
    app.run()