/// Theme centralizado de la app. Colores juveniles, tipografia moderna.
import 'package:flutter/material.dart';

import '../../constants/style.dart';
import '../device.dart';

class AppTheme {
  static final lightTheme = ThemeData(
    colorScheme: _lightColorScheme,
    scaffoldBackgroundColor: background,
    fontFamily: 'Roboto',
    appBarTheme: const AppBarTheme(
      backgroundColor: background,
      elevation: 0,
      scrolledUnderElevation: 0,
      centerTitle: true,
      iconTheme: IconThemeData(color: primary),
      titleTextStyle: TextStyle(
        color: primary,
        fontSize: 18,
        fontWeight: FontWeight.w700,
      ),
    ),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: white,
      selectedItemColor: secondary,
      unselectedItemColor: grey2,
      type: BottomNavigationBarType.fixed,
      selectedLabelStyle: const TextStyle(fontSize: 12),
      unselectedLabelStyle: const TextStyle(fontSize: 12),
    ),
    floatingActionButtonTheme: const FloatingActionButtonThemeData(
      backgroundColor: secondary,
      foregroundColor: white,
      shape: CircleBorder(),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ButtonStyle(
        foregroundColor: const WidgetStatePropertyAll(white),
        backgroundColor: WidgetStateProperty.resolveWith<Color>((states) {
          if (states.contains(WidgetState.disabled)) return grey2;
          return secondary;
        }),
        elevation: const WidgetStatePropertyAll(0),
        padding: const WidgetStatePropertyAll(EdgeInsets.all(Sizes.lg)),
        shape: WidgetStatePropertyAll(
          RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(Sizes.borderRadiusLarge),
          ),
        ),
        textStyle: const WidgetStatePropertyAll(
          TextStyle(fontSize: 16.0, fontWeight: FontWeight.w600),
        ),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: grey3,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(Sizes.borderRadius),
        borderSide: BorderSide.none,
      ),
      contentPadding: const EdgeInsets.symmetric(
        horizontal: Sizes.lg,
        vertical: Sizes.md,
      ),
      hintStyle: const TextStyle(color: grey2),
    ),
    cardTheme: CardThemeData(
      color: white,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(Sizes.borderRadius),
      ),
    ),
    dividerTheme: const DividerThemeData(
      color: grey3,
      space: 1,
      thickness: 1,
    ),
    snackBarTheme: SnackBarThemeData(
      backgroundColor: primary,
      contentTextStyle: const TextStyle(color: white, fontSize: 14),
      behavior: SnackBarBehavior.floating,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(Sizes.borderRadius),
      ),
    ),
    textTheme: const TextTheme(
      // Display: titulos grandes (dashboard balance)
      displayLarge: TextStyle(fontSize: 34.0, fontWeight: FontWeight.w700),
      displayMedium: TextStyle(fontSize: 28.0, fontWeight: FontWeight.w600),
      // Headline: secciones
      headlineLarge: TextStyle(fontSize: 24.0, fontWeight: FontWeight.w700),
      headlineMedium: TextStyle(fontSize: 20.0, fontWeight: FontWeight.w600),
      // Title: cards, items
      titleLarge: TextStyle(fontSize: 18.0, fontWeight: FontWeight.w700),
      titleMedium: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w600),
      titleSmall: TextStyle(fontSize: 14.0, fontWeight: FontWeight.w500),
      // Body: contenido
      bodyLarge: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w400),
      bodyMedium: TextStyle(fontSize: 14.0, fontWeight: FontWeight.w400),
      bodySmall: TextStyle(fontSize: 12.0, fontWeight: FontWeight.w400),
      // Label: badges, captions
      labelLarge: TextStyle(fontSize: 12.0, fontWeight: FontWeight.w600),
      labelMedium: TextStyle(fontSize: 10.0, fontWeight: FontWeight.w400),
      labelSmall: TextStyle(fontSize: 8.0, fontWeight: FontWeight.w600),
    ),
  );
}

const _lightColorScheme = ColorScheme(
  brightness: Brightness.light,
  primary: primary,
  onPrimary: white,
  secondary: secondary,
  onSecondary: white,
  tertiary: accent,
  error: error,
  onError: white,
  surface: white,
  onSurface: primary,
);
