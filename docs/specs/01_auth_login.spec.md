# Especificación: 01_auth_login

## 1. Contexto y Usuario
El módulo de Autenticación permite a los gestores de la fundación Asocolgi acceder al panel de administración de la base de datos.
**Nota Arquitectónica:** Se permitirá el acceso concurrente desde diferentes dispositivos usando la misma cuenta dado que el equipo administrativo comparte credenciales de gestión. Las medidas de seguridad anti-fuerza bruta se basarán estrictamente en la dirección IP del cliente, no en la cuenta.

## 2. Historia de Usuario
* **Como** gestor de la base de datos,
* **Quiero** iniciar sesión de forma segura ingresando mi correo y contraseña, y poder ver la contraseña (toggle) para asegurar que la escribí bien.
* **Para** poder acceder a la gestión principal de usuarios.
* **Además**, necesito recuperar mi contraseña si la olvido mediante un botón que envíe un correo automáticamente, y que el sistema se proteja de ataques bloqueando IPs progresivamente tras intentos fallidos, notificando al correo oficial.

## 3. Requisitos Funcionales (E.A.R.S)

### 3.1 Interfaz y Flujo Básico (Ubiquitous)
* **El sistema deberá** renderizar la pantalla de Login manteniendo la estética y diseño exacto (glassmorphism, logos, fondos) de la versión anterior.
* **El sistema deberá** contener campos de entrada para Correo Electrónico y Contraseña, un botón de "Ver Contraseña" (ojo/toggle), un botón de "¿Olvidaste tu contraseña?" y un botón de "Ingresar".

### 3.2 Proceso de Autenticación (Event-driven)
* **Cuando** el usuario envíe el formulario con credenciales válidas, **el sistema deberá** generar un token JWT de sesión.
* **Cuando** el token JWT sea validado exitosamente, **el sistema deberá** redirigir al usuario al apartado principal del Dashboard de Gestión.

### 3.3 Recuperación de Contraseña (Event-driven)
* **Cuando** el usuario presione el botón de recuperar contraseña, **el sistema deberá** omitir pedir una dirección de correo y enviar directamente un token temporal seguro por email a la cuenta predefinida: `asocolgibasededatos@gmail.com`.

### 3.4 Seguridad y Bloqueo por IP (Unwanted Behavior / State-driven)
* **Si** el usuario envía una contraseña incorrecta, **entonces el sistema deberá** mostrar un mensaje de error genérico ("Credenciales incorrectas").
* **Si** una Dirección IP falla 3 intentos consecutivos, **entonces el sistema deberá** bloquear los intentos de inicio de sesión de esa IP por 15 segundos y enviar una alerta de seguridad al correo administrador.
* **Si** esa IP falla nuevamente, **entonces el sistema deberá** bloquear la IP por 30 segundos y enviar otra alerta.
* **Si** esa IP falla nuevamente tras el bloqueo de 30 segundos, **entonces el sistema deberá** bloquear la IP por 5 minutos y enviar alerta.
* **Si** esa IP falla nuevamente tras el bloqueo de 5 minutos, **entonces el sistema deberá** bloquear la IP por 10 minutos de forma recurrente (cualquier fallo posterior resultará en otro bloqueo de 10 minutos).
* **Cuando** pasen 24 horas desde el último bloqueo de una IP, **el sistema deberá** resetear el historial de fallos de esa IP a cero.

## 4. Contratos y Tipos (Pydantic / Dart Classes)

**Request (Frontend -> Backend):**
```json
{
  "email": "asocolgibasededatos@gmail.com",
  "password": "mi_password_secreto"
}
```

**Response Éxito (Backend -> Frontend):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5c...",
  "token_type": "bearer"
}
```

## 5. Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Bloqueo progresivo por IP
  Given una IP que ha fallado la contraseña 5 veces seguidas (alcanzando el bloqueo de 5 minutos)
  When la IP intenta iniciar sesión con una contraseña incorrecta nuevamente
  Then el sistema rechaza la petición y bloquea la IP por 10 minutos
  And el sistema envía un correo de alerta a asocolgibasededatos@gmail.com
```
