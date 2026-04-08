/// Bottom sheet para crear presupuesto. Ref: Solution Design, UC-03 Create Monthly Budget.
/// Campos: category selector, limit amount. Mes/anio = actual.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../constants/style.dart';
import '../../../model/category.dart';
import '../../../providers/budgets_provider.dart';
import '../../../providers/categories_provider.dart';
import '../../../providers/dashboard_provider.dart';
import '../../../ui/device.dart';

class CreateBudgetSheet extends ConsumerStatefulWidget {
  const CreateBudgetSheet({super.key});

  @override
  ConsumerState<CreateBudgetSheet> createState() => _CreateBudgetSheetState();
}

class _CreateBudgetSheetState extends ConsumerState<CreateBudgetSheet> {
  final _formKey = GlobalKey<FormState>();
  final _amountCtrl = TextEditingController();
  int? _categoryId;

  @override
  void dispose() {
    _amountCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate() || _categoryId == null) return;

    final now = DateTime.now();
    final success = await ref.read(budgetsProvider.notifier).create(
          categoryId: _categoryId!,
          limitAmount: double.parse(_amountCtrl.text),
          month: now.month,
          year: now.year,
        );

    if (success && mounted) {
      ref.read(dashboardProvider.notifier).load();
      Navigator.of(context).pop();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Budget created')),
      );
    } else if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
            content: Text('Budget already exists for this category')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final categories = ref.watch(categoriesProvider);

    return Padding(
      padding: EdgeInsets.only(
        left: Sizes.xl,
        right: Sizes.xl,
        top: Sizes.xl,
        bottom: MediaQuery.of(context).viewInsets.bottom + Sizes.xl,
      ),
      child: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text('Create budget',
                  style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: Sizes.lg),

              // Category selector
              Text('Select category',
                  style: Theme.of(context).textTheme.titleSmall),
              const SizedBox(height: Sizes.sm),
              categories.when(
                loading: () =>
                    const Center(child: CircularProgressIndicator()),
                error: (err, _) => Text('Error: $err'),
                data: (cats) => Wrap(
                  spacing: Sizes.sm,
                  runSpacing: Sizes.sm,
                  children: cats.map((c) => _categoryChip(c)).toList(),
                ),
              ),
              const SizedBox(height: Sizes.lg),

              // Spending limit
              TextFormField(
                controller: _amountCtrl,
                decoration: const InputDecoration(
                  hintText: 'Monthly spending limit',
                  prefixText: '\$ ',
                ),
                keyboardType:
                    const TextInputType.numberWithOptions(decimal: true),
                validator: (v) {
                  if (v == null || v.isEmpty) return 'Required';
                  final n = double.tryParse(v);
                  if (n == null || n <= 0) return 'Must be greater than 0';
                  return null;
                },
              ),
              const SizedBox(height: Sizes.xl),

              // Submit
              ElevatedButton(
                onPressed: _categoryId != null ? _submit : null,
                child: const Text('Save budget'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _categoryChip(Category cat) {
    final selected = _categoryId == cat.categoryId;
    final color = categoryColors[cat.categoryId] ?? grey2;

    return ChoiceChip(
      label: Text(cat.name),
      selected: selected,
      selectedColor: color.withValues(alpha: 0.3),
      backgroundColor: grey3,
      labelStyle: TextStyle(
        color: selected ? primary : grey1,
        fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
      ),
      avatar: Icon(
        categoryIcons[cat.categoryId] ?? Icons.category,
        size: 18,
        color: color,
      ),
      onSelected: (_) => setState(() => _categoryId = cat.categoryId),
    );
  }
}
