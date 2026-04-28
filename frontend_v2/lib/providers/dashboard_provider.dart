/// Provider del dashboard: resumen financiero del mes actual.
/// Ref: Solution Design, UC-05 View Dashboard / Simple Analytics.
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../model/dashboard.dart';
import '../services/api_client.dart';
import 'auth_provider.dart';

/// Datos del dashboard (spending, budgets, recent transactions)
final dashboardProvider =
    StateNotifierProvider<DashboardNotifier, AsyncValue<Dashboard>>((ref) {
  final api = ref.watch(apiClientProvider);
  return DashboardNotifier(api);
});

class DashboardNotifier extends StateNotifier<AsyncValue<Dashboard>> {
  final ApiClient _api;

  DashboardNotifier(this._api) : super(const AsyncValue.loading());

  /// Cargar datos del dashboard desde GET /api/dashboard
  Future<void> load() async {
    state = const AsyncValue.loading();

    try {
      final data = await _api.get('/dashboard');
      state = AsyncValue.data(Dashboard.fromJson(data));
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}
