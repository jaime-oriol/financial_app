/// Chip selector de categoria reutilizable en formularios de expense y budget.
import 'package:flutter/material.dart';

import '../../constants/style.dart';
import '../../model/category.dart';

class CategoryChip extends StatelessWidget {
  const CategoryChip({
    required this.category,
    required this.selected,
    required this.onSelected,
    super.key,
  });

  final Category category;
  final bool selected;
  final VoidCallback onSelected;

  @override
  Widget build(BuildContext context) {
    final color = categoryColors[category.categoryId] ?? grey2;

    return ChoiceChip(
      label: Text(category.name),
      selected: selected,
      selectedColor: color.withValues(alpha: 0.3),
      backgroundColor: grey3,
      labelStyle: TextStyle(
        color: selected ? primary : grey1,
        fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
      ),
      avatar: Icon(
        categoryIcons[category.categoryId] ?? Icons.category,
        size: 18,
        color: color,
      ),
      onSelected: (_) => onSelected(),
    );
  }
}
