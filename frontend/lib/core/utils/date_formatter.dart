/// Utility for formatting and parsing dates in MM/DD/YYYY format.
class DateFormatter {
  /// Format a [DateTime] into "MM/DD/YYYY" string.
  static String formatMMDDYYYY(DateTime? date) {
    if (date == null) return '';
    final month = date.month.toString().padLeft(2, '0');
    final day = date.day.toString().padLeft(2, '0');
    return '$month/$day/${date.year}';
  }

  /// Parse a date string ("MM/DD/YYYY" or "YYYY-MM-DD" or "MM-DD-YYYY") into [DateTime].
  static DateTime? parseDate(String? input) {
    if (input == null || input.trim().isEmpty) return null;
    final str = input.trim();

    // Check MM/DD/YYYY or MM-DD-YYYY
    final slashParts = str.split('/');
    if (slashParts.length == 3) {
      final m = int.tryParse(slashParts[0]);
      final d = int.tryParse(slashParts[1]);
      final y = int.tryParse(slashParts[2]);
      if (m != null && d != null && y != null) {
        return DateTime(y, m, d);
      }
    }

    final dashParts = str.split('-');
    if (dashParts.length == 3) {
      if (dashParts[0].length == 4) {
        // YYYY-MM-DD
        final y = int.tryParse(dashParts[0]);
        final m = int.tryParse(dashParts[1]);
        final d = int.tryParse(dashParts[2]);
        if (y != null && m != null && d != null) {
          return DateTime(y, m, d);
        }
      } else {
        // MM-DD-YYYY
        final m = int.tryParse(dashParts[0]);
        final d = int.tryParse(dashParts[1]);
        final y = int.tryParse(dashParts[2]);
        if (m != null && d != null && y != null) {
          return DateTime(y, m, d);
        }
      }
    }

    return DateTime.tryParse(str);
  }

  /// Convert any input date string ("YYYY-MM-DD" or "MM/DD/YYYY") into display "MM/DD/YYYY".
  static String displayDate(String? input) {
    if (input == null || input.trim().isEmpty) return '';
    final dt = parseDate(input);
    if (dt == null) return input;
    return formatMMDDYYYY(dt);
  }
}
