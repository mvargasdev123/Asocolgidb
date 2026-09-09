import 'package:dio/dio.dart';
import '../../../../core/network/dio_client.dart';
import '../../domain/models/expediente_model.dart';
import '../../domain/repositories/expediente_repository.dart';

class ExpedienteRepositoryImpl implements ExpedienteRepository {
  final DioClient _dioClient;

  ExpedienteRepositoryImpl(this._dioClient);

  @override
  Future<List<ExpedienteModel>> getExpedientes({String? estado}) async {
    final queryParams = <String, dynamic>{};
    if (estado != null && estado.isNotEmpty) {
      queryParams['estado'] = estado;
    }
    final response = await _dioClient.dio.get(
      '/expedientes/',
      queryParameters: queryParams,
    );
    final list = response.data as List<dynamic>;
    return list.map((json) => ExpedienteModel.fromJson(json as Map<String, dynamic>)).toList();
  }

  @override
  Future<List<ExpedienteModel>> getExpedientesPersona(int idPersona) async {
    final response = await _dioClient.dio.get('/personas/$idPersona/expedientes');
    final list = response.data as List<dynamic>;
    return list.map((json) => ExpedienteModel.fromJson(json as Map<String, dynamic>)).toList();
  }

  @override
  Future<ExpedienteModel> getExpedienteById(int idExpediente) async {
    final response = await _dioClient.dio.get('/expedientes/$idExpediente');
    return ExpedienteModel.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<ExpedienteModel> createExpediente({
    required int idPersona,
    required String tipoTramite,
    required String fechaPresentacion,
    String? numeroExpedienteAsignado,
    String? representanteLegal,
    String? consultorioJuridico,
    String aporteSocial = 'Sí',
    bool solicitanteExtranjeria = false,
    bool antecedentesTraducidosYApostillados = false,
    String? fechaResolucion,
  }) async {
    try {
      final payload = <String, dynamic>{
        'tipo_tramite': tipoTramite,
        'fecha_presentacion': fechaPresentacion,
        'aporte_social': aporteSocial,
        'solicitante_extranjeria': solicitanteExtranjeria,
        'antecedentes_traducidos_y_apostillados': antecedentesTraducidosYApostillados,
      };

      if (numeroExpedienteAsignado != null && numeroExpedienteAsignado.isNotEmpty) {
        payload['numero_expediente_asignado'] = numeroExpedienteAsignado;
      }
      if (representanteLegal != null && representanteLegal.isNotEmpty) {
        payload['representante_legal'] = representanteLegal;
      }
      if (consultorioJuridico != null && consultorioJuridico.isNotEmpty) {
        payload['consultorio_juridico'] = consultorioJuridico;
      }
      if (fechaResolucion != null && fechaResolucion.isNotEmpty) {
        payload['fecha_resolucion'] = fechaResolucion;
      }

      final response = await _dioClient.dio.post(
        '/personas/$idPersona/expedientes',
        data: payload,
      );
      return ExpedienteModel.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      final msg = e.response?.data?['detail'] ?? e.message ?? 'Error al crear expediente';
      throw Exception(msg);
    }
  }

  @override
  Future<ExpedienteModel> updateExpedienteStatus({
    required int idExpediente,
    required String estado,
  }) async {
    try {
      final response = await _dioClient.dio.patch(
        '/expedientes/$idExpediente',
        data: {'estado': estado},
      );
      return ExpedienteModel.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      final msg = e.response?.data?['detail'] ?? e.message ?? 'Error al actualizar estado del expediente';
      throw Exception(msg);
    }
  }

  @override
  Future<void> deleteExpediente(int idExpediente) async {
    await _dioClient.dio.delete('/expedientes/$idExpediente');
  }
}
