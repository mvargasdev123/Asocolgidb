import 'package:dio/dio.dart';
import '../../../../core/network/dio_client.dart';
import '../../domain/models/auth_response.dart';
import '../../domain/repositories/auth_repository.dart';

class AuthRepositoryImpl implements AuthRepository {
  final Dio _dio;

  // URL base consumida de la configuración centralizada de DioClient
  static String get _baseUrl => DioClient.baseUrl;

  AuthRepositoryImpl({Dio? dio})
    : _dio = dio ?? Dio(BaseOptions(baseUrl: _baseUrl));

  @override
  Future<AuthResponse> login(String email, String password) async {
    try {
      final response = await _dio.post(
        '/auth/login',
        data: {'username': email, 'password': password},
        options: Options(contentType: Headers.formUrlEncodedContentType),
      );

      if (response.statusCode == 200) {
        return AuthResponse.fromJson(response.data);
      } else {
        throw Exception('Error al iniciar sesión');
      }
    } on DioException catch (e) {
      if (e.response != null) {
        // Manejar errores de IP bloqueada (429 Too Many Requests) u otros como 401/403
        if (e.response?.statusCode == 429) {
          throw Exception(
            'IP bloqueada temporalmente por intentos fallidos. Revisa el correo oficial.',
          );
        } else if (e.response?.statusCode == 401 ||
            e.response?.statusCode == 403) {
          throw Exception('Credenciales incorrectas');
        }

        // Tratar de sacar el detalle del JSON que envía FastAPI: {"detail": "..."}
        final data = e.response?.data;
        if (data is Map<String, dynamic> && data.containsKey('detail')) {
          throw Exception(data['detail']);
        }
      }
      throw Exception('Error de conexión con el servidor.');
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  @override
  Future<void> forgotPassword() async {
    try {
      // Envía a la cuenta predefinida por la especificación
      await _dio.post(
        '/forgot-password',
        data: {'email': 'asocolgibasededatos@gmail.com'},
      );
    } on DioException catch (e) {
      if (e.response != null) {
        final data = e.response?.data;
        if (data is Map<String, dynamic> && data.containsKey('detail')) {
          throw Exception(data['detail']);
        }
      }
      throw Exception('Error al solicitar recuperación de contraseña.');
    } catch (e) {
      throw Exception(e.toString());
    }
  }
}
