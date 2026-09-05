import 'package:equatable/equatable.dart';

abstract class AuthEvent extends Equatable {
  const AuthEvent();

  @override
  List<Object> get props => [];
}

class LoginRequested extends AuthEvent {
  final String email;
  final String password;

  const LoginRequested(this.email, this.password);

  @override
  List<Object> get props => [email, password];
}

class ForgotPasswordRequested extends AuthEvent {
  const ForgotPasswordRequested();
}

class TogglePasswordVisibility extends AuthEvent {
  const TogglePasswordVisibility();
}
