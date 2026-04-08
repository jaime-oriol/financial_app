/// Tamanios estandar y utilidades de pantalla.
import 'package:flutter/material.dart';

/// Tamanios estandar para padding, margin, iconos, bordes.
class Sizes {
  static const double unit = 16;

  /// 2px
  static const double xxs = 0.125 * unit;

  /// 4px
  static const double xs = 0.25 * unit;

  /// 8px
  static const double sm = 0.5 * unit;

  /// 12px
  static const double md = 0.75 * unit;

  /// 16px
  static const double lg = unit;

  /// 24px
  static const double xl = 1.5 * unit;

  /// 32px
  static const double xxl = 2 * unit;

  /// Border radius por defecto: 8px
  static const double borderRadius = 0.5 * unit;

  /// Border radius grande: 16px
  static const double borderRadiusLarge = unit;

  /// Border radius small: 4px
  static const double borderRadiusSmall = 0.25 * unit;
}

/// Extension en BuildContext para detectar si el teclado esta visible.
extension ScreenUtils on BuildContext {
  bool get isKeyboardVisible => MediaQuery.of(this).viewInsets.bottom > 100;
}
