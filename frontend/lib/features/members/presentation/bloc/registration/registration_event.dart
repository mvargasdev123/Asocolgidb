import 'package:equatable/equatable.dart';
import '../../../domain/models/member_registration_request.dart';

abstract class RegistrationEvent extends Equatable {
  const RegistrationEvent();

  @override
  List<Object?> get props => [];
}

class ToggleAsociado extends RegistrationEvent {
  final bool isAsociado;
  const ToggleAsociado(this.isAsociado);

  @override
  List<Object?> get props => [isAsociado];
}

class ToggleVoluntario extends RegistrationEvent {
  final bool isVoluntario;
  const ToggleVoluntario(this.isVoluntario);

  @override
  List<Object?> get props => [isVoluntario];
}

class SubmitRegistration extends RegistrationEvent {
  final MemberRegistrationRequest request;

  const SubmitRegistration(this.request);

  @override
  List<Object?> get props => [request];
}

class LoadMemberForEdit extends RegistrationEvent {
  final int memberId;
  const LoadMemberForEdit(this.memberId);

  @override
  List<Object?> get props => [memberId];
}

class UpdateRegistration extends RegistrationEvent {
  final int memberId;
  final MemberRegistrationRequest request;

  const UpdateRegistration(this.memberId, this.request);

  @override
  List<Object?> get props => [memberId, request];
}

class DeleteMemberRequested extends RegistrationEvent {
  final int memberId;
  const DeleteMemberRequested(this.memberId);

  @override
  List<Object?> get props => [memberId];
}

class ResetRegistration extends RegistrationEvent {}
