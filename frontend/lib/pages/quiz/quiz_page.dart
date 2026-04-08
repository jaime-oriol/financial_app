/// Quiz page. Ref: Solution Design, wireframe 5.
/// 4 opciones, feedback verde/rojo, +10 XP, score tracking.
import 'package:flutter/material.dart';

import '../../constants/style.dart';
import '../../ui/device.dart';
import '../../ui/widgets/default_container.dart';

// Datos mock de preguntas financieras
const _questions = [
  {
    'question': 'If you save \$10 every week for a year, how much will you have saved in total?',
    'options': ['\$120', '\$520', '\$480', '\$1,040'],
    'correct': 1,
    'explanation': '\$10 × 52 weeks = \$520. Small consistent savings add up over time!',
  },
  {
    'question': 'Which of the following is a "need" rather than a "want"?',
    'options': ['New sneakers', 'Movie tickets', 'School supplies', 'Video game'],
    'correct': 2,
    'explanation': 'School supplies are essential for education. The others are wants — nice to have but not necessary.',
  },
  {
    'question': 'What does a budget help you do?',
    'options': [
      'Spend more money',
      'Track and control your spending',
      'Avoid saving money',
      'Ignore your expenses',
    ],
    'correct': 1,
    'explanation': 'A budget helps you understand where your money goes and stay within your limits.',
  },
];

class QuizPage extends StatefulWidget {
  const QuizPage({super.key});

  @override
  State<QuizPage> createState() => _QuizPageState();
}

class _QuizPageState extends State<QuizPage> {
  int _currentIndex = 0;
  int? _selectedOption;
  bool _answered = false;
  int _score = 0;
  int _xp = 0;

  Map<String, dynamic> get _current => _questions[_currentIndex];
  bool get _isCorrect => _selectedOption == _current['correct'];
  bool get _isFinished => _currentIndex >= _questions.length;

  void _selectOption(int index) {
    if (_answered) return;
    setState(() {
      _selectedOption = index;
      _answered = true;
      if (_isCorrect) {
        _score++;
        _xp += 10;
      }
    });
  }

  void _next() {
    setState(() {
      _currentIndex++;
      _selectedOption = null;
      _answered = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isFinished) return _buildResults(context);

    final options = _current['options'] as List;
    final correctIdx = _current['correct'] as int;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Quiz'),
        actions: [
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
                  '${_xp} XP',
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
      body: Padding(
        padding: const EdgeInsets.all(Sizes.lg),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Progress
            Text(
              'Question ${_currentIndex + 1} of ${_questions.length}',
              style: Theme.of(context).textTheme.labelLarge?.copyWith(color: grey1),
            ),
            const SizedBox(height: Sizes.xs),
            ClipRRect(
              borderRadius: BorderRadius.circular(Sizes.borderRadiusSmall),
              child: LinearProgressIndicator(
                value: (_currentIndex + 1) / _questions.length,
                backgroundColor: grey3,
                color: secondary,
                minHeight: 6,
              ),
            ),
            const SizedBox(height: Sizes.xl),

            // Question
            DefaultContainer(
              margin: EdgeInsets.zero,
              child: Text(
                _current['question'] as String,
                style: Theme.of(context).textTheme.titleMedium,
              ),
            ),
            const SizedBox(height: Sizes.lg),

            // Options
            ...List.generate(options.length, (i) {
              Color bgColor = grey3;
              Color borderColor = Colors.transparent;
              Color textColor = primary;

              if (_answered) {
                if (i == correctIdx) {
                  bgColor = accent.withValues(alpha: 0.15);
                  borderColor = accent;
                  textColor = accent;
                } else if (i == _selectedOption && !_isCorrect) {
                  bgColor = error.withValues(alpha: 0.15);
                  borderColor = error;
                  textColor = error;
                }
              } else if (i == _selectedOption) {
                borderColor = secondary;
              }

              return Padding(
                padding: const EdgeInsets.only(bottom: Sizes.sm),
                child: GestureDetector(
                  onTap: () => _selectOption(i),
                  child: Container(
                    padding: const EdgeInsets.all(Sizes.lg),
                    decoration: BoxDecoration(
                      color: bgColor,
                      border: Border.all(color: borderColor, width: 2),
                      borderRadius: BorderRadius.circular(Sizes.borderRadius),
                    ),
                    child: Row(
                      children: [
                        Text(
                          '${String.fromCharCode(65 + i)}.',
                          style: TextStyle(
                              color: textColor, fontWeight: FontWeight.w600),
                        ),
                        const SizedBox(width: Sizes.sm),
                        Expanded(
                          child: Text(options[i] as String,
                              style: TextStyle(color: textColor)),
                        ),
                        if (_answered && i == correctIdx)
                          const Icon(Icons.check_circle, color: accent, size: 20),
                        if (_answered && i == _selectedOption && !_isCorrect)
                          const Icon(Icons.cancel, color: error, size: 20),
                      ],
                    ),
                  ),
                ),
              );
            }),

            // Explanation + Next
            if (_answered) ...[
              const SizedBox(height: Sizes.sm),
              DefaultContainer(
                margin: EdgeInsets.zero,
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(
                      _isCorrect ? Icons.lightbulb : Icons.info_outline,
                      color: _isCorrect ? accent : warning,
                      size: 20,
                    ),
                    const SizedBox(width: Sizes.sm),
                    Expanded(
                      child: Text(
                        _current['explanation'] as String,
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ),
                  ],
                ),
              ),
              const Spacer(),
              ElevatedButton(
                onPressed: _next,
                child: Text(_currentIndex < _questions.length - 1
                    ? 'Next question'
                    : 'See results'),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildResults(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Results')),
      body: Padding(
        padding: const EdgeInsets.all(Sizes.xl),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Icon(
              _score == _questions.length ? Icons.emoji_events : Icons.school,
              size: 80,
              color: _score == _questions.length ? warning : secondary,
            ),
            const SizedBox(height: Sizes.xl),
            Text(
              _score == _questions.length ? 'Perfect score!' : 'Good effort!',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.headlineLarge,
            ),
            const SizedBox(height: Sizes.md),
            Text(
              '$_score / ${_questions.length} correct',
              textAlign: TextAlign.center,
              style: Theme.of(context)
                  .textTheme
                  .titleLarge
                  ?.copyWith(color: grey1),
            ),
            const SizedBox(height: Sizes.sm),
            Text(
              '+$_xp XP earned',
              textAlign: TextAlign.center,
              style: Theme.of(context)
                  .textTheme
                  .titleMedium
                  ?.copyWith(color: secondary),
            ),
            const SizedBox(height: Sizes.xxl),
            ElevatedButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Back to lessons'),
            ),
          ],
        ),
      ),
    );
  }
}
