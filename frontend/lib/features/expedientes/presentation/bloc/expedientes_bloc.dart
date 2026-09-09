import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/repositories/expediente_repository.dart';
import 'expedientes_event.dart';
import 'expedientes_state.dart';

class ExpedientesBloc extends Bloc<ExpedientesEvent, ExpedientesState> {
  final ExpedienteRepository repository;

  ExpedientesBloc({required this.repository}) : super(const ExpedientesState()) {
    on<LoadExpedientes>(_onLoadExpedientes);
    on<CreateExpedienteEvent>(_onCreateExpediente);
    on<UpdateExpedienteStatusEvent>(_onUpdateExpedienteStatus);
  }

  Future<void> _onLoadExpedientes(
    LoadExpedientes event,
    Emitter<ExpedientesState> emit,
  ) async {
    emit(state.copyWith(status: ExpedientesStatus.loading, selectedEstadoFilter: event.estado));
    try {
      final list = await repository.getExpedientes(estado: event.estado);
      emit(state.copyWith(
        status: ExpedientesStatus.success,
        expedientes: list,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: ExpedientesStatus.failure,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onCreateExpediente(
    CreateExpedienteEvent event,
    Emitter<ExpedientesState> emit,
  ) async {
    try {
      await repository.createExpediente(
        idPersona: event.idPersona,
        tipoTramite: event.tipoTramite,
        fechaPresentacion: event.fechaPresentacion,
      );
      emit(state.copyWith(successMessage: 'Expediente creado con éxito'));
      add(LoadExpedientes(estado: state.selectedEstadoFilter));
    } catch (e) {
      emit(state.copyWith(
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onUpdateExpedienteStatus(
    UpdateExpedienteStatusEvent event,
    Emitter<ExpedientesState> emit,
  ) async {
    try {
      await repository.updateExpedienteStatus(
        idExpediente: event.idExpediente,
        estado: event.nuevoEstado,
      );
      emit(state.copyWith(successMessage: 'Estado de expediente actualizado'));
      add(LoadExpedientes(estado: state.selectedEstadoFilter));
    } catch (e) {
      emit(state.copyWith(
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }
}
