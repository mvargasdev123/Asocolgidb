import 'package:equatable/equatable.dart';
import '../../domain/models/auth_response.dart';

enum AuthStatus { initial, loading, success, failure }

class AuthState extends Equatable {
  final AuthStatus status;
  final AuthResponse? response;
  final String? errorMessage;
  final bool obscurePassword;
  final bool isForgotPasswordSuccess;

  const AuthState({
    this.status = AuthStatus.initial,
    this.response,
    this.errorMessage,
    this.obscurePassword = true,
    this.isForgotPasswordSuccess = false,
  });

  AuthState copyWith({
    AuthStatus? status,
    AuthResponse? response,
    String? errorMessage,
    bool? obscurePassword,
    bool? isForgotPasswordSuccess,
  }) {
    return AuthState(
      status: status ?? this.status,
      response: response ?? this.response,
      errorMessage: errorMessage ?? this.errorMessage,
      obscurePassword: obscurePassword ?? this.obscurePassword,
      isForgotPasswordSuccess:
          isForgotPasswordSuccess ?? this.isForgotPasswordSuccess,
    );
  }

  @override
  List<Object?> get props => [
    status,
    response,
    errorMessage,
    obscurePassword,
    isForgotPasswordSuccess,
  ];
}
