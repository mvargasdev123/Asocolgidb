import 'package:file_picker/file_picker.dart';

Future<Map<String, dynamic>?> pickExcelFileImpl() async {
  final files = await FilePicker.pickFiles(
    type: FileType.custom,
    allowedExtensions: ['xlsx', 'xls'],
  );
  if (files.isNotEmpty) {
    final file = files.first;
    final bytes = await file.readAsBytes();
    return {'bytes': bytes, 'name': file.name};
  }
  return null;
}
