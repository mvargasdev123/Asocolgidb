import 'package:equatable/equatable.dart';

abstract class ExcelEvent extends Equatable {
  const ExcelEvent();

  @override
  List<Object?> get props => [];
}

class ExportarExcelEvent extends ExcelEvent {
  final String tipoExportacion;

  const ExportarExcelEvent(this.tipoExportacion);

  @override
  List<Object?> get props => [tipoExportacion];
}

class DescargarExcelDirectoEvent extends ExcelEvent {
  final String tipoExportacion;

  const DescargarExcelDirectoEvent(this.tipoExportacion);

  @override
  List<Object?> get props => [tipoExportacion];
}

class AnalizarImportacionEvent extends ExcelEvent {
  final List<int> bytes;
  final String filename;

  const AnalizarImportacionEvent({required this.bytes, required this.filename});

  @override
  List<Object?> get props => [bytes, filename];
}

class ConfirmarImportacionEvent extends ExcelEvent {
  final List<int> bytes;
  final String filename;
  final Map<String, String> decisiones;

  const ConfirmarImportacionEvent({
    required this.bytes,
    required this.filename,
    required this.decisiones,
  });

  @override
  List<Object?> get props => [bytes, filename, decisiones];
}

class ResetExcelStateEvent extends ExcelEvent {}
