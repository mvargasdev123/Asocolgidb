import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../domain/repositories/member_repository.dart';
import 'registration_event.dart';
import 'registration_state.dart';

class RegistrationBloc extends Bloc<RegistrationEvent, RegistrationState> {
  final MemberRepository _repository;

  RegistrationBloc({required MemberRepository repository})
    : _repository = repository,
      super(const RegistrationState()) {
    on<ToggleAsociado>(_onToggleAsociado);
    on<ToggleVoluntario>(_onToggleVoluntario);
    on<SubmitRegistration>(_onSubmitRegistration);
    on<LoadMemberForEdit>(_onLoadMemberForEdit);
    on<UpdateRegistration>(_onUpdateRegistration);
    on<DeleteMemberRequested>(_onDeleteMemberRequested);
    on<ResetRegistration>(_onResetRegistration);
  }

  void _onToggleAsociado(
    ToggleAsociado event,
    Emitter<RegistrationState> emit,
  ) {
    emit(state.copyWith(isAsociado: event.isAsociado));
  }

  void _onToggleVoluntario(
    ToggleVoluntario event,
    Emitter<RegistrationState> emit,
  ) {
    emit(state.copyWith(isVoluntario: event.isVoluntario));
  }

  void _onResetRegistration(
    ResetRegistration event,
    Emitter<RegistrationState> emit,
  ) {
    emit(const RegistrationState());
  }

  Future<void> _onLoadMemberForEdit(
    LoadMemberForEdit event,
    Emitter<RegistrationState> emit,
  ) async {
    emit(state.copyWith(status: RegistrationStatus.loading, errorMessage: null));
    try {
      final data = await _repository.getMemberDetails(event.memberId);
      final bool esAsociado = data['es_asociado'] == true;
      final bool esVoluntario = data['es_voluntario'] == true;
      emit(state.copyWith(
        isEditMode: true,
        isAsociado: esAsociado,
        isVoluntario: esVoluntario,
        memberData: data,
        status: RegistrationStatus.editLoaded,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: RegistrationStatus.failureGeneric,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onUpdateRegistration(
    UpdateRegistration event,
    Emitter<RegistrationState> emit,
  ) async {
    emit(state.copyWith(status: RegistrationStatus.loading, errorMessage: null));
    try {
      await _repository.updateMember(event.memberId, event.request.toJson());
      emit(state.copyWith(status: RegistrationStatus.success));
    } catch (e) {
      emit(state.copyWith(
        status: RegistrationStatus.failureGeneric,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onDeleteMemberRequested(
    DeleteMemberRequested event,
    Emitter<RegistrationState> emit,
  ) async {
    emit(state.copyWith(status: RegistrationStatus.loading, errorMessage: null));
    try {
      await _repository.deleteMember(event.memberId);
      emit(state.copyWith(status: RegistrationStatus.deleteSuccess));
    } catch (e) {
      emit(state.copyWith(
        status: RegistrationStatus.failureGeneric,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onSubmitRegistration(
    SubmitRegistration event,
    Emitter<RegistrationState> emit,
  ) async {
    emit(
      state.copyWith(status: RegistrationStatus.loading, errorMessage: null),
    );
    try {
      await _repository.registerMember(event.request);
      emit(state.copyWith(status: RegistrationStatus.success));
    } catch (e) {
      final message = e.toString().replaceAll('Exception: ', '');
      if (message.contains('Esta persona ya existe') ||
          message.contains('409')) {
        emit(
          state.copyWith(
            status: RegistrationStatus.failureConflict,
            errorMessage: 'Esta persona ya existe',
          ),
        );
      } else {
        emit(
          state.copyWith(
            status: RegistrationStatus.failureGeneric,
            errorMessage: message,
          ),
        );
      }
    }
  }
}
