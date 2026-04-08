/// Budget Tracker. Ref: Solution Design, wireframe 3.
/// Donut chart de spending, category budget bars con progress, add expense, create budget.
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../constants/style.dart';
import '../../model/dashboard.dart';
import '../../providers/budgets_provider.dart';
import '../../providers/dashboard_provider.dart';
import '../../ui/device.dart';
import '../../ui/widgets/default_container.dart';
import 'widgets/add_expense_sheet.dart';
import 'widgets/create_budget_sheet.dart';

class BudgetPage extends ConsumerStatefulWidget {
  const BudgetPage({super.key});

  @override
  ConsumerState<BudgetPage> createState() => _BudgetPageState();
}

class _BudgetPageState extends ConsumerState<BudgetPage> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      ref.read(dashboardProvider.notifier).load();
      ref.read(budgetsProvider.notifier).load();
    });
  }

  void _showAddExpense() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(Sizes.borderRadiusLarge)),
      ),
      builder: (_) => const AddExpenseSheet(),
    );
  }

  void _showCreateBudget() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(Sizes.borderRadiusLarge)),
      ),
      builder: (_) => const CreateBudgetSheet(),
    );
  }

  @override
  Widget build(BuildContext context) {
    final dashboard = ref.watch(dashboardProvider);
    final budgets = ref.watch(budgetsProvider);

    return dashboard.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, _) => Center(child: Text('Error: $err')),
      data: (data) => RefreshIndicator(
        onRefresh: () async {
          await ref.read(dashboardProvider.notifier).load();
          await ref.read(budgetsProvider.notifier).load();
        },
        child: ListView(
          padding: const EdgeInsets.all(Sizes.lg),
          children: [
            // Donut chart de spending por categoria
            if (data.spendingByCategory.isNotEmpty) ...[
              DefaultContainer(
                margin: EdgeInsets.zero,
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Budget tracker',
                            style: Theme.of(context).textTheme.titleLarge),
                        Text(
                          '${_totalPercent(data)}%',
                          style: Theme.of(context)
                              .textTheme
                              .titleMedium
                              ?.copyWith(color: secondary),
                        ),
                      ],
                    ),
                    const SizedBox(height: Sizes.md),
                    SizedBox(
                      height: 180,
                      child: _buildDonutChart(data.spendingByCategory),
                    ),
                    const SizedBox(height: Sizes.md),
                    // Leyenda
                    Wrap(
                      spacing: Sizes.lg,
                      runSpacing: Sizes.xs,
                      children: data.spendingByCategory.map((s) {
                        return Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Container(
                              width: 10,
                              height: 10,
                              decoration: BoxDecoration(
                                color: categoryColors[s.categoryId] ?? grey2,
                                shape: BoxShape.circle,
                              ),
                            ),
                            const SizedBox(width: Sizes.xs),
                            Text(s.categoryName,
                                style: Theme.of(context).textTheme.bodySmall),
                          ],
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: Sizes.lg),
            ],

            // Category budget bars con progress
            Text('Category budgets',
                style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: Sizes.sm),
            budgets.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, _) => Text('Error: $err'),
              data: (budgetList) {
                if (budgetList.isEmpty) {
                  return DefaultContainer(
                    margin: EdgeInsets.zero,
                    child: Text(
                      'No budgets set yet. Create one to start tracking!',
                      style: Theme.of(context)
                          .textTheme
                          .bodySmall
                          ?.copyWith(color: grey1, fontStyle: FontStyle.italic),
                    ),
                  );
                }
                return Column(
                  children: budgetList.map((b) {
                    final color = categoryColors[b.categoryId] ?? grey2;
                    return Padding(
                      padding: const EdgeInsets.only(bottom: Sizes.sm),
                      child: DefaultContainer(
                        margin: EdgeInsets.zero,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Icon(
                                  categoryIcons[b.categoryId] ?? Icons.category,
                                  color: color,
                                  size: 20,
                                ),
                                const SizedBox(width: Sizes.sm),
                                Expanded(
                                  child: Text(b.categoryName ?? 'Category',
                                      style: Theme.of(context).textTheme.titleSmall),
                                ),
                                Text(
                                  '\$${b.spent.toStringAsFixed(0)} / \$${b.limitAmount.toStringAsFixed(0)}',
                                  style: Theme.of(context).textTheme.bodySmall,
                                ),
                              ],
                            ),
                            const SizedBox(height: Sizes.sm),
                            ClipRRect(
                              borderRadius:
                                  BorderRadius.circular(Sizes.borderRadiusSmall),
                              child: LinearProgressIndicator(
                                value: (b.progress / 100).clamp(0.0, 1.0),
                                backgroundColor: grey3,
                                color: b.progress > 90 ? error : color,
                                minHeight: 8,
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  }).toList(),
                );
              },
            ),
            const SizedBox(height: Sizes.lg),

            // Botones de accion
            ElevatedButton.icon(
              onPressed: _showAddExpense,
              icon: const Icon(Icons.add),
              label: const Text('Add expense'),
            ),
            const SizedBox(height: Sizes.sm),
            OutlinedButton.icon(
              onPressed: _showCreateBudget,
              icon: const Icon(Icons.pie_chart_outline),
              label: const Text('Create new budget'),
              style: OutlinedButton.styleFrom(
                foregroundColor: secondary,
                side: const BorderSide(color: secondary),
                padding: const EdgeInsets.all(Sizes.lg),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(Sizes.borderRadiusLarge),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Donut chart con fl_chart
  Widget _buildDonutChart(List<SpendingByCategory> items) {
    final total = items.fold(0.0, (sum, s) => sum + s.total);
    if (total == 0) return const SizedBox();

    return PieChart(
      PieChartData(
        sectionsSpace: 2,
        centerSpaceRadius: 50,
        sections: items.map((s) {
          final pct = (s.total / total) * 100;
          return PieChartSectionData(
            color: categoryColors[s.categoryId] ?? grey2,
            value: pct,
            title: '',
            radius: 25,
          );
        }).toList(),
      ),
    );
  }

  /// Porcentaje medio de uso de presupuestos
  String _totalPercent(Dashboard data) {
    if (data.budgets.isEmpty) return '0';
    final avg = data.budgets.fold(0.0, (sum, b) => sum + b.progress) /
        data.budgets.length;
    return avg.toStringAsFixed(0);
  }
}
