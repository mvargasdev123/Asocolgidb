import '../models/auth_response.dart';

abstract class AuthRepository {
  Future<AuthResponse> login(String email, String password);
  Future<AuthResponse> refreshToken(String currentToken);
  Future<void> forgotPassword();
}
