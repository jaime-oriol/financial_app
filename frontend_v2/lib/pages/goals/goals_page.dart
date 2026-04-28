/// Savings Goals page. Ref: Solution Design, wireframe 7.
/// Goal cards con progress bar, behind-pace warning, time estimate. Datos mock.
import 'package:flutter/material.dart';

import '../../constants/style.dart';
import '../../ui/device.dart';
import '../../ui/widgets/default_container.dart';

const _goals = [
  {
    'name': 'New headphones',
    'target': 150.0,
    'saved': 84.50,
    'deadline': '2026-06-30',
    'status': 'on_track',
  },
  {
    'name': 'Summer trip fund',
    'target': 500.0,
    'saved': 30.0,
    'deadline': '2026-08-15',
    'status': 'behind',
  },
];

class GoalsPage extends StatelessWidget {
  const GoalsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(Sizes.lg),
      children: [
        // Goal cards
        ...List.generate(_goals.length, (i) {
          final g = _goals[i];
          final target = g['target'] as double;
          final saved = g['saved'] as double;
          final progress = target > 0 ? (saved / target).clamp(0.0, 1.0) : 0.0;
          final isBehind = g['status'] == 'behind';

          return Padding(
            padding: const EdgeInsets.only(bottom: Sizes.lg),
            child: DefaultContainer(
              margin: EdgeInsets.zero,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Header: nombre + status badge
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(g['name'] as String,
                          style: Theme.of(context).textTheme.titleMedium),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: Sizes.sm, vertical: Sizes.xs),
                        decoration: BoxDecoration(
                          color: isBehind
                              ? warning.withValues(alpha: 0.2)
                              : accent.withValues(alpha: 0.2),
                          borderRadius:
                              BorderRadius.circular(Sizes.borderRadius),
                        ),
                        child: Text(
                          isBehind ? 'Behind' : 'On track',
                          style: Theme.of(context).textTheme.labelLarge?.copyWith(
                              color: isBehind ? warning : accent),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: Sizes.md),

                  // Monto ahorrado
                  Text(
                    '\$${saved.toStringAsFixed(2)}',
                    style: Theme.of(context).textTheme.headlineMedium,
                  ),
                  Text(
                    'of \$${target.toStringAsFixed(0)} goal',
                    style: Theme.of(context)
                        .textTheme
                        .bodySmall
                        ?.copyWith(color: grey1),
                  ),
                  const SizedBox(height: Sizes.md),

                  // Progress bar
                  ClipRRect(
                    borderRadius:
                        BorderRadius.circular(Sizes.borderRadiusSmall),
                    child: LinearProgressIndicator(
                      value: progress,
                      backgroundColor: grey3,
                      color: isBehind ? warning : accent,
                      minHeight: 10,
                    ),
                  ),
                  const SizedBox(height: Sizes.sm),

                  // Info row
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        '${(progress * 100).toStringAsFixed(0)}% saved',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                      Text(
                        'Target: ${g['deadline']}',
                        style: Theme.of(context)
                            .textTheme
                            .bodySmall
                            ?.copyWith(color: grey1),
                      ),
                    ],
                  ),

                  // Behind-pace warning
                  if (isBehind) ...[
                    const SizedBox(height: Sizes.sm),
                    Container(
                      padding: const EdgeInsets.all(Sizes.sm),
                      decoration: BoxDecoration(
                        color: warning.withValues(alpha: 0.1),
                        borderRadius:
                            BorderRadius.circular(Sizes.borderRadiusSmall),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.info_outline,
                              color: warning, size: 16),
                          const SizedBox(width: Sizes.sm),
                          Expanded(
                            child: Text(
                              'Save \$12/week to reach this goal on time',
                              style: Theme.of(context)
                                  .textTheme
                                  .bodySmall
                                  ?.copyWith(color: warning),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ],
              ),
            ),
          );
        }),

        // Add new goal button
        ElevatedButton.icon(
          onPressed: () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Coming soon!')),
            );
          },
          icon: const Icon(Icons.add),
          label: const Text('Add a new goal'),
        ),
        const SizedBox(height: Sizes.lg),

        // Tip
        DefaultContainer(
          margin: EdgeInsets.zero,
          child: Text(
            'Setting at least 2 savings goals increases your chances of building lasting money habits. You\'re on the right track!',
            style: Theme.of(context)
                .textTheme
                .bodySmall
                ?.copyWith(color: grey1, fontStyle: FontStyle.italic),
          ),
        ),
      ],
    );
  }
}
