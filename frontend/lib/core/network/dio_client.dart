import 'package:dio/dio.dart';
import 'token_storage.dart';
import 'inactivity_service.dart';

class DioClient {
  static const String baseUrl = String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: 'https://asocolgidb.onrender.com',
  );
  final Dio dio;
  final TokenStorage tokenStorage;

  DioClient({required this.tokenStorage})
      : dio = Dio(
          BaseOptions(
            baseUrl: baseUrl,
            connectTimeout: const Duration(seconds: 60),
            receiveTimeout: const Duration(seconds: 60),
            sendTimeout: const Duration(seconds: 60),
          ),
        ) {
    
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // Leer token e inyectarlo si existe
          final token = await tokenStorage.getToken();
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          
          // Notificar actividad al hacer peticiones API (salvo login)
          if (!options.path.contains('/auth/login')) {
            InactivityService().recordUserActivity();
          }
          
          return handler.next(options);
        },
        onError: (DioException e, handler) async {
          final isAuthEndpoint = e.requestOptions.path.contains('/auth/login') ||
              e.requestOptions.path.contains('/auth/refresh');

          // Si el servidor responde 401 en una petición protegida
          if (e.response?.statusCode == 401 && !isAuthEndpoint) {
            final currentToken = await tokenStorage.getToken();
            if (currentToken != null) {
              try {
                // Intentar auto-refresco único transparente de token
                final refreshResponse = await dio.post(
                  '/auth/refresh',
                  options: Options(
                    headers: {'Authorization': 'Bearer $currentToken'},
                  ),
                );

                if (refreshResponse.statusCode == 200 && refreshResponse.data != null) {
                  final newToken = refreshResponse.data['access_token'] as String?;
                  if (newToken != null) {
                    await tokenStorage.saveToken(newToken);
                    InactivityService().notifyTokenRefreshed();

                    // Reintentar la petición original sin interrumpir al usuario
                    final opts = e.requestOptions;
                    opts.headers['Authorization'] = 'Bearer $newToken';
                    final clonedResponse = await dio.fetch(opts);
                    return handler.resolve(clonedResponse);
                  }
                }
              } catch (_) {
                // Si el refresco transparente falla, la sesión realmente expiró
              }
            }

            // Si no fue posible refrescar, purgar sesión y notificar
            await tokenStorage.deleteToken();
            InactivityService().onSessionExpired?.call();
          }
          return handler.next(e);
        },
      ),
    );
  }
}
