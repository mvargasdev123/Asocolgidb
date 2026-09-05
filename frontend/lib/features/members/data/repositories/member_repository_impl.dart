import 'dart:convert';
import 'package:dio/dio.dart';
import '../../domain/models/member_registration_request.dart';
import '../../domain/repositories/member_repository.dart';

class MemberRepositoryImpl implements MemberRepository {
  final Dio _dio;

  MemberRepositoryImpl({required Dio dio}) : _dio = dio;

  @override
  Future<void> registerMember(MemberRegistrationRequest request) async {
    final payload = request.toJson();

    try {
      final response = await _dio.post('/personas/', data: payload);
      if (response.statusCode != 200 && response.statusCode != 201) {
        throw Exception('Error al registrar usuario');
      }
    } on DioException catch (e) {
      _handleDioError(e);
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  @override
  Future<List<Map<String, dynamic>>> getMembers({int? lastId, int limit = 10}) async {
    try {
      final queryParams = {'limit': limit};
      if (lastId != null) queryParams['last_id'] = lastId;

      final response = await _dio.get('/personas/', queryParameters: queryParams);
      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(response.data);
      }
      throw Exception('Error al cargar la lista de miembros');
    } on DioException catch (e) {
      _handleDioError(e);
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  @override
  Future<Map<String, dynamic>> getMemberDetails(int id) async {
    try {
      final response = await _dio.get('/personas/$id');
      if (response.statusCode == 200) {
        return Map<String, dynamic>.from(response.data);
      }
      throw Exception('Error al cargar el detalle del miembro');
    } on DioException catch (e) {
      _handleDioError(e);
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  @override
  Future<void> updateMember(int id, Map<String, dynamic> data) async {
    try {
      final response = await _dio.patch('/personas/$id', data: data);
      if (response.statusCode != 200) {
        throw Exception('Error al actualizar el miembro');
      }
    } on DioException catch (e) {
      _handleDioError(e);
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  @override
  Future<void> deleteMember(int id) async {
    try {
      final response = await _dio.delete('/personas/$id');
      if (response.statusCode != 204) {
        throw Exception('Error al eliminar el miembro');
      }
    } on DioException catch (e) {
      _handleDioError(e);
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  Never _handleDioError(DioException e) {
    if (e.response != null) {
      if (e.response?.statusCode == 409) {
        throw Exception('Este Número de Documento ya está asignado a otro usuario');
      }
      final data = e.response?.data;
      if (data is Map<String, dynamic> && data.containsKey('detail')) {
        throw Exception(data['detail']);
      }
    }
    throw Exception('Error de red al conectar con el servidor.');
  }
}
