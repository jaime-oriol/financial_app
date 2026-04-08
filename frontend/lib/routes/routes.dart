/// Configuracion de rutas con onGenerateRoute y navegacion adaptativa.
import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../pages/auth/login_page.dart';
import '../pages/auth/register_page.dart';
import '../pages/structure.dart';

Route<dynamic> makeRoute(RouteSettings settings) {
  switch (settings.name) {
    case '/':
      return _buildRoute(settings.name, const Structure());
    case '/register':
      return _buildRoute(settings.name, const RegisterPage());
    case '/login':
      return _buildRoute(settings.name, const LoginPage());
    default:
      throw 'Route ${settings.name} is not defined';
  }
}

PageRoute _buildRoute(String? name, Widget page) {
  final settings = RouteSettings(name: name);
  if (Platform.isIOS) {
    return CupertinoPageRoute(settings: settings, builder: (_) => page);
  }
  return MaterialPageRoute(settings: settings, builder: (_) => page);
}
