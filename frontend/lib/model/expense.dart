/// Modelo de gasto. Ref: Solution Design, DB Schema p.12 — tabla EXPENSE.
/// Relaciones: user_id -> Users (N:1), category_id -> Categories (N:1).
class Expense {
  final int expenseId;
  final int userId;
  final int categoryId;
  final double amount;
  final String description;
  final DateTime expenseDate;
  final DateTime createdAt;
  final String? categoryName;

  const Expense({
    required this.expenseId,
    required this.userId,
    required this.categoryId,
    required this.amount,
    required this.description,
    required this.expenseDate,
    required this.createdAt,
    this.categoryName,
  });

  factory Expense.fromJson(Map<String, dynamic> json) => Expense(
        expenseId: json['expense_id'] as int,
        userId: json['user_id'] as int,
        categoryId: json['category_id'] as int,
        amount: double.parse(json['amount'].toString()),
        description: json['description'] as String,
        expenseDate: DateTime.parse(json['expense_date'] as String),
        createdAt: DateTime.parse(json['created_at'] as String),
        categoryName: json['category_name'] as String?,
      );

  Map<String, dynamic> toJson() => {
        'amount': amount,
        'description': description,
        'expense_date': expenseDate.toIso8601String().split('T').first,
        'category_id': categoryId,
      };
}
