import 'dart:async';
import 'dart:html' as html;
import 'dart:typed_data';

Future<Map<String, dynamic>?> pickExcelFileImpl() async {
  final uploadInput = html.FileUploadInputElement();
  uploadInput.accept = '.xlsx,.xls';
  uploadInput.click();

  await uploadInput.onChange.first;
  final files = uploadInput.files;
  if (files == null || files.isEmpty) return null;

  final file = files.first;
  final reader = html.FileReader();
  reader.readAsArrayBuffer(file);
  await reader.onLoadEnd.first;

  final result = reader.result;
  if (result is Uint8List) {
    return {'bytes': result.toList(), 'name': file.name};
  } else if (result is ByteBuffer) {
    return {'bytes': result.asUint8List().toList(), 'name': file.name};
  }
  return null;
}
