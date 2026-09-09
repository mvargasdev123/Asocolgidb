import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/repositories/metrics_repository.dart';
import 'metrics_event.dart';
import 'metrics_state.dart';

class MetricsBloc extends Bloc<MetricsEvent, MetricsState> {
  final MetricsRepository repository;

  MetricsBloc({required this.repository}) : super(const MetricsState()) {
    on<LoadMetricsEvent>(_onLoadMetrics);
    on<LoadMorososPendientesEvent>(_onLoadMorososPendientes);
  }

  Future<void> _onLoadMetrics(
    LoadMetricsEvent event,
    Emitter<MetricsState> emit,
  ) async {
    emit(state.copyWith(status: MetricsStatus.loading));
    try {
      final summary = await repository.getMetrics();
      emit(state.copyWith(
        status: MetricsStatus.success,
        summary: summary,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: MetricsStatus.failure,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onLoadMorososPendientes(
    LoadMorososPendientesEvent event,
    Emitter<MetricsState> emit,
  ) async {
    try {
      final res = await repository.getAsociadosMorososYPendientes();
      emit(state.copyWith(morososPendientes: res));
    } catch (e) {
      emit(state.copyWith(
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }
}
