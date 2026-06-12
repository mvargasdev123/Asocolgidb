import 'dart:ui';
import 'package:flutter/material.dart';

/// ---- CONTENEDOR EFECTO VIDRIO (GLASSMORPHISM) ----
/// ¿Qué es esto?: Es un componente visual moderno que hace que un cuadro se vea
/// como un trozo de vidrio esmerilado (translúcido y un poco borroso por detrás).
/// Le da a nuestra aplicación ese toque "Ultra Premium" digno de portafolio.
class GlassContainer extends StatelessWidget {
  /// Lo que vamos a poner dentro del vidrio (texto, fotos, botones).
  final Widget child;
  
  /// El nivel de desenfoque (borroso) del fondo.
  final double blur;
  
  /// La cantidad de transparencia de la capa blanca (0.0 es invisible, 1.0 es blanco sólido).
  final double opacity;
  
  /// Espaciado interno entre el borde del vidrio y el contenido.
  final EdgeInsetsGeometry padding;

  /// Constructor del vidrio. Te permite ajustar qué tan borroso y transparente es.
  const GlassContainer({
    super.key,
    required this.child,
    this.blur = 10.0,
    this.opacity = 0.15,
    this.padding = const EdgeInsets.all(16.0),
  });

  @override
  Widget build(BuildContext context) {
    // 'ClipRRect' recorta las esquinas de lo que haya adentro para que queden redondas.
    return ClipRRect(
      borderRadius: BorderRadius.circular(20.0), // Esquinas bien redonditas y modernas.
      
      // 'BackdropFilter' es el cristal mágico que aplica filtros visuales a lo que está DEBAJO de él.
      child: BackdropFilter(
        // Aplicamos el filtro de desenfoque (blur) estilo lente de cámara borroso.
        filter: ImageFilter.blur(sigmaX: blur, sigmaY: blur),
        
        // El contenido en sí
        child: Container(
          padding: padding,
          // 'BoxDecoration' nos permite pintar el fondo, bordes y sombras del cuadro.
          decoration: BoxDecoration(
            // Le damos un color blanco muy transparente para que actúe como cristal ahumado.
            color: Colors.white.withValues(alpha: opacity),
            
            // Las esquinas del contenedor deben coincidir con el recorte (20.0).
            borderRadius: BorderRadius.circular(20.0),
            
            // Un truco clave del Glassmorphism: Un borde súper delgadito blanco brillante
            // que simula el filo iluminado del cristal al recibir luz.
            border: Border.all(
              color: Colors.white.withValues(alpha: 0.3),
              width: 1.5,
            ),
          ),
          child: child, // Aquí dentro ponemos el texto, imagen, etc.
        ),
      ),
    );
  }
}
