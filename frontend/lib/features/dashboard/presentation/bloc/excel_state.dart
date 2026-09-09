import 'package:equatable/equatable.dart';

enum ExcelStatus { initial, loading, exportSuccess, dryRunSuccess, importSuccess, failure }

class ExcelState extends Equatable {
  final ExcelStatus status;
  final String? successMessage;
  final String? errorMessage;
  final Map<String, dynamic>? dryRunReport;
  final Map<String, dynamic>? importResult;

  const ExcelState({
    this.status = ExcelStatus.initial,
    this.successMessage,
    this.errorMessage,
    this.dryRunReport,
    this.importResult,
  });

  ExcelState copyWith({
    ExcelStatus? status,
    String? successMessage,
    String? errorMessage,
    Map<String, dynamic>? dryRunReport,
    Map<String, dynamic>? importResult,
  }) {
    return ExcelState(
      status: status ?? this.status,
      successMessage: successMessage,
      errorMessage: errorMessage,
      dryRunReport: dryRunReport ?? this.dryRunReport,
      importResult: importResult ?? this.importResult,
    );
  }

  @override
  List<Object?> get props => [
        status,
        successMessage,
        errorMessage,
        dryRunReport,
        importResult,
      ];
}
