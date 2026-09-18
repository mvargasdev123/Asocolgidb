/// Utility for formatting and parsing dates in DD/MM/YYYY format.
class DateFormatter {
  /// Format a [DateTime] into "DD/MM/YYYY" string.
  static String formatDDMMYYYY(DateTime? date) {
    if (date == null) return '';
    final month = date.month.toString().padLeft(2, '0');
    final day = date.day.toString().padLeft(2, '0');
    return '$day/$month/${date.year}';
  }

  /// Alias for backward compatibility, formats as "DD/MM/YYYY".
  static String formatMMDDYYYY(DateTime? date) => formatDDMMYYYY(date);

  /// Parse a date string ("DD/MM/YYYY" or "YYYY-MM-DD" or "MM/DD/YYYY") into [DateTime].
  static DateTime? parseDate(String? input) {
    if (input == null || input.trim().isEmpty) return null;
    final str = input.trim();

    // Check DD/MM/YYYY or MM/DD/YYYY
    final slashParts = str.split('/');
    if (slashParts.length == 3) {
      final p1 = int.tryParse(slashParts[0]);
      final p2 = int.tryParse(slashParts[1]);
      final p3 = int.tryParse(slashParts[2]);
      if (p1 != null && p2 != null && p3 != null) {
        if (p3 > 1000) {
          // p3 is year YYYY
          if (p1 > 12) {
            // p1 is day, p2 is month (DD/MM/YYYY)
            return DateTime(p3, p2, p1);
          } else if (p2 > 12) {
            // p2 is day, p1 is month (legacy MM/DD/YYYY)
            return DateTime(p3, p1, p2);
          } else {
            // Default DD/MM/YYYY
            return DateTime(p3, p2, p1);
          }
        } else if (p1 > 1000) {
          // YYYY/MM/DD
          return DateTime(p1, p2, p3);
        }
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
        // DD-MM-YYYY
        final d = int.tryParse(dashParts[0]);
        final m = int.tryParse(dashParts[1]);
        final y = int.tryParse(dashParts[2]);
        if (d != null && m != null && y != null) {
          if (d > 12) {
            return DateTime(y, m, d);
          } else if (m > 12) {
            return DateTime(y, d, m);
          } else {
            return DateTime(y, m, d);
          }
        }
      }
    }

    return DateTime.tryParse(str);
  }

  /// Convert any input date string ("YYYY-MM-DD" or "DD/MM/YYYY") into display "DD/MM/YYYY".
  static String displayDate(String? input) {
    if (input == null || input.trim().isEmpty) return '';
    final dt = parseDate(input);
    if (dt == null) return input;
    return formatDDMMYYYY(dt);
  }
}
