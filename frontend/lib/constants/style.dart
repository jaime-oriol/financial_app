/// Colores, sombras e iconos de la app. Theme juvenil para adolescentes (13-18).
import 'package:flutter/material.dart';

// Sombra por defecto para containers y cards
BoxShadow defaultShadow = BoxShadow(
  color: primary.withValues(alpha: 0.12),
  blurRadius: 4.0,
  offset: const Offset(0, 2),
);

// --- Colores principales ---
const primary = Color(0xFF1A1A2E);       // Titulos y texto principal
const secondary = Color(0xFF6C63FF);     // Botones, acciones, acentos
const accent = Color(0xFF00D9A6);        // Exito, progreso positivo
const warning = Color(0xFFFFB74D);       // Alertas, behind-pace
const error = Color(0xFFEF5350);         // Errores, sobre-presupuesto
const white = Color(0xFFFFFFFF);
const black = Color(0xFF000000);

// --- Grises ---
const grey1 = Color(0xFF757575);         // Texto secundario
const grey2 = Color(0xFFBDBDBD);         // Placeholders, disabled
const grey3 = Color(0xFFF5F5F5);         // Fondos de cards/surfaces

// --- Fondo ---
const background = Color(0xFFF8F9FE);    // Scaffold background

// --- Colores de categorias (6 seeds del backend) ---
const categoryFood = Color(0xFFFF6B6B);
const categoryTransport = Color(0xFF4ECDC4);
const categoryEntertainment = Color(0xFFFFE66D);
const categoryHealth = Color(0xFF95E1D3);
const categoryEducation = Color(0xFF6C63FF);
const categoryOther = Color(0xFFADB5BD);

/// Mapa de category_id a color (match con seeds del backend)
const Map<int, Color> categoryColors = {
  1: categoryFood,
  2: categoryTransport,
  3: categoryEntertainment,
  4: categoryHealth,
  5: categoryEducation,
  6: categoryOther,
};

/// Mapa de category_id a icono Material (match con seeds del backend)
const Map<int, IconData> categoryIcons = {
  1: Icons.restaurant,
  2: Icons.directions_bus,
  3: Icons.movie,
  4: Icons.local_hospital,
  5: Icons.school,
  6: Icons.more_horiz,
};
