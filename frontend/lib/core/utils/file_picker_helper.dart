import 'file_picker_stub.dart'
    if (dart.library.html) 'file_picker_web.dart'
    if (dart.library.io) 'file_picker_io.dart';

class CustomFilePicker {
  static Future<Map<String, dynamic>?> pickExcelFile() {
    return pickExcelFileImpl();
  }
}
