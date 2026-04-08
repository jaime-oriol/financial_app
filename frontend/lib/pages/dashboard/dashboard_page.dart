/// Dashboard / Home. Ref: Solution Design, UC-05, wireframe 2.
/// Muestra: savings total, budget %, recent transactions, spending by category.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../constants/style.dart';
import '../../providers/dashboard_provider.dart';
import '../../ui/device.dart';
import '../../ui/widgets/default_container.dart';

class DashboardPage extends ConsumerStatefulWidget {
  const DashboardPage({super.key});

  @override
  ConsumerState<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends ConsumerState<DashboardPage> {
  @override
  void initState() {
    super.initState();
    // Cargar datos del dashboard al montar
    Future.microtask(() => ref.read(dashboardProvider.notifier).load());
  }

  @override
  Widget build(BuildContext context) {
    final dashboard = ref.watch(dashboardProvider);

    return dashboard.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, _) => Center(child: Text('Error: $err')),
      data: (data) => RefreshIndicator(
        onRefresh: () => ref.read(dashboardProvider.notifier).load(),
        child: ListView(
          padding: const EdgeInsets.all(Sizes.lg),
          children: [
            // Total gastado este mes
            DefaultContainer(
              margin: EdgeInsets.zero,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'This month',
                    style: Theme.of(context)
                        .textTheme
                        .labelLarge
                        ?.copyWith(color: grey1),
                  ),
                  const SizedBox(height: Sizes.xs),
                  Text(
                    '\$${_totalSpent(data.spendingByCategory).toStringAsFixed(2)}',
                    style: Theme.of(context).textTheme.displayMedium,
                  ),
                ],
              ),
            ),
            const SizedBox(height: Sizes.lg),

            // Spending por categoria
            if (data.spendingByCategory.isNotEmpty) ...[
              Text(
                'Spending by category',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: Sizes.sm),
              ...data.spendingByCategory.map((s) => Padding(
                    padding: const EdgeInsets.only(bottom: Sizes.sm),
                    child: DefaultContainer(
                      margin: EdgeInsets.zero,
                      child: Row(
                        children: [
                          Icon(
                            categoryIcons[s.categoryId] ?? Icons.category,
                            color: categoryColors[s.categoryId] ?? grey1,
                          ),
                          const SizedBox(width: Sizes.md),
                          Expanded(
                            child: Text(s.categoryName,
                                style:
                                    Theme.of(context).textTheme.titleSmall),
                          ),
                          Text(
                            '\$${s.total.toStringAsFixed(2)}',
                            style: Theme.of(context)
                                .textTheme
                                .titleSmall
                                ?.copyWith(fontWeight: FontWeight.w700),
                          ),
                        ],
                      ),
                    ),
                  )),
              const SizedBox(height: Sizes.lg),
            ],

            // Presupuestos con progreso
            if (data.budgets.isNotEmpty) ...[
              Text(
                'Budget progress',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: Sizes.sm),
              ...data.budgets.map((b) => Padding(
                    padding: const EdgeInsets.only(bottom: Sizes.sm),
                    child: DefaultContainer(
                      margin: EdgeInsets.zero,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(b.categoryName ?? 'Category',
                                  style: Theme.of(context)
                                      .textTheme
                                      .titleSmall),
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
                              color: b.progress > 100 ? error : secondary,
                              minHeight: 8,
                            ),
                          ),
                        ],
                      ),
                    ),
                  )),
              const SizedBox(height: Sizes.lg),
            ],

            // Transacciones recientes
            Text(
              'Recent transactions',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: Sizes.sm),
            if (data.recentTransactions.isEmpty)
              DefaultContainer(
                margin: EdgeInsets.zero,
                child: Text(
                  'No expenses yet. Add one to get started!',
                  style: Theme.of(context)
                      .textTheme
                      .bodySmall
                      ?.copyWith(color: grey1, fontStyle: FontStyle.italic),
                ),
              )
            else
              DefaultContainer(
                margin: EdgeInsets.zero,
                padding: EdgeInsets.zero,
                child: ListView.separated(
                  physics: const NeverScrollableScrollPhysics(),
                  shrinkWrap: true,
                  itemCount: data.recentTransactions.length,
                  separatorBuilder: (_, __) => const Divider(height: 1),
                  itemBuilder: (context, index) {
                    final e = data.recentTransactions[index];
                    return ListTile(
                      leading: CircleAvatar(
                        backgroundColor:
                            categoryColors[e.categoryId]?.withValues(alpha: 0.2) ??
                                grey3,
                        child: Icon(
                          categoryIcons[e.categoryId] ?? Icons.category,
                          color: categoryColors[e.categoryId] ?? grey1,
                          size: 20,
                        ),
                      ),
                      title: Text(e.description,
                          overflow: TextOverflow.ellipsis),
                      subtitle: Text(e.categoryName ?? ''),
                      trailing: Text(
                        '-\$${e.amount.toStringAsFixed(2)}',
                        style: const TextStyle(
                          color: error,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    );
                  },
                ),
              ),
          ],
        ),
      ),
    );
  }

  double _totalSpent(List spendingByCategory) {
    double total = 0;
    for (final s in spendingByCategory) {
      total += s.total;
    }
    return total;
  }
}
