import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/utils/file_download_helper.dart';
import '../../domain/repositories/excel_repository.dart';
import 'excel_event.dart';
import 'excel_state.dart';

class ExcelBloc extends Bloc<ExcelEvent, ExcelState> {
  final ExcelRepository _repository;

  ExcelBloc(this._repository) : super(const ExcelState()) {
    on<ExportarExcelEvent>(_onExportarExcel);
    on<DescargarExcelDirectoEvent>(_onDescargarExcelDirecto);
    on<AnalizarImportacionEvent>(_onAnalizarImportacion);
    on<ConfirmarImportacionEvent>(_onConfirmarImportacion);
    on<ResetExcelStateEvent>(_onResetExcelState);
  }

  Future<void> _onExportarExcel(
      ExportarExcelEvent event, Emitter<ExcelState> emit) async {
    emit(state.copyWith(status: ExcelStatus.loading));
    try {
      final msg = await _repository.exportarAEmail(event.tipoExportacion);
      emit(state.copyWith(
        status: ExcelStatus.exportSuccess,
        successMessage: msg,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: ExcelStatus.failure,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onDescargarExcelDirecto(
      DescargarExcelDirectoEvent event, Emitter<ExcelState> emit) async {
    emit(state.copyWith(status: ExcelStatus.loading));
    try {
      final bytes = await _repository.descargarDirecto(event.tipoExportacion);
      final filename = 'asocolgi_${event.tipoExportacion}_${DateTime.now().millisecondsSinceEpoch}.xlsx';
      downloadFileBytes(bytes, filename);
      emit(state.copyWith(
        status: ExcelStatus.exportSuccess,
        successMessage: 'Archivo Excel descargado con éxito ($filename)',
      ));
    } catch (e) {
      emit(state.copyWith(
        status: ExcelStatus.failure,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onAnalizarImportacion(
      AnalizarImportacionEvent event, Emitter<ExcelState> emit) async {
    emit(state.copyWith(status: ExcelStatus.loading));
    try {
      final report = await _repository.analizarImportacion(event.bytes, event.filename);
      emit(state.copyWith(
        status: ExcelStatus.dryRunSuccess,
        dryRunReport: report,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: ExcelStatus.failure,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onConfirmarImportacion(
      ConfirmarImportacionEvent event, Emitter<ExcelState> emit) async {
    emit(state.copyWith(status: ExcelStatus.loading));
    try {
      final res = await _repository.confirmarImportacion(
          event.bytes, event.filename, event.decisiones);
      final msg = res['mensaje'] as String? ?? 'Importación realizada con éxito.';
      emit(state.copyWith(
        status: ExcelStatus.importSuccess,
        successMessage: msg,
        importResult: res,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: ExcelStatus.failure,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  void _onResetExcelState(
      ResetExcelStateEvent event, Emitter<ExcelState> emit) {
    emit(const ExcelState());
  }
}
