/// Bottom sheet para anadir un gasto. Ref: Solution Design, UC-02 Add Expense.
/// Campos: amount, description, date, category selector.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../constants/style.dart';
import '../../../providers/categories_provider.dart';
import '../../../ui/widgets/category_chip.dart';
import '../../../providers/dashboard_provider.dart';
import '../../../providers/expenses_provider.dart';
import '../../../ui/device.dart';

class AddExpenseSheet extends ConsumerStatefulWidget {
  const AddExpenseSheet({super.key});

  @override
  ConsumerState<AddExpenseSheet> createState() => _AddExpenseSheetState();
}

class _AddExpenseSheetState extends ConsumerState<AddExpenseSheet> {
  final _formKey = GlobalKey<FormState>();
  final _amountCtrl = TextEditingController();
  final _descCtrl = TextEditingController();
  DateTime _date = DateTime.now();
  int? _categoryId;

  @override
  void dispose() {
    _amountCtrl.dispose();
    _descCtrl.dispose();
    super.dispose();
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _date,
      firstDate: DateTime(2020),
      lastDate: DateTime.now(),
    );
    if (picked != null) setState(() => _date = picked);
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate() || _categoryId == null) return;

    final success = await ref.read(expensesProvider.notifier).create(
          amount: double.parse(_amountCtrl.text),
          description: _descCtrl.text.trim().isEmpty
              ? 'No description'
              : _descCtrl.text.trim(),
          expenseDate: _date.toIso8601String().split('T').first,
          categoryId: _categoryId!,
        );

    if (success && mounted) {
      // Recargar dashboard tras crear gasto
      ref.read(dashboardProvider.notifier).load();
      Navigator.of(context).pop();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Expense added')),
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
              Text('Add expense',
                  style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: Sizes.lg),

              // Amount
              TextFormField(
                controller: _amountCtrl,
                decoration: const InputDecoration(
                  hintText: 'Amount',
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
              const SizedBox(height: Sizes.md),

              // Description
              TextFormField(
                controller: _descCtrl,
                decoration:
                    const InputDecoration(hintText: 'Description (optional)'),
              ),
              const SizedBox(height: Sizes.md),

              // Date picker
              GestureDetector(
                onTap: _pickDate,
                child: Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: Sizes.lg, vertical: Sizes.md),
                  decoration: BoxDecoration(
                    color: grey3,
                    borderRadius: BorderRadius.circular(Sizes.borderRadius),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.calendar_today, size: 18, color: grey1),
                      const SizedBox(width: Sizes.sm),
                      Text(
                        '${_date.day}/${_date.month}/${_date.year}',
                        style: const TextStyle(fontSize: 16),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: Sizes.md),

              // Category selector
              Text('Category',
                  style: Theme.of(context).textTheme.titleSmall),
              const SizedBox(height: Sizes.sm),
              categories.when(
                loading: () =>
                    const Center(child: CircularProgressIndicator()),
                error: (err, _) => Text('Error: $err'),
                data: (cats) => Wrap(
                  spacing: Sizes.sm,
                  runSpacing: Sizes.sm,
                  children: cats
                      .map((c) => CategoryChip(
                            category: c,
                            selected: _categoryId == c.categoryId,
                            onSelected: () =>
                                setState(() => _categoryId = c.categoryId),
                          ))
                      .toList(),
                ),
              ),
              const SizedBox(height: Sizes.xl),

              // Submit
              ElevatedButton(
                onPressed: _categoryId != null ? _submit : null,
                child: const Text('Save expense'),
              ),
            ],
          ),
        ),
      ),
    );
  }

}
