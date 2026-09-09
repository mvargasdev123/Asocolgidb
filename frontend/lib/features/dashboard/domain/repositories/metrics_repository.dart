import '../models/metrics_model.dart';

abstract class MetricsRepository {
  Future<MetricsSummaryModel> getMetrics();
  Future<AsociadosMorososPendientesModel> getAsociadosMorososYPendientes();
}
