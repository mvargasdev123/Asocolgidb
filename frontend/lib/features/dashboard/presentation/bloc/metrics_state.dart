import '../../domain/models/metrics_model.dart';

enum MetricsStatus { initial, loading, success, failure }

class MetricsState {
  final MetricsStatus status;
  final MetricsSummaryModel? summary;
  final AsociadosMorososPendientesModel? morososPendientes;
  final String? errorMessage;

  const MetricsState({
    this.status = MetricsStatus.initial,
    this.summary,
    this.morososPendientes,
    this.errorMessage,
  });

  MetricsState copyWith({
    MetricsStatus? status,
    MetricsSummaryModel? summary,
    AsociadosMorososPendientesModel? morososPendientes,
    String? errorMessage,
  }) {
    return MetricsState(
      status: status ?? this.status,
      summary: summary ?? this.summary,
      morososPendientes: morososPendientes ?? this.morososPendientes,
      errorMessage: errorMessage,
    );
  }
}
