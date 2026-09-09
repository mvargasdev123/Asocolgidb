import 'dart:convert';
import 'package:dio/dio.dart';
import '../../domain/repositories/excel_repository.dart';

class ExcelRepositoryImpl implements ExcelRepository {
  final Dio _dio;

  ExcelRepositoryImpl(this._dio);

  @override
  Future<String> exportarAEmail(String tipoExportacion) async {
    try {
      final response = await _dio.post(
        '/excel/exportar',
        data: {'tipo_exportacion': tipoExportacion},
      );
      return response.data['message'] as String? ??
          'Archivo generado en memoria y enviado al correo oficial.';
    } on DioException catch (e) {
      final msg = e.response?.data?['detail'] ?? 'Error al exportar el archivo.';
      throw Exception(msg);
    }
  }

  @override
  Future<List<int>> descargarDirecto(String tipoExportacion) async {
    try {
      final response = await _dio.post(
        '/excel/descargar-directo',
        data: {'tipo_exportacion': tipoExportacion},
        options: Options(responseType: ResponseType.bytes),
      );
      final data = response.data;
      if (data is List<int>) {
        return data;
      } else if (data is List) {
        return List<int>.from(data);
      } else {
        throw Exception('Respuesta no válida del servidor.');
      }
    } on DioException catch (e) {
      final msg = e.response?.data?['detail'] ?? 'Error al descargar el archivo.';
      throw Exception(msg);
    }
  }

  @override
  Future<Map<String, dynamic>> analizarImportacion(
      List<int> bytes, String filename) async {
    try {
      final formData = FormData.fromMap({
        'file': MultipartFile.fromBytes(bytes, filename: filename),
      });

      final response = await _dio.post(
        '/excel/analizar-importacion',
        data: formData,
      );

      return response.data['reporte'] as Map<String, dynamic>;
    } on DioException catch (e) {
      final msg = e.response?.data?['detail'] ?? 'Error al analizar el archivo Excel.';
      throw Exception(msg);
    }
  }

  @override
  Future<Map<String, dynamic>> confirmarImportacion(
      List<int> bytes, String filename, Map<String, String> decisiones) async {
    try {
      final formData = FormData.fromMap({
        'file': MultipartFile.fromBytes(bytes, filename: filename),
        'decisiones_json': jsonEncode(decisiones),
      });

      final response = await _dio.post(
        '/excel/confirmar-importacion',
        data: formData,
      );

      return response.data as Map<String, dynamic>;
    } on DioException catch (e) {
      final msg = e.response?.data?['detail'] ?? 'Error al confirmar la importación.';
      throw Exception(msg);
    }
  }
}
