/// Modelo del dashboard. Ref: Solution Design, diagrama de secuencia 5.
/// Agrega spending por categoria, presupuestos y transacciones recientes.
import 'budget.dart';
import 'expense.dart';

class SpendingByCategory {
  final int categoryId;
  final String categoryName;
  final double total;

  const SpendingByCategory({
    required this.categoryId,
    required this.categoryName,
    required this.total,
  });

  factory SpendingByCategory.fromJson(Map<String, dynamic> json) =>
      SpendingByCategory(
        categoryId: json['category_id'] as int,
        categoryName: json['category_name'] as String,
        total: double.parse(json['total'].toString()),
      );
}

class Dashboard {
  final List<SpendingByCategory> spendingByCategory;
  final List<Budget> budgets;
  final List<Expense> recentTransactions;

  const Dashboard({
    required this.spendingByCategory,
    required this.budgets,
    required this.recentTransactions,
  });

  factory Dashboard.fromJson(Map<String, dynamic> json) => Dashboard(
        spendingByCategory: (json['spending_by_category'] as List)
            .map((e) => SpendingByCategory.fromJson(e))
            .toList(),
        budgets: (json['budgets'] as List)
            .map((e) => Budget.fromJson(e))
            .toList(),
        recentTransactions: (json['recent_transactions'] as List)
            .map((e) => Expense.fromJson(e))
            .toList(),
      );
}
