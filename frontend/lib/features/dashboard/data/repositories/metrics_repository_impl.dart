import '../../../../core/network/dio_client.dart';
import '../../domain/models/metrics_model.dart';
import '../../domain/repositories/metrics_repository.dart';

class MetricsRepositoryImpl implements MetricsRepository {
  final DioClient _dioClient;

  MetricsRepositoryImpl(this._dioClient);

  @override
  Future<MetricsSummaryModel> getMetrics() async {
    final response = await _dioClient.dio.get('/metrics');
    return MetricsSummaryModel.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<AsociadosMorososPendientesModel> getAsociadosMorososYPendientes() async {
    final response = await _dioClient.dio.get('/metrics/asociados-morosos-pendientes');
    return AsociadosMorososPendientesModel.fromJson(response.data as Map<String, dynamic>);
  }
}
