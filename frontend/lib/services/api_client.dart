/// Cliente HTTP centralizado. Gestiona JWT, base URL y errores.
/// Todos los providers usan esta clase para comunicarse con el backend.
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiClient {
  // En desarrollo local: 10.0.2.2 para emulador Android, localhost para web
  static const String _baseUrl = 'http://10.0.2.2:8000/api';
  static const String _tokenKey = 'jwt_token';
  static const String _userIdKey = 'user_id';

  final SharedPreferences _prefs;

  ApiClient(this._prefs);

  /// Token JWT almacenado localmente
  String? get token => _prefs.getString(_tokenKey);

  /// ID del usuario logueado
  int? get userId {
    final id = _prefs.getInt(_userIdKey);
    return id;
  }

  /// Guardar credenciales tras login/registro
  Future<void> saveAuth(String token, int userId) async {
    await _prefs.setString(_tokenKey, token);
    await _prefs.setInt(_userIdKey, userId);
  }

  /// Borrar credenciales (logout)
  Future<void> clearAuth() async {
    await _prefs.remove(_tokenKey);
    await _prefs.remove(_userIdKey);
  }

  /// Si hay token guardado
  bool get isAuthenticated => token != null;

  /// Headers comunes: JSON + JWT si existe
  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };

  /// GET request
  Future<dynamic> get(String path, {Map<String, String>? queryParams}) async {
    final uri = Uri.parse('$_baseUrl$path').replace(queryParameters: queryParams);
    final response = await http.get(uri, headers: _headers);
    return _handleResponse(response);
  }

  /// POST request
  Future<dynamic> post(String path, {Map<String, dynamic>? body}) async {
    final uri = Uri.parse('$_baseUrl$path');
    final response = await http.post(
      uri,
      headers: _headers,
      body: body != null ? jsonEncode(body) : null,
    );
    return _handleResponse(response);
  }

  /// Procesar respuesta: decodificar JSON o lanzar error
  dynamic _handleResponse(http.Response response) {
    final body = jsonDecode(response.body);

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return body;
    }

    // Extraer mensaje de error del backend
    final detail = body is Map ? body['detail'] ?? 'Unknown error' : 'Unknown error';
    throw ApiException(response.statusCode, detail.toString());
  }
}

/// Excepcion con codigo HTTP y mensaje del backend
class ApiException implements Exception {
  final int statusCode;
  final String message;

  ApiException(this.statusCode, this.message);

  @override
  String toString() => 'ApiException($statusCode): $message';
}
