import 'package:equatable/equatable.dart';

enum RegistrationStatus {
  initial,
  loading,
  editLoaded,
  success,
  deleteSuccess,
  failureConflict,
  failureGeneric,
}

class RegistrationState extends Equatable {
  final bool isAsociado;
  final bool isVoluntario;
  final bool isEditMode;
  final Map<String, dynamic>? memberData;
  final RegistrationStatus status;
  final String? errorMessage;

  const RegistrationState({
    this.isAsociado = false,
    this.isVoluntario = false,
    this.isEditMode = false,
    this.memberData,
    this.status = RegistrationStatus.initial,
    this.errorMessage,
  });

  RegistrationState copyWith({
    bool? isAsociado,
    bool? isVoluntario,
    bool? isEditMode,
    Map<String, dynamic>? memberData,
    RegistrationStatus? status,
    String? errorMessage,
  }) {
    return RegistrationState(
      isAsociado: isAsociado ?? this.isAsociado,
      isVoluntario: isVoluntario ?? this.isVoluntario,
      isEditMode: isEditMode ?? this.isEditMode,
      memberData: memberData ?? this.memberData,
      status: status ?? this.status,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }

  @override
  List<Object?> get props => [
        isAsociado,
        isVoluntario,
        isEditMode,
        memberData,
        status,
        errorMessage,
      ];
}
