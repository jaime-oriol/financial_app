/// Colores, sombras e iconos de la app. Theme juvenil para adolescentes (13-18).
import 'package:flutter/material.dart';

// Sombra suave para cards
BoxShadow defaultShadow = BoxShadow(
  color: Colors.black.withValues(alpha: 0.06),
  blurRadius: 12.0,
  offset: const Offset(0, 4),
);

// --- Colores principales (alineados con wireframes) ---
const primary = Color(0xFF16213E);       // Titulos, header oscuro
const secondary = Color(0xFF2675E3);     // Botones, acciones, links
const accent = Color(0xFF27AE60);        // Exito, on track, progreso positivo
const warning = Color(0xFFF39C12);       // Alertas, behind-pace, streak
const error = Color(0xFFE74C3C);         // Gastos, sobre-presupuesto
const white = Color(0xFFFFFFFF);
const black = Color(0xFF000000);

// --- Grises ---
const grey1 = Color(0xFF7F8C8D);         // Texto secundario, labels
const grey2 = Color(0xFFBDC3C7);         // Placeholders, iconos disabled
const grey3 = Color(0xFFF0F2F5);         // Fondos de inputs y cards

// --- Fondo ---
const background = Color(0xFFFAFBFD);    // Scaffold background

// --- Colores de categorias (6 seeds del backend) ---
const categoryFood = Color(0xFFE74C3C);
const categoryTransport = Color(0xFF2980B9);
const categoryEntertainment = Color(0xFFF1C40F);
const categoryHealth = Color(0xFF1ABC9C);
const categoryEducation = Color(0xFF8E44AD);
const categoryOther = Color(0xFF95A5A6);

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
