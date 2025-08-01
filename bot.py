from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# Guardamos estado del usuario (clave: número)
usuarios = {}

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    data = request.form
    numero = data.get("From")
    mensaje = data.get("Body", "").strip().lower()

    # Estado actual
    estado = usuarios.get(numero, {}).get("estado", "inicio")

    if estado == "inicio":
        respuesta = (
            "👋 ¡Hola! Soy Nano, tu asistente virtual de Ingeniería Mendivil.\n"
            "¿En qué te puedo ayudar?\n"
            "1️⃣ Urgencia\n2️⃣ Presupuesto\n3️⃣ Información\n4️⃣ Otra consulta"
        )
        usuarios[numero] = {"estado": "esperando_opcion"}

    elif estado == "esperando_opcion":
        usuarios[numero]["opcion"] = mensaje
        respuesta = "👉 ¿Qué tipo de servicio necesitás?\n- Electricidad\n- Gas"
        usuarios[numero]["estado"] = "esperando_servicio"

    elif estado == "esperando_servicio":
        usuarios[numero]["servicio"] = mensaje
        respuesta = "📝 Por favor, decime tu nombre y apellido:"
        usuarios[numero]["estado"] = "esperando_nombre"

    elif estado == "esperando_nombre":
        usuarios[numero]["nombre"] = mensaje
        respuesta = "🏠 Ahora indicame la dirección del domicilio:"
        usuarios[numero]["estado"] = "esperando_direccion"

    elif estado == "esperando_direccion":
        usuarios[numero]["direccion"] = mensaje
        respuesta = "✍️ Por último, contame brevemente tu consulta:"
        usuarios[numero]["estado"] = "esperando_descripcion"

    elif estado == "esperando_descripcion":
        usuarios[numero]["descripcion"] = mensaje
        respuesta = "✅ ¡Gracias! Hemos recibido tu consulta. Te contactaremos a la brevedad."
        print("🚨 NUEVA CONSULTA:")
        print(usuarios[numero])
        usuarios[numero]["estado"] = "finalizado"

    else:
        respuesta = "¿Querés empezar otra vez? Escribí *Hola* para reiniciar."
        usuarios[numero]["estado"] = "inicio"

    # Respondemos a Twilio
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{respuesta}</Message>
</Response>"""

if __name__ == "__main__":
   app.run(host='0.0.0.0')
