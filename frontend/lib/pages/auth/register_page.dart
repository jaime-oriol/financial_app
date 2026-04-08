/// Pantalla de registro. Ref: Solution Design, wireframe 1 (Register/Onboarding).
/// Campos: name, surname, age range, email, password. Checkbox terms.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../constants/style.dart';
import '../../providers/auth_provider.dart';
import '../../ui/device.dart';

class RegisterPage extends ConsumerStatefulWidget {
  const RegisterPage({super.key});

  @override
  ConsumerState<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends ConsumerState<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  final _nameCtrl = TextEditingController();
  final _surnameCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  DateTime? _birthdate;
  bool _acceptedTerms = false;

  @override
  void dispose() {
    _nameCtrl.dispose();
    _surnameCtrl.dispose();
    _emailCtrl.dispose();
    _passwordCtrl.dispose();
    super.dispose();
  }

  Future<void> _pickBirthdate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime(2008, 1, 1),
      firstDate: DateTime(2000),
      lastDate: DateTime.now(),
    );
    if (picked != null) setState(() => _birthdate = picked);
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    if (_birthdate == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select your birthdate')),
      );
      return;
    }
    if (!_acceptedTerms) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('You must accept the terms')),
      );
      return;
    }

    final auth = ref.read(authStateProvider.notifier);
    final success = await auth.register(
      name: _nameCtrl.text.trim(),
      surname: _surnameCtrl.text.trim(),
      birthdate: _birthdate!.toIso8601String().split('T').first,
      email: _emailCtrl.text.trim(),
      password: _passwordCtrl.text,
    );

    if (success && mounted) {
      Navigator.of(context).pushReplacementNamed('/');
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = ref.watch(authStateProvider);

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(Sizes.xl),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: Sizes.lg),
                // Logo
                Center(
                  child: Image.asset('assets/logo.png', height: 80),
                ),
                const SizedBox(height: Sizes.lg),
                // Titulo
                Text(
                  'Create your account',
                  style: Theme.of(context).textTheme.headlineLarge,
                ),
                const SizedBox(height: Sizes.sm),
                Text(
                  'Start your financial journey today',
                  style: Theme.of(context)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(color: grey1),
                ),
                const SizedBox(height: Sizes.xxl),

                // Campos del formulario
                TextFormField(
                  controller: _nameCtrl,
                  decoration: const InputDecoration(hintText: 'First name'),
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? 'Required' : null,
                ),
                const SizedBox(height: Sizes.md),
                TextFormField(
                  controller: _surnameCtrl,
                  decoration: const InputDecoration(hintText: 'Last name'),
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? 'Required' : null,
                ),
                const SizedBox(height: Sizes.md),

                // Selector de fecha de nacimiento
                GestureDetector(
                  onTap: _pickBirthdate,
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: Sizes.lg,
                      vertical: Sizes.md,
                    ),
                    decoration: BoxDecoration(
                      color: grey3,
                      borderRadius:
                          BorderRadius.circular(Sizes.borderRadius),
                    ),
                    child: Text(
                      _birthdate != null
                          ? '${_birthdate!.day}/${_birthdate!.month}/${_birthdate!.year}'
                          : 'Birthdate',
                      style: TextStyle(
                        color: _birthdate != null ? primary : grey2,
                        fontSize: 16,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: Sizes.md),

                TextFormField(
                  controller: _emailCtrl,
                  decoration: const InputDecoration(hintText: 'Email'),
                  keyboardType: TextInputType.emailAddress,
                  validator: (v) {
                    if (v == null || v.trim().isEmpty) return 'Required';
                    if (!v.contains('@')) return 'Invalid email';
                    return null;
                  },
                ),
                const SizedBox(height: Sizes.md),
                TextFormField(
                  controller: _passwordCtrl,
                  decoration: const InputDecoration(hintText: 'Password'),
                  obscureText: true,
                  validator: (v) {
                    if (v == null || v.length < 6) {
                      return 'At least 6 characters';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: Sizes.lg),

                // Checkbox de terminos
                Row(
                  children: [
                    Checkbox(
                      value: _acceptedTerms,
                      onChanged: (v) =>
                          setState(() => _acceptedTerms = v ?? false),
                      activeColor: secondary,
                    ),
                    Expanded(
                      child: Text(
                        'I agree to the Terms of Service and Privacy Policy',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: Sizes.lg),

                // Error
                if (auth.error != null)
                  Padding(
                    padding: const EdgeInsets.only(bottom: Sizes.md),
                    child: Text(
                      auth.error!,
                      style: const TextStyle(color: error, fontSize: 14),
                    ),
                  ),

                // Boton de registro
                ElevatedButton(
                  onPressed: auth.loading ? null : _submit,
                  child: auth.loading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: white,
                          ),
                        )
                      : const Text('Create account'),
                ),
                const SizedBox(height: Sizes.lg),

                // Link a login
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Already have an account? '),
                    GestureDetector(
                      onTap: () =>
                          Navigator.of(context).pushReplacementNamed('/login'),
                      child: Text(
                        'Sign in',
                        style: TextStyle(
                          color: secondary,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
