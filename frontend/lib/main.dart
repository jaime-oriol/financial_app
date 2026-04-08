/// Punto de entrada de la app. Inicializa providers y decide ruta inicial.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'providers/auth_provider.dart';
import 'routes/routes.dart';
import 'ui/theme/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final sharedPreferences = await SharedPreferences.getInstance();

  runApp(
    ProviderScope(
      overrides: [
        sharedPrefsProvider.overrideWithValue(sharedPreferences),
      ],
      child: const FappLauncher(),
    ),
  );
}

class FappLauncher extends ConsumerWidget {
  const FappLauncher({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auth = ref.watch(authStateProvider);

    return MaterialApp(
      title: 'FAPP',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      onGenerateRoute: makeRoute,
      // Si hay token guardado ir al home, sino al registro
      initialRoute: auth.isAuthenticated ? '/' : '/register',
    );
  }
}
