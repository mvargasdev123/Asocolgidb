import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../../../core/network/token_storage.dart';
import '../../../../core/network/inactivity_service.dart';
import 'auth_event.dart';
import 'auth_state.dart';

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final AuthRepository _authRepository;
  final TokenStorage _tokenStorage;

  AuthBloc({
    required AuthRepository authRepository,
    required TokenStorage tokenStorage,
  })  : _authRepository = authRepository,
        _tokenStorage = tokenStorage,
        super(const AuthState()) {
    on<LoginRequested>(_onLoginRequested);
    on<ForgotPasswordRequested>(_onForgotPasswordRequested);
    on<TogglePasswordVisibility>(_onTogglePasswordVisibility);
    on<AutoRefreshTokenRequested>(_onAutoRefreshTokenRequested);
    on<SessionExpiredByInactivity>(_onSessionExpiredByInactivity);
    on<LogoutRequested>(_onLogoutRequested);
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
        InactivityService().startMonitoring();
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

  Future<void> _onAutoRefreshTokenRequested(
    AutoRefreshTokenRequested event,
    Emitter<AuthState> emit,
  ) async {
    try {
      final currentToken = await _tokenStorage.getToken();
      if (currentToken != null) {
        final response = await _authRepository.refreshToken(currentToken);
        if (response.accessToken != null) {
          await _tokenStorage.saveToken(response.accessToken!);
          InactivityService().notifyTokenRefreshed();
        }
      }
    } catch (_) {
      // Si el auto-refresco en segundo plano falla por red efímera, el interceptor reintentará
    }
  }

  Future<void> _onSessionExpiredByInactivity(
    SessionExpiredByInactivity event,
    Emitter<AuthState> emit,
  ) async {
    await _tokenStorage.deleteToken();
    InactivityService().stopMonitoring();
    emit(state.copyWith(
      status: AuthStatus.sessionExpired,
      errorMessage: 'Tu sesión ha expirado por inactividad. Por favor inicia sesión de nuevo.',
    ));
  }

  Future<void> _onLogoutRequested(
    LogoutRequested event,
    Emitter<AuthState> emit,
  ) async {
    await _tokenStorage.deleteToken();
    InactivityService().stopMonitoring();
    emit(const AuthState(status: AuthStatus.initial));
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
