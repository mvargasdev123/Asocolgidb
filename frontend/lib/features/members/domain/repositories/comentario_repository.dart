import '../models/comentario_model.dart';

abstract class ComentarioRepository {
  Future<List<ComentarioModel>> getComentarios(int idPersona);
  Future<ComentarioModel> createComentario(
    int idPersona,
    String texto,
    String tipo, {
    DateTime? fechaCreacion,
  });
  Future<ComentarioModel> updateComentario(
    int idComentario, {
    String? texto,
    String? tipo,
    DateTime? fechaCreacion,
  });
  Future<void> deleteComentario(int idComentario);
}
