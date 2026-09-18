import 'dart:async';
import 'package:flutter/material.dart';

/// Servicio global para rastrear inactividad del usuario y gestionar 
/// la renovación de sesión (Sliding Expiration) y aviso previo de expiración.
class InactivityService {
  static final InactivityService _instance = InactivityService._internal();
  factory InactivityService() => _instance;
  InactivityService._internal();

  // Tiempos configurados: 60 min de inactividad total, aviso 2 min antes (a los 58 min)
  static const Duration inactivityDuration = Duration(minutes: 60);
  static const Duration warningLeadTime = Duration(minutes: 2);
  static const Duration minRefreshInterval = Duration(minutes: 15);

  Timer? _warningTimer;
  Timer? _expirationTimer;
  DateTime? _lastRefreshTime;
  DateTime? _lastActivityTime;

  bool _isWarningDialogShowing = false;

  VoidCallback? onShowWarningDialog;
  VoidCallback? onDismissWarningDialog;
  VoidCallback? onSessionExpired;
  VoidCallback? onAutoRefreshRequested;

  void initialize({
    required VoidCallback onShowWarning,
    required VoidCallback onDismissWarning,
    required VoidCallback onExpired,
    required VoidCallback onAutoRefresh,
  }) {
    onShowWarningDialog = onShowWarning;
    onDismissWarningDialog = onDismissWarning;
    onSessionExpired = onExpired;
    onAutoRefreshRequested = onAutoRefresh;
  }

  /// Inicia o reinicia el monitoreo de sesión al autenticarse exitosamente.
  void startMonitoring() {
    _lastRefreshTime = DateTime.now();
    _lastActivityTime = DateTime.now();
    _isWarningDialogShowing = false;
    _resetTimers();
  }

  /// Detiene todos los temporizadores (al cerrar sesión o en login).
  void stopMonitoring() {
    _warningTimer?.cancel();
    _expirationTimer?.cancel();
    _warningTimer = null;
    _expirationTimer = null;
    _isWarningDialogShowing = false;
  }

  /// Notifica que el token se acaba de renovar con éxito.
  void notifyTokenRefreshed() {
    _lastRefreshTime = DateTime.now();
  }

  /// Registra interacción del usuario (movimiento de ratón, clics, teclas, scroll o llamadas API).
  void recordUserActivity() {
    final now = DateTime.now();
    _lastActivityTime = now;

    // Si la advertencia previa está visible y el usuario realiza una acción, la cerramos y renovamos
    if (_isWarningDialogShowing) {
      _isWarningDialogShowing = false;
      onDismissWarningDialog?.call();
      onAutoRefreshRequested?.call();
      _resetTimers();
      return;
    }

    _resetTimers();

    // Si el usuario está activo y han pasado más de 15 minutos desde el último refresco, renovamos token en segundo plano
    if (_lastRefreshTime == null ||
        now.difference(_lastRefreshTime!) >= minRefreshInterval) {
      _lastRefreshTime = now;
      onAutoRefreshRequested?.call();
    }
  }

  void _resetTimers() {
    _warningTimer?.cancel();
    _expirationTimer?.cancel();

    // Temporizador de advertencia previa a los 58 minutos (2 min antes de los 60 min)
    final warningDuration = inactivityDuration - warningLeadTime;
    _warningTimer = Timer(warningDuration, () {
      _isWarningDialogShowing = true;
      onShowWarningDialog?.call();
    });

    // Temporizador de expiración definitiva a los 60 minutos
    _expirationTimer = Timer(inactivityDuration, () {
      _isWarningDialogShowing = false;
      onDismissWarningDialog?.call();
      stopMonitoring();
      onSessionExpired?.call();
    });
  }
}
