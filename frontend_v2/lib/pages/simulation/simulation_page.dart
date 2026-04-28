/// Financial Simulation page. Ref: Solution Design, wireframe 6.
/// Scenario: $200 split, choices risky/smart/not ideal, outcome card with feedback.
import 'package:flutter/material.dart';

import '../../constants/style.dart';
import '../../ui/device.dart';
import '../../ui/widgets/default_container.dart';

// Datos mock del escenario
const _scenario = {
  'title': 'Smart spending',
  'description':
      'You received \$200 this month from your part-time job. You need to cover essentials AND save for your headphone goal.',
  'budget': 200.0,
  'categories': 'Rent + Food',
};

const _choices = [
  {
    'label': 'Spend it all, enjoy now',
    'split': '\$120 fun · \$80 food · \$0 savings',
    'tag': 'Risky',
    'tagColor': 0xFFEF5350,
    'outcome':
        'You had a great weekend but now you\'re broke until next paycheck. Your headphone goal is delayed by another month.',
    'savings': 0.0,
  },
  {
    'label': 'Balance spending and saving',
    'split': '\$50 fun · \$80 food · \$70 savings',
    'tag': 'Smart',
    'tagColor': 0xFF00D9A6,
    'outcome':
        'You covered your needs, had some fun, AND put \$70 toward your headphones. At this rate you\'ll reach your goal in 2 months!',
    'savings': 70.0,
  },
  {
    'label': 'Save everything, skip fun',
    'split': '\$0 fun · \$80 food · \$120 savings',
    'tag': 'Not ideal',
    'tagColor': 0xFFFFB74D,
    'outcome':
        'You\'ll reach your goal faster, but completely skipping fun isn\'t sustainable. Balance is key to building lasting habits.',
    'savings': 120.0,
  },
];

class SimulationPage extends StatefulWidget {
  const SimulationPage({super.key});

  @override
  State<SimulationPage> createState() => _SimulationPageState();
}

class _SimulationPageState extends State<SimulationPage> {
  int? _selectedChoice;
  bool _showOutcome = false;

  void _selectChoice(int index) {
    if (_showOutcome) return;
    setState(() {
      _selectedChoice = index;
    });
  }

  void _confirm() {
    if (_selectedChoice == null) return;
    setState(() => _showOutcome = true);
  }

  void _reset() {
    setState(() {
      _selectedChoice = null;
      _showOutcome = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Simulation'),
        actions: [
          if (_showOutcome)
            Padding(
              padding: const EdgeInsets.only(right: Sizes.lg),
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: Sizes.sm, vertical: Sizes.xs),
                  decoration: BoxDecoration(
                    color: secondary,
                    borderRadius: BorderRadius.circular(Sizes.borderRadius),
                  ),
                  child: Text(
                    'Challenge',
                    style: Theme.of(context)
                        .textTheme
                        .labelLarge
                        ?.copyWith(color: white),
                  ),
                ),
              ),
            ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(Sizes.lg),
        children: [
          // Scenario card
          DefaultContainer(
            margin: EdgeInsets.zero,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
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
                      child: Text(
                        _scenario['title'] as String,
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: Sizes.md),
                Text(
                  _scenario['description'] as String,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
                const SizedBox(height: Sizes.md),
                Container(
                  padding: const EdgeInsets.all(Sizes.md),
                  decoration: BoxDecoration(
                    color: grey3,
                    borderRadius: BorderRadius.circular(Sizes.borderRadiusSmall),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text('Available',
                          style: Theme.of(context).textTheme.bodySmall),
                      Text(
                        '\$${(_scenario['budget'] as double).toStringAsFixed(0)}',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      Text(_scenario['categories'] as String,
                          style: Theme.of(context)
                              .textTheme
                              .bodySmall
                              ?.copyWith(color: grey1)),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: Sizes.lg),

          // Title
          Text(
            _showOutcome ? 'Outcome' : 'How do you split it?',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: Sizes.sm),

          // Show outcome or choices
          if (_showOutcome) ...[
            _buildOutcomeCard(context),
          ] else ...[
            // Choices
            ...List.generate(_choices.length, (i) {
              final c = _choices[i];
              final isSelected = _selectedChoice == i;
              final tagColor = Color(c['tagColor'] as int);

              return Padding(
                padding: const EdgeInsets.only(bottom: Sizes.sm),
                child: GestureDetector(
                  onTap: () => _selectChoice(i),
                  child: Container(
                    padding: const EdgeInsets.all(Sizes.lg),
                    decoration: BoxDecoration(
                      color: white,
                      border: Border.all(
                        color: isSelected ? tagColor : Colors.transparent,
                        width: 2,
                      ),
                      borderRadius: BorderRadius.circular(Sizes.borderRadius),
                      boxShadow: [defaultShadow],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Expanded(
                              child: Text(
                                c['label'] as String,
                                style: Theme.of(context).textTheme.titleSmall,
                              ),
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: Sizes.sm, vertical: Sizes.xs),
                              decoration: BoxDecoration(
                                color: tagColor.withValues(alpha: 0.2),
                                borderRadius:
                                    BorderRadius.circular(Sizes.borderRadius),
                              ),
                              child: Text(
                                c['tag'] as String,
                                style: Theme.of(context)
                                    .textTheme
                                    .labelLarge
                                    ?.copyWith(color: tagColor),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: Sizes.xs),
                        Text(
                          c['split'] as String,
                          style: Theme.of(context)
                              .textTheme
                              .bodySmall
                              ?.copyWith(color: grey1),
                        ),
                      ],
                    ),
                  ),
                ),
              );
            }),
            const SizedBox(height: Sizes.md),
            ElevatedButton(
              onPressed: _selectedChoice != null ? _confirm : null,
              child: const Text('See what happens'),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildOutcomeCard(BuildContext context) {
    final c = _choices[_selectedChoice!];
    final tagColor = Color(c['tagColor'] as int);
    final savings = c['savings'] as double;

    return DefaultContainer(
      margin: EdgeInsets.zero,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Choice recap
          Row(
            children: [
              Icon(
                savings >= 70 ? Icons.check_circle : Icons.warning_amber,
                color: tagColor,
              ),
              const SizedBox(width: Sizes.sm),
              Text(
                c['tag'] as String,
                style: Theme.of(context)
                    .textTheme
                    .titleMedium
                    ?.copyWith(color: tagColor),
              ),
            ],
          ),
          const SizedBox(height: Sizes.md),
          Text(
            c['outcome'] as String,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: Sizes.lg),

          // Savings result
          Container(
            padding: const EdgeInsets.all(Sizes.md),
            decoration: BoxDecoration(
              color: tagColor.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(Sizes.borderRadiusSmall),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Savings this month',
                    style: Theme.of(context).textTheme.bodySmall),
                Text(
                  '\$${savings.toStringAsFixed(0)}',
                  style: Theme.of(context)
                      .textTheme
                      .titleLarge
                      ?.copyWith(color: tagColor),
                ),
              ],
            ),
          ),
          const SizedBox(height: Sizes.lg),
          Row(
            children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: _reset,
                  style: OutlinedButton.styleFrom(
                    foregroundColor: secondary,
                    side: const BorderSide(color: secondary),
                  ),
                  child: const Text('Try again'),
                ),
              ),
              const SizedBox(width: Sizes.sm),
              Expanded(
                child: ElevatedButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text('Back to lessons'),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
