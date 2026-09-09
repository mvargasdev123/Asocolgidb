import '../../domain/models/expediente_model.dart';

enum ExpedientesStatus { initial, loading, success, failure }

class ExpedientesState {
  final ExpedientesStatus status;
  final List<ExpedienteModel> expedientes;
  final String? selectedEstadoFilter;
  final String? errorMessage;
  final String? successMessage;

  const ExpedientesState({
    this.status = ExpedientesStatus.initial,
    this.expedientes = const [],
    this.selectedEstadoFilter,
    this.errorMessage,
    this.successMessage,
  });

  ExpedientesState copyWith({
    ExpedientesStatus? status,
    List<ExpedienteModel>? expedientes,
    String? selectedEstadoFilter,
    String? errorMessage,
    String? successMessage,
  }) {
    return ExpedientesState(
      status: status ?? this.status,
      expedientes: expedientes ?? this.expedientes,
      selectedEstadoFilter: selectedEstadoFilter ?? this.selectedEstadoFilter,
      errorMessage: errorMessage,
      successMessage: successMessage,
    );
  }
}
