/// Provider de gastos: crear y listar con filtros.
/// Ref: Solution Design, UC-02 Add Expense, UC-04 View Expense History.
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../model/expense.dart';
import '../services/api_client.dart';
import 'auth_provider.dart';

/// Lista de gastos del usuario (puede filtrarse)
final expensesProvider =
    StateNotifierProvider<ExpensesNotifier, AsyncValue<List<Expense>>>((ref) {
  final api = ref.watch(apiClientProvider);
  return ExpensesNotifier(api);
});

class ExpensesNotifier extends StateNotifier<AsyncValue<List<Expense>>> {
  final ApiClient _api;

  ExpensesNotifier(this._api) : super(const AsyncValue.loading());

  /// Cargar gastos con filtros opcionales
  Future<void> load({
    String? startDate,
    String? endDate,
    int? categoryId,
  }) async {
    state = const AsyncValue.loading();

    try {
      final params = <String, String>{};
      if (startDate != null) params['start_date'] = startDate;
      if (endDate != null) params['end_date'] = endDate;
      if (categoryId != null) params['category_id'] = categoryId.toString();

      final data = await _api.get('/expenses', queryParams: params) as List;
      final expenses = data.map((e) => Expense.fromJson(e)).toList();
      state = AsyncValue.data(expenses);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  /// UC-02: Crear gasto nuevo
  Future<bool> create({
    required double amount,
    required String description,
    required String expenseDate,
    required int categoryId,
  }) async {
    try {
      await _api.post('/expenses', body: {
        'amount': amount,
        'description': description,
        'expense_date': expenseDate,
        'category_id': categoryId,
      });
      await load(); // Recargar lista tras crear
      return true;
    } on ApiException {
      return false;
    }
  }
}
