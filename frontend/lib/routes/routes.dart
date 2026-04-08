/// Configuracion de rutas con onGenerateRoute.
import 'package:flutter/material.dart';

import '../pages/auth/login_page.dart';
import '../pages/auth/register_page.dart';
import '../pages/quiz/quiz_page.dart';
import '../pages/simulation/simulation_page.dart';
import '../pages/structure.dart';

Route<dynamic> makeRoute(RouteSettings settings) {
  switch (settings.name) {
    case '/':
      return _buildRoute(settings.name, const Structure());
    case '/register':
      return _buildRoute(settings.name, const RegisterPage());
    case '/login':
      return _buildRoute(settings.name, const LoginPage());
    case '/quiz':
      return _buildRoute(settings.name, const QuizPage());
    case '/simulation':
      return _buildRoute(settings.name, const SimulationPage());
    default:
      throw 'Route ${settings.name} is not defined';
  }
}

PageRoute _buildRoute(String? name, Widget page) {
  return MaterialPageRoute(
    settings: RouteSettings(name: name),
    builder: (_) => page,
  );
}
