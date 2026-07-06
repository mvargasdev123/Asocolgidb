import requests

url = "http://127.0.0.1:8000/personas/10"
payload = {
  "nombre": "Victor",
  "correo": "user_patch@example.com",
  "fecha_nacimiento": "2026-07-06",
  "direccion": "string",
  "proteccion_datos": True,
  "tipo_documento": "string",
  "nacionalidad": "string",
  "numero_identificacion": "string_patch",
  "genero": "M",
  "situacion_administrativa": "Regular",
  "madre_soltera": "Sí",
  "violencia_genero": "Sí",
  "tiene_padron": "Sí",
  "autoriza_uso_imagen": True,
  "codigo_postal": "string",
  "ciudad_residencia": "string",
  "unidad_familiar": 0,
  "fecha_padron": "2026-07-06"
}
try:
    response = requests.patch(url, json=payload)
    print(response.status_code)
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
