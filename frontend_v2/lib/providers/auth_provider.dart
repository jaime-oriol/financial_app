/// Provider de autenticacion: registro, login, logout y estado de sesion.
/// Ref: Solution Design, UC-01 Register Account.
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../services/api_client.dart';

/// Instancia global de SharedPreferences
final sharedPrefsProvider = Provider<SharedPreferences>((ref) {
  throw UnimplementedError('Debe inicializarse en main.dart con override');
});

/// Instancia global del API client
final apiClientProvider = Provider<ApiClient>((ref) {
  final prefs = ref.watch(sharedPrefsProvider);
  return ApiClient(prefs);
});

/// Estado de autenticacion
final authStateProvider = ChangeNotifierProvider<AuthNotifier>((ref) {
  final api = ref.watch(apiClientProvider);
  return AuthNotifier(api);
});

class AuthNotifier extends ChangeNotifier {
  final ApiClient _api;
  bool _loading = false;
  String? _error;

  AuthNotifier(this._api);

  bool get isAuthenticated => _api.isAuthenticated;
  bool get loading => _loading;
  String? get error => _error;

  /// UC-01: Registrar cuenta nueva
  Future<bool> register({
    required String name,
    required String surname,
    required String birthdate,
    required String email,
    required String password,
  }) async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      final data = await _api.post('/auth/register', body: {
        'name': name,
        'surname': surname,
        'birthdate': birthdate,
        'email': email,
        'password': password,
      });
      await _api.saveAuth(data['token'], data['user_id']);
      _loading = false;
      notifyListeners();
      return true;
    } on ApiException catch (e) {
      _error = e.message;
      _loading = false;
      notifyListeners();
      return false;
    }
  }

  /// Login con email y password
  Future<bool> login({
    required String email,
    required String password,
  }) async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      final data = await _api.post('/auth/login', body: {
        'email': email,
        'password': password,
      });
      await _api.saveAuth(data['token'], data['user_id']);
      _loading = false;
      notifyListeners();
      return true;
    } on ApiException catch (e) {
      _error = e.message;
      _loading = false;
      notifyListeners();
      return false;
    }
  }

  /// Cerrar sesion
  Future<void> logout() async {
    await _api.clearAuth();
    notifyListeners();
  }
}
