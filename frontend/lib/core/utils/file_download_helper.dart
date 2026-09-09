import 'file_download_helper_stub.dart'
    if (dart.library.html) 'file_download_helper_web.dart';

void downloadFileBytes(List<int> bytes, String filename) {
  downloadFileBytesImpl(bytes, filename);
}
