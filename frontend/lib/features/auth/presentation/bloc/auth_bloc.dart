import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../../../core/network/token_storage.dart';
import 'auth_event.dart';
import 'auth_state.dart';

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final AuthRepository _authRepository;
  final TokenStorage _tokenStorage;

  AuthBloc({
    required AuthRepository authRepository,
    required TokenStorage tokenStorage,
  })
    : _authRepository = authRepository,
      _tokenStorage = tokenStorage,
      super(const AuthState()) {
    on<LoginRequested>(_onLoginRequested);
    on<ForgotPasswordRequested>(_onForgotPasswordRequested);
    on<TogglePasswordVisibility>(_onTogglePasswordVisibility);
  }

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(state.copyWith(status: AuthStatus.loading, errorMessage: null));
    try {
      final response = await _authRepository.login(event.email, event.password);
      if (response.accessToken != null) {
        await _tokenStorage.saveToken(response.accessToken!);
      }
      emit(state.copyWith(status: AuthStatus.success, response: response));
    } catch (e) {
      emit(
        state.copyWith(
          status: AuthStatus.failure,
          errorMessage: e.toString().replaceAll('Exception: ', ''),
        ),
      );
    }
  }

  Future<void> _onForgotPasswordRequested(
    ForgotPasswordRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(
      state.copyWith(
        status: AuthStatus.loading,
        errorMessage: null,
        isForgotPasswordSuccess: false,
      ),
    );
    try {
      await _authRepository.forgotPassword();
      // Mantenemos el estado de éxito sin cambiar la pantalla entera
      emit(
        state.copyWith(
          status: AuthStatus.initial,
          isForgotPasswordSuccess: true,
        ),
      );
    } catch (e) {
      emit(
        state.copyWith(
          status: AuthStatus.failure,
          errorMessage: e.toString().replaceAll('Exception: ', ''),
        ),
      );
    }
  }

  void _onTogglePasswordVisibility(
    TogglePasswordVisibility event,
    Emitter<AuthState> emit,
  ) {
    emit(state.copyWith(obscurePassword: !state.obscurePassword));
  }
}
