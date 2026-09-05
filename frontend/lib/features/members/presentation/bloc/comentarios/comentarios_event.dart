import 'package:equatable/equatable.dart';

abstract class ComentariosEvent extends Equatable {
  const ComentariosEvent();

  @override
  List<Object?> get props => [];
}

class LoadComentarios extends ComentariosEvent {
  final int idPersona;

  const LoadComentarios(this.idPersona);

  @override
  List<Object?> get props => [idPersona];
}

class AddComentario extends ComentariosEvent {
  final int idPersona;
  final String texto;
  final String tipo;
  final DateTime? fechaCreacion;

  const AddComentario({
    required this.idPersona,
    required this.texto,
    required this.tipo,
    this.fechaCreacion,
  });

  @override
  List<Object?> get props => [idPersona, texto, tipo, fechaCreacion];
}

class UpdateComentario extends ComentariosEvent {
  final int idComentario;
  final int idPersona;
  final String? texto;
  final String? tipo;
  final DateTime? fechaCreacion;

  const UpdateComentario({
    required this.idComentario,
    required this.idPersona,
    this.texto,
    this.tipo,
    this.fechaCreacion,
  });

  @override
  List<Object?> get props => [idComentario, idPersona, texto, tipo, fechaCreacion];
}

class DeleteComentario extends ComentariosEvent {
  final int idComentario;
  final int idPersona;

  const DeleteComentario({
    required this.idComentario,
    required this.idPersona,
  });

  @override
  List<Object?> get props => [idComentario, idPersona];
}
