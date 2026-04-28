/// Modelo de presupuesto mensual. Ref: Solution Design, DB Schema p.12 — tabla BUDGET.
/// Incluye campos calculados: spent y progress (devueltos por la API).
class Budget {
  final int budgetId;
  final int userId;
  final int categoryId;
  final int month;
  final int year;
  final double limitAmount;
  final DateTime createdAt;
  final String? categoryName;
  final double spent;
  final double progress;

  const Budget({
    required this.budgetId,
    required this.userId,
    required this.categoryId,
    required this.month,
    required this.year,
    required this.limitAmount,
    required this.createdAt,
    this.categoryName,
    this.spent = 0.0,
    this.progress = 0.0,
  });

  factory Budget.fromJson(Map<String, dynamic> json) => Budget(
        budgetId: json['budget_id'] as int,
        userId: json['user_id'] as int,
        categoryId: json['category_id'] as int,
        month: json['month'] as int,
        year: json['year'] as int,
        limitAmount: double.parse(json['limit_amount'].toString()),
        createdAt: DateTime.parse(json['created_at'] as String),
        categoryName: json['category_name'] as String?,
        spent: double.parse((json['spent'] ?? '0.00').toString()),
        progress: (json['progress'] as num?)?.toDouble() ?? 0.0,
      );

  Map<String, dynamic> toJson() => {
        'category_id': categoryId,
        'limit_amount': limitAmount,
        'month': month,
        'year': year,
      };
}
