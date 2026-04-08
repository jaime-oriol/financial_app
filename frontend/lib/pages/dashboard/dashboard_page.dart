/// Dashboard / Home. Ref: Solution Design, wireframe 2.
/// Header oscuro con saludo + total, budget %, streak, weekly activity,
/// lesson card, recent transactions.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../constants/style.dart';
import '../../model/dashboard.dart';
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
          padding: EdgeInsets.zero,
          children: [
            _buildHeader(context, data),
            Padding(
              padding: const EdgeInsets.all(Sizes.lg),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildStatsRow(context, data),
                  const SizedBox(height: Sizes.lg),
                  _buildWeeklyActivity(context),
                  const SizedBox(height: Sizes.lg),
                  _buildLessonCard(context),
                  const SizedBox(height: Sizes.lg),
                  _buildRecentTransactions(context, data),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Header card oscuro con saludo y total del mes (wireframe: area azul oscuro)
  Widget _buildHeader(BuildContext context, Dashboard data) {
    final total = data.spendingByCategory.fold(0.0, (s, e) => s + e.total);
    final colors = data.spendingByCategory
        .map((s) => categoryColors[s.categoryId] ?? grey2)
        .toList();
    final values = data.spendingByCategory.map((s) => s.total).toList();
    final sum = values.fold(0.0, (a, b) => a + b);

    return Container(
      padding: const EdgeInsets.fromLTRB(Sizes.xl, Sizes.xl, Sizes.xl, Sizes.lg),
      decoration: const BoxDecoration(
        color: primary,
        borderRadius: BorderRadius.only(
          bottomLeft: Radius.circular(Sizes.borderRadiusLarge * 1.5),
          bottomRight: Radius.circular(Sizes.borderRadiusLarge * 1.5),
        ),
      ),
      child: SafeArea(
        bottom: false,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Saludo
            Text(
              'Good morning!',
              style: Theme.of(context)
                  .textTheme
                  .bodyMedium
                  ?.copyWith(color: grey2),
            ),
            const SizedBox(height: Sizes.xs),

            // Label
            Text(
              'Total spending this month',
              style: Theme.of(context)
                  .textTheme
                  .labelLarge
                  ?.copyWith(color: Colors.white70),
            ),
            const SizedBox(height: Sizes.xs),

            // Monto grande
            Text(
              '\$${total.toStringAsFixed(2)}',
              style: Theme.of(context).textTheme.displayLarge?.copyWith(
                    color: white,
                    fontWeight: FontWeight.w800,
                  ),
            ),
            const SizedBox(height: Sizes.md),

            // Barra de colores segmentada (como en el wireframe)
            if (sum > 0)
              ClipRRect(
                borderRadius: BorderRadius.circular(Sizes.borderRadiusSmall),
                child: SizedBox(
                  height: 8,
                  child: Row(
                    children: List.generate(colors.length, (i) {
                      return Expanded(
                        flex: (values[i] / sum * 100).round().clamp(1, 100),
                        child: Container(color: colors[i]),
                      );
                    }),
                  ),
                ),
              ),
            if (sum > 0) const SizedBox(height: Sizes.sm),

            // Leyenda inline
            if (sum > 0)
              Wrap(
                spacing: Sizes.md,
                children: data.spendingByCategory.map((s) {
                  return Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Container(
                        width: 8,
                        height: 8,
                        decoration: BoxDecoration(
                          color: categoryColors[s.categoryId] ?? grey2,
                          shape: BoxShape.circle,
                        ),
                      ),
                      const SizedBox(width: Sizes.xs),
                      Text(
                        '${s.categoryName} \$${s.total.toStringAsFixed(0)}',
                        style: Theme.of(context)
                            .textTheme
                            .labelMedium
                            ?.copyWith(color: Colors.white70),
                      ),
                    ],
                  );
                }).toList(),
              ),
          ],
        ),
      ),
    );
  }

  /// Budget % y Streak side by side (wireframe: dos cards pequenas)
  Widget _buildStatsRow(BuildContext context, Dashboard data) {
    final budgetPct = data.budgets.isEmpty
        ? 0.0
        : data.budgets.fold(0.0, (s, b) => s + b.progress) /
            data.budgets.length;

    return Row(
      children: [
        Expanded(
          child: DefaultContainer(
            margin: EdgeInsets.zero,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Budget used',
                    style: Theme.of(context)
                        .textTheme
                        .labelLarge
                        ?.copyWith(color: grey1)),
                const SizedBox(height: Sizes.xs),
                Text(
                  '${budgetPct.toStringAsFixed(0)}%',
                  style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                        color: budgetPct > 90 ? error : secondary,
                        fontWeight: FontWeight.w800,
                      ),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(width: Sizes.sm),
        Expanded(
          child: DefaultContainer(
            margin: EdgeInsets.zero,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Streak',
                    style: Theme.of(context)
                        .textTheme
                        .labelLarge
                        ?.copyWith(color: grey1)),
                const SizedBox(height: Sizes.xs),
                Row(
                  children: [
                    Text(
                      '7 days',
                      style: Theme.of(context)
                          .textTheme
                          .headlineLarge
                          ?.copyWith(fontWeight: FontWeight.w800),
                    ),
                    const SizedBox(width: Sizes.xs),
                    const Icon(Icons.local_fire_department,
                        color: warning, size: 24),
                  ],
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  /// Weekly activity dots (wireframe: 7 dias con circulos coloreados)
  Widget _buildWeeklyActivity(BuildContext context) {
    final days = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
    // Mock: primeros 5 dias activos
    final active = [true, true, true, true, true, false, false];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('WEEKLY ACTIVITY',
            style: Theme.of(context)
                .textTheme
                .labelLarge
                ?.copyWith(color: grey1, letterSpacing: 1)),
        const SizedBox(height: Sizes.sm),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: List.generate(7, (i) {
            return Column(
              children: [
                Container(
                  width: 36,
                  height: 36,
                  decoration: BoxDecoration(
                    color: active[i] ? secondary : grey3,
                    shape: BoxShape.circle,
                  ),
                  child: Center(
                    child: Text(
                      days[i],
                      style: TextStyle(
                        color: active[i] ? white : grey2,
                        fontWeight: FontWeight.w600,
                        fontSize: 13,
                      ),
                    ),
                  ),
                ),
              ],
            );
          }),
        ),
      ],
    );
  }

  /// Lesson card (wireframe: card con progreso de leccion)
  Widget _buildLessonCard(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('CONTINUE LEARNING',
            style: Theme.of(context)
                .textTheme
                .labelLarge
                ?.copyWith(color: grey1, letterSpacing: 1)),
        const SizedBox(height: Sizes.sm),
        GestureDetector(
          onTap: () => Navigator.of(context).pushNamed('/quiz'),
          child: DefaultContainer(
            margin: EdgeInsets.zero,
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(Sizes.sm),
                  decoration: BoxDecoration(
                    color: secondary.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(Sizes.borderRadius),
                  ),
                  child: const Icon(Icons.menu_book, color: secondary),
                ),
                const SizedBox(width: Sizes.md),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Try compound interest',
                          style: Theme.of(context).textTheme.titleSmall),
                      const SizedBox(height: Sizes.xs),
                      ClipRRect(
                        borderRadius:
                            BorderRadius.circular(Sizes.borderRadiusSmall),
                        child: const LinearProgressIndicator(
                          value: 0.3,
                          backgroundColor: grey3,
                          color: secondary,
                          minHeight: 4,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: Sizes.sm),
                const Icon(Icons.chevron_right, color: grey2),
              ],
            ),
          ),
        ),
      ],
    );
  }

  /// Recent transactions (wireframe: lista con icono de categoria, nombre, monto rojo)
  Widget _buildRecentTransactions(BuildContext context, Dashboard data) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('RECENT TRANSACTIONS',
            style: Theme.of(context)
                .textTheme
                .labelLarge
                ?.copyWith(color: grey1, letterSpacing: 1)),
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
            padding: const EdgeInsets.symmetric(vertical: Sizes.sm),
            child: Column(
              children: List.generate(data.recentTransactions.length, (i) {
                final e = data.recentTransactions[i];
                final color = categoryColors[e.categoryId] ?? grey2;
                return Padding(
                  padding: const EdgeInsets.symmetric(
                      horizontal: Sizes.md, vertical: Sizes.sm),
                  child: Row(
                    children: [
                      // Icono con fondo de color
                      Container(
                        width: 40,
                        height: 40,
                        decoration: BoxDecoration(
                          color: color.withValues(alpha: 0.15),
                          borderRadius:
                              BorderRadius.circular(Sizes.borderRadius),
                        ),
                        child: Icon(
                          categoryIcons[e.categoryId] ?? Icons.category,
                          color: color,
                          size: 20,
                        ),
                      ),
                      const SizedBox(width: Sizes.md),
                      // Nombre y categoria
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(e.categoryName ?? '',
                                style:
                                    Theme.of(context).textTheme.titleSmall),
                            Text(e.description,
                                style: Theme.of(context)
                                    .textTheme
                                    .bodySmall
                                    ?.copyWith(color: grey1),
                                overflow: TextOverflow.ellipsis),
                          ],
                        ),
                      ),
                      // Monto en rojo
                      Text(
                        '-\$${e.amount.toStringAsFixed(2)}',
                        style: Theme.of(context)
                            .textTheme
                            .titleSmall
                            ?.copyWith(
                                color: error, fontWeight: FontWeight.w700),
                      ),
                    ],
                  ),
                );
              }),
            ),
          ),
      ],
    );
  }
}
