abstract class ExcelRepository {
  Future<String> exportarAEmail(String tipoExportacion);
  Future<List<int>> descargarDirecto(String tipoExportacion);
  Future<Map<String, dynamic>> analizarImportacion(List<int> bytes, String filename);
  Future<Map<String, dynamic>> confirmarImportacion(List<int> bytes, String filename, Map<String, String> decisiones);
}
