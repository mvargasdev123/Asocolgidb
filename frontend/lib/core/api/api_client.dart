import 'package:dio/dio.dart';

/// Este archivo configura nuestro "Cartero" virtual que llevará y traerá los
/// mensajes entre nuestra aplicación y el servidor de Python (FastAPI).
/// Usamos un paquete llamado 'Dio', que es como un cartero en bicicleta súper rápido
/// y con muchas herramientas útiles para hacer peticiones por Internet.

/// Clase que envuelve y configura a nuestro cartero (Dio).
class ApiClient {
  /// Esta es la bicicleta del cartero. 'Dio' es la herramienta principal que usaremos.
  final Dio dio;

  /// Constructor de nuestro cartero.
  ApiClient() : dio = Dio(
    // Aquí configuramos las reglas base para nuestro cartero.
    BaseOptions(
      // Cambiamos 127.0.0.1 por localhost. A veces Chrome web tiene conflictos 
      // resolviendo IPs estáticas locales dependiendo de si usa IPv4 o IPv6.
      baseUrl: 'http://localhost:8000',
      
      // En Flutter Web, los timeouts explícitos de conexión a veces causan bugs
      // o abortan prematuramente la petición de XMLHttpRequest. Los desactivamos para web.
      
      // Especificamos que siempre vamos a enviar y recibir información en formato JSON.
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    )
  );
}
