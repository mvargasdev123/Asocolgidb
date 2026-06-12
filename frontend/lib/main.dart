import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

import 'core/router/app_router.dart';

/// Punto de entrada principal de nuestra aplicación Asocolgi.
/// ¿Qué hace?: Es la primera función que se ejecuta cuando abres la app.
/// ¿Por qué lo hace?: Toda aplicación en Flutter necesita saber por dónde empezar.
/// ¿Para qué sirve?: 'runApp' le dice al teléfono "Dibuja esta aplicación en la pantalla",
/// y 'ProviderScope' es un envoltorio mágico que nos permite compartir datos y estado 
/// (como la lista de personas) por toda la aplicación sin esfuerzo, gracias a Riverpod.
void main() {
  runApp(
    // ProviderScope es necesario para que Riverpod funcione y guarde el "estado" de la app.
    const ProviderScope(
      child: AsocolgiApp(),
    ),
  );
}

/// Esta clase representa la aplicación entera.
/// Es un "StatelessWidget", lo que significa que su configuración básica no cambia
/// una vez que se dibuja (como un póster en la pared).
class AsocolgiApp extends StatelessWidget {
  /// El constructor de la aplicación.
  /// La clave 'Key' es para que Flutter pueda identificar este componente internamente,
  /// 'super.key' simplemente le pasa esa identificación a las entrañas de Flutter.
  const AsocolgiApp({super.key});

  /// El método 'build' es el corazón de cualquier Widget (componente de pantalla).
  /// ¿Qué hace?: Describe cómo se verá la interfaz de usuario en la pantalla.
  /// Siempre que Flutter necesita pintar algo, llama a este método.
  @override
  Widget build(BuildContext context) {
    // MaterialApp.router se utiliza para manejar navegación compleja con GoRouter.
    return MaterialApp.router(
      // Título interno de la app (útil para el sistema operativo)
      title: 'Asocolgi',
      
      // Aquí quitamos la cintita de "Debug" (Depuración) que aparece en la esquina superior derecha
      // cuando estamos programando, para que luzca más profesional.
      debugShowCheckedModeBanner: false,

      // Aplicamos la configuración de GoRouter
      routerConfig: appRouter,

      // Configuramos el "Tema" visual (colores, fuentes tipográficas).
      // ¿Por qué aquí?: Para que toda la app comparta el mismo estilo de forma automática.
      theme: ThemeData(
        // Indicamos que queremos usar las últimas versiones de los componentes visuales.
        useMaterial3: true,
        
        // Configuramos la paleta de colores. 
        // Usamos un Azul Profundo como base, que transmite confianza y seriedad (ideal para la ONG).
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF0F4C75), // Azul oscuro institucional
          background: const Color(0xFFF9F9F9), // Un gris ultra claro casi blanco para el fondo
        ),
        
        // Usamos la fuente 'Inter' para toda la app.
        // ¿Para qué?: 'Inter' es moderna, muy limpia y fácil de leer en cualquier pantalla.
        textTheme: GoogleFonts.interTextTheme(
          Theme.of(context).textTheme,
        ),
      ),
      
      // La navegación inicial ahora la maneja GoRouter en app_router.dart
    );
  }
}
