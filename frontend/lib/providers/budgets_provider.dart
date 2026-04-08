/// Provider de presupuestos: crear y listar con progreso.
/// Ref: Solution Design, UC-03 Create Monthly Budget.
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../model/budget.dart';
import '../services/api_client.dart';
import 'auth_provider.dart';

/// Lista de presupuestos del mes actual
final budgetsProvider =
    StateNotifierProvider<BudgetsNotifier, AsyncValue<List<Budget>>>((ref) {
  final api = ref.watch(apiClientProvider);
  return BudgetsNotifier(api);
});

class BudgetsNotifier extends StateNotifier<AsyncValue<List<Budget>>> {
  final ApiClient _api;

  BudgetsNotifier(this._api) : super(const AsyncValue.loading());

  /// Cargar presupuestos de un mes/anio (por defecto el actual)
  Future<void> load({int? month, int? year}) async {
    state = const AsyncValue.loading();

    try {
      final now = DateTime.now();
      final params = {
        'month': (month ?? now.month).toString(),
        'year': (year ?? now.year).toString(),
      };
      final data = await _api.get('/budgets', queryParams: params) as List;
      final budgets = data.map((e) => Budget.fromJson(e)).toList();
      state = AsyncValue.data(budgets);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  /// UC-03: Crear presupuesto mensual por categoria
  Future<bool> create({
    required int categoryId,
    required double limitAmount,
    required int month,
    required int year,
  }) async {
    try {
      await _api.post('/budgets', body: {
        'category_id': categoryId,
        'limit_amount': limitAmount,
        'month': month,
        'year': year,
      });
      await load(month: month, year: year); // Recargar lista tras crear
      return true;
    } on ApiException {
      return false;
    }
  }
}
