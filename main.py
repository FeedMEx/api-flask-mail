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
    name = " ".join(name.split())

    email = request.json['email'].strip()

    message = request.json['message']
    message = " ".join(message.split())

    if len(name) < 8:
        return jsonify({'value': False, 'msg': 'err_name'})

    elif validar_email(email) == False:
        return jsonify({'value': False, 'msg': 'err_email'})
    
    elif len(message) < 64 or len(message) > 512:
        return jsonify({'value': False, 'msg':'err_message'})

    msg = Message('¡MENSAJE DESDE TU PÁGINA WEB!', 
        sender = app.config['MAIL_USERNAME'],
        recipients = [os.getenv("RECIPIENT")] #correo destinatario
    )

    msg.html = render_template('email.html', data=[name, email, message])
    try:
        mail.send(msg)
    except ConnectionRefusedError:
        return jsonify({'value': False, 'msg': 'Connection refused error'}), 500
    except:
        return jsonify({'value': False, 'msg': 'Unknown error'}), 500

    return jsonify({'value': True, 'msg': 'send successfully'}), 200


if __name__ == "__main__":
    app.run()