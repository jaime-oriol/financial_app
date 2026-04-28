/// Modelo de categoria de gasto. Ref: Solution Design, DB Schema p.12 — tabla CATEGORY.
class Category {
  final int categoryId;
  final String name;
  final String? icon;
  final String? description;

  const Category({
    required this.categoryId,
    required this.name,
    this.icon,
    this.description,
  });

  factory Category.fromJson(Map<String, dynamic> json) => Category(
        categoryId: json['category_id'] as int,
        name: json['name'] as String,
        icon: json['icon'] as String?,
        description: json['description'] as String?,
      );

  Map<String, dynamic> toJson() => {
        'category_id': categoryId,
        'name': name,
        'icon': icon,
        'description': description,
      };
}
