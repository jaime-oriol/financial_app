/// Lessons / Learn page. Ref: Solution Design, wireframe 4 (Lessons).
/// Daily challenge, modulos con progreso, badges. Datos mockeados.
import 'package:flutter/material.dart';

import '../../constants/style.dart';
import '../../ui/device.dart';
import '../../ui/widgets/default_container.dart';

// Datos mock de modulos de educacion financiera
const _modules = [
  {'title': 'Budgeting basics', 'lessons': 5, 'completed': 5, 'locked': false},
  {'title': 'Needs vs. wants', 'lessons': 4, 'completed': 3, 'locked': false},
  {'title': 'Saving money', 'lessons': 6, 'completed': 0, 'locked': false},
  {'title': 'Compound interest', 'lessons': 4, 'completed': 0, 'locked': true},
  {'title': 'Smart spending', 'lessons': 5, 'completed': 0, 'locked': true},
];

const _badges = [
  {'icon': Icons.star, 'name': 'First Saver', 'earned': true},
  {'icon': Icons.local_fire_department, 'name': 'Hot Streak', 'earned': true},
  {'icon': Icons.emoji_events, 'name': 'Budget Pro', 'earned': false},
];

class LessonsPage extends StatelessWidget {
  const LessonsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(Sizes.lg),
      children: [
        // Header con nivel
        DefaultContainer(
          margin: EdgeInsets.zero,
          child: Row(
            children: [
              const Icon(Icons.school, color: secondary, size: 28),
              const SizedBox(width: Sizes.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('2 modules completed',
                        style: Theme.of(context).textTheme.titleSmall),
                    const SizedBox(height: Sizes.xs),
                    ClipRRect(
                      borderRadius:
                          BorderRadius.circular(Sizes.borderRadiusSmall),
                      child: const LinearProgressIndicator(
                        value: 0.4,
                        backgroundColor: grey3,
                        color: secondary,
                        minHeight: 6,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: Sizes.md),
              Container(
                padding: const EdgeInsets.symmetric(
                    horizontal: Sizes.sm, vertical: Sizes.xs),
                decoration: BoxDecoration(
                  color: secondary,
                  borderRadius: BorderRadius.circular(Sizes.borderRadius),
                ),
                child: Text('Level 2',
                    style: Theme.of(context)
                        .textTheme
                        .labelLarge
                        ?.copyWith(color: white)),
              ),
            ],
          ),
        ),
        const SizedBox(height: Sizes.lg),

        // Daily challenge — navega a Quiz
        Text('Daily challenge',
            style: Theme.of(context).textTheme.titleMedium),
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
                    color: warning.withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(Sizes.borderRadius),
                  ),
                  child: const Icon(Icons.quiz, color: warning),
                ),
                const SizedBox(width: Sizes.md),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Needs vs. Wants quiz',
                          style: Theme.of(context).textTheme.titleSmall),
                      Text('3 questions - Earn 30 XP',
                          style: Theme.of(context)
                              .textTheme
                              .bodySmall
                              ?.copyWith(color: grey1)),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: Sizes.sm, vertical: Sizes.xs),
                  decoration: BoxDecoration(
                    color: accent,
                    borderRadius: BorderRadius.circular(Sizes.borderRadius),
                  ),
                  child: Text('New',
                      style: Theme.of(context)
                          .textTheme
                          .labelLarge
                          ?.copyWith(color: white)),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: Sizes.sm),

        // Simulation challenge — navega a Simulation
        GestureDetector(
          onTap: () => Navigator.of(context).pushNamed('/simulation'),
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
                  child: const Icon(Icons.psychology, color: secondary),
                ),
                const SizedBox(width: Sizes.md),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Smart spending simulation',
                          style: Theme.of(context).textTheme.titleSmall),
                      Text('Split \$200 wisely',
                          style: Theme.of(context)
                              .textTheme
                              .bodySmall
                              ?.copyWith(color: grey1)),
                    ],
                  ),
                ),
                const Icon(Icons.chevron_right, color: grey2),
              ],
            ),
          ),
        ),
        const SizedBox(height: Sizes.lg),

        // Modulos
        Text('Modules', style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: Sizes.sm),
        ...List.generate(_modules.length, (i) {
          final m = _modules[i];
          final locked = m['locked'] as bool;
          final completed = m['completed'] as int;
          final total = m['lessons'] as int;
          final isDone = completed == total && total > 0;

          final moduleColor = isDone ? accent : locked ? grey2 : secondary;
          return Padding(
            padding: const EdgeInsets.only(bottom: Sizes.sm),
            child: Opacity(
              opacity: locked ? 0.45 : 1.0,
              child: Container(
                decoration: BoxDecoration(
                  color: white,
                  borderRadius: BorderRadius.circular(14),
                  boxShadow: [defaultShadow],
                ),
                child: IntrinsicHeight(
                  child: Row(
                    children: [
                      Container(
                        width: 4,
                        decoration: BoxDecoration(
                          color: moduleColor,
                          borderRadius: const BorderRadius.only(
                            topLeft: Radius.circular(14),
                            bottomLeft: Radius.circular(14),
                          ),
                        ),
                      ),
                      Expanded(
                        child: Padding(
                          padding: const EdgeInsets.all(Sizes.md),
                          child: Row(
                            children: [
                              Container(
                                width: 36,
                                height: 36,
                                decoration: BoxDecoration(
                                  color: moduleColor.withValues(alpha: 0.12),
                                  borderRadius: BorderRadius.circular(10),
                                ),
                                child: Icon(
                                  locked ? Icons.lock_outline
                                      : isDone ? Icons.check_rounded
                                      : Icons.play_arrow_rounded,
                                  color: moduleColor,
                                  size: 18,
                                ),
                              ),
                              const SizedBox(width: Sizes.md),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(m['title'] as String,
                                        style: Theme.of(context).textTheme.titleSmall),
                                    const SizedBox(height: 2),
                                    Text('$completed / $total lessons',
                                        style: Theme.of(context).textTheme.bodySmall),
                                  ],
                                ),
                              ),
                              if (isDone)
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: Sizes.sm, vertical: 3),
                                  decoration: BoxDecoration(
                                    color: accent.withValues(alpha: 0.12),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Text('Done',
                                      style: Theme.of(context)
                                          .textTheme
                                          .labelLarge
                                          ?.copyWith(color: accent)),
                                ),
                              if (!isDone && !locked)
                                const Icon(Icons.chevron_right, color: grey2, size: 20),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          );
        }),
        const SizedBox(height: Sizes.lg),

        // Badges
        Text('Earned badges', style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: Sizes.sm),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: _badges.map((b) {
            final earned = b['earned'] as bool;
            return Column(
              children: [
                CircleAvatar(
                  radius: 28,
                  backgroundColor:
                      earned ? warning.withValues(alpha: 0.2) : grey3,
                  child: Icon(
                    b['icon'] as IconData,
                    color: earned ? warning : grey2,
                    size: 28,
                  ),
                ),
                const SizedBox(height: Sizes.xs),
                Text(
                  b['name'] as String,
                  style: Theme.of(context).textTheme.labelLarge?.copyWith(
                      color: earned ? primary : grey2),
                ),
              ],
            );
          }).toList(),
        ),
      ],
    );
  }
}
