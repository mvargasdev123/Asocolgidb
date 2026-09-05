import 'package:dio/dio.dart';
import '../../domain/models/comentario_model.dart';
import '../../domain/repositories/comentario_repository.dart';

class ComentarioRepositoryImpl implements ComentarioRepository {
  final Dio _dio;

  ComentarioRepositoryImpl({required Dio dio}) : _dio = dio;

  @override
  Future<List<ComentarioModel>> getComentarios(int idPersona) async {
    try {
      final response = await _dio.get('/personas/$idPersona/comentarios');
      if (response.statusCode == 200) {
        final list = response.data as List;
        return list.map((e) => ComentarioModel.fromJson(e as Map<String, dynamic>)).toList();
      }
      throw Exception('Error al cargar comentarios');
    } on DioException catch (e) {
      _handleDioError(e);
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  @override
  Future<ComentarioModel> createComentario(
    int idPersona,
    String texto,
    String tipo, {
    DateTime? fechaCreacion,
  }) async {
    try {
      final payload = <String, dynamic>{
        'texto': texto,
        'tipo': tipo,
      };
      if (fechaCreacion != null) {
        payload['fecha_creacion'] = fechaCreacion.toUtc().toIso8601String();
      }

      final response = await _dio.post(
        '/personas/$idPersona/comentarios',
        data: payload,
      );
      if (response.statusCode == 201) {
        return ComentarioModel.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Error al crear comentario');
    } on DioException catch (e) {
      _handleDioError(e);
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  @override
  Future<ComentarioModel> updateComentario(
    int idComentario, {
    String? texto,
    String? tipo,
    DateTime? fechaCreacion,
  }) async {
    try {
      final payload = <String, dynamic>{};
      if (texto != null) payload['texto'] = texto;
      if (tipo != null) payload['tipo'] = tipo;
      if (fechaCreacion != null) {
        payload['fecha_creacion'] = fechaCreacion.toUtc().toIso8601String();
      }

      final response = await _dio.patch(
        '/comentarios/$idComentario',
        data: payload,
      );
      if (response.statusCode == 200) {
        return ComentarioModel.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Error al actualizar comentario');
    } on DioException catch (e) {
      _handleDioError(e);
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  @override
  Future<void> deleteComentario(int idComentario) async {
    try {
      final response = await _dio.delete('/comentarios/$idComentario');
      if (response.statusCode != 204) {
        throw Exception('Error al eliminar comentario');
      }
    } on DioException catch (e) {
      _handleDioError(e);
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  Never _handleDioError(DioException e) {
    if (e.response != null) {
      final data = e.response?.data;
      if (data is Map<String, dynamic> && data.containsKey('detail')) {
        throw Exception(data['detail']);
      }
    }
    throw Exception('Error de red al conectar con el servidor.');
  }
}
