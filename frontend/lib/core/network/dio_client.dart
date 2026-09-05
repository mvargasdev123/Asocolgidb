import 'package:dio/dio.dart';
import 'token_storage.dart';

class DioClient {
  static const String baseUrl = 'http://127.0.0.1:8001';
  final Dio dio;
  final TokenStorage tokenStorage;

  DioClient({required this.tokenStorage})
      : dio = Dio(BaseOptions(baseUrl: baseUrl)) {
    
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // Leer token e inyectarlo si existe
          final token = await tokenStorage.getToken();
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          return handler.next(options);
        },
        onError: (DioException e, handler) async {
          // Manejo global de expiración de token si backend responde 401
          if (e.response?.statusCode == 401) {
            await tokenStorage.deleteToken();
            // TODO: Podría emitirse un evento o trigger para desloguear al usuario a nivel UI
          }
          return handler.next(e);
        },
      ),
    );
  }
}
