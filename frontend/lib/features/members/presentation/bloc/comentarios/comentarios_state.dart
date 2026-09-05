import 'package:equatable/equatable.dart';
import '../../../domain/models/comentario_model.dart';

enum ComentariosStatus { initial, loading, loaded, failure }

class ComentariosState extends Equatable {
  final ComentariosStatus status;
  final List<ComentarioModel> comentarios;
  final String? errorMessage;
  final bool isSubmitting;

  const ComentariosState({
    this.status = ComentariosStatus.initial,
    this.comentarios = const [],
    this.errorMessage,
    this.isSubmitting = false,
  });

  ComentariosState copyWith({
    ComentariosStatus? status,
    List<ComentarioModel>? comentarios,
    String? errorMessage,
    bool? isSubmitting,
  }) {
    return ComentariosState(
      status: status ?? this.status,
      comentarios: comentarios ?? this.comentarios,
      errorMessage: errorMessage,
      isSubmitting: isSubmitting ?? this.isSubmitting,
    );
  }

  @override
  List<Object?> get props => [status, comentarios, errorMessage, isSubmitting];
}
