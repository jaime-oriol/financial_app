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
      backgroundColor: white,
      elevation: 0,
      scrolledUnderElevation: 0,
      centerTitle: true,
      iconTheme: IconThemeData(color: primary),
      titleTextStyle: TextStyle(
        color: primary,
        fontSize: 20,
        fontWeight: FontWeight.w700,
      ),
    ),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: white,
      selectedItemColor: secondary,
      unselectedItemColor: grey2,
      type: BottomNavigationBarType.fixed,
      elevation: 0,
      selectedLabelStyle: TextStyle(fontSize: 11, fontWeight: FontWeight.w600),
      unselectedLabelStyle: TextStyle(fontSize: 11),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ButtonStyle(
        foregroundColor: const WidgetStatePropertyAll(white),
        backgroundColor: WidgetStateProperty.resolveWith<Color>((states) {
          if (states.contains(WidgetState.disabled)) return grey2;
          return secondary;
        }),
        elevation: const WidgetStatePropertyAll(0),
        padding: const WidgetStatePropertyAll(
          EdgeInsets.symmetric(vertical: 14, horizontal: Sizes.xl),
        ),
        shape: WidgetStatePropertyAll(
          RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        textStyle: const WidgetStatePropertyAll(
          TextStyle(fontSize: 15.0, fontWeight: FontWeight.w600),
        ),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: grey3,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide.none,
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide.none,
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: secondary, width: 1.5),
      ),
      contentPadding: const EdgeInsets.symmetric(
        horizontal: Sizes.lg,
        vertical: 14,
      ),
      hintStyle: const TextStyle(color: grey2, fontSize: 15),
    ),
    cardTheme: CardThemeData(
      color: white,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
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
        borderRadius: BorderRadius.circular(10),
      ),
    ),
    chipTheme: ChipThemeData(
      backgroundColor: grey3,
      selectedColor: secondary.withValues(alpha: 0.15),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
      ),
      side: BorderSide.none,
      labelStyle: const TextStyle(fontSize: 13),
    ),
    textTheme: const TextTheme(
      displayLarge: TextStyle(fontSize: 32.0, fontWeight: FontWeight.w800, color: primary),
      displayMedium: TextStyle(fontSize: 26.0, fontWeight: FontWeight.w700, color: primary),
      headlineLarge: TextStyle(fontSize: 22.0, fontWeight: FontWeight.w700, color: primary),
      headlineMedium: TextStyle(fontSize: 20.0, fontWeight: FontWeight.w600, color: primary),
      titleLarge: TextStyle(fontSize: 17.0, fontWeight: FontWeight.w700, color: primary),
      titleMedium: TextStyle(fontSize: 15.0, fontWeight: FontWeight.w600, color: primary),
      titleSmall: TextStyle(fontSize: 14.0, fontWeight: FontWeight.w500, color: primary),
      bodyLarge: TextStyle(fontSize: 15.0, fontWeight: FontWeight.w400, color: primary),
      bodyMedium: TextStyle(fontSize: 14.0, fontWeight: FontWeight.w400, color: primary),
      bodySmall: TextStyle(fontSize: 12.0, fontWeight: FontWeight.w400, color: grey1),
      labelLarge: TextStyle(fontSize: 11.0, fontWeight: FontWeight.w600, color: grey1),
      labelMedium: TextStyle(fontSize: 10.0, fontWeight: FontWeight.w400, color: grey1),
      labelSmall: TextStyle(fontSize: 9.0, fontWeight: FontWeight.w600, color: grey2),
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
