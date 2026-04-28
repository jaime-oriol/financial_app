/// Pantalla de login. Misma estetica que register.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../constants/style.dart';
import '../../providers/auth_provider.dart';
import '../../ui/device.dart';

class LoginPage extends ConsumerStatefulWidget {
  const LoginPage({super.key});

  @override
  ConsumerState<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends ConsumerState<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _emailCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passwordCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    final auth = ref.read(authStateProvider.notifier);
    final success = await auth.login(
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
      backgroundColor: white,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: Sizes.xl),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: Sizes.xxl * 2),

                Center(child: Image.asset('assets/logo.png', height: 72)),
                const SizedBox(height: Sizes.xl),

                Text('Welcome back',
                    style: Theme.of(context).textTheme.headlineLarge,
                    textAlign: TextAlign.center),
                const SizedBox(height: Sizes.xs),
                Text('Sign in to continue',
                    style: Theme.of(context)
                        .textTheme
                        .bodyMedium
                        ?.copyWith(color: grey1),
                    textAlign: TextAlign.center),
                const SizedBox(height: Sizes.xxl),

                TextFormField(
                  controller: _emailCtrl,
                  decoration: const InputDecoration(
                    hintText: 'Email',
                    prefixIcon: Icon(Icons.email_outlined, color: grey2),
                  ),
                  keyboardType: TextInputType.emailAddress,
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? 'Required' : null,
                ),
                const SizedBox(height: Sizes.md),

                TextFormField(
                  controller: _passwordCtrl,
                  decoration: const InputDecoration(
                    hintText: 'Password',
                    prefixIcon: Icon(Icons.lock_outline, color: grey2),
                  ),
                  obscureText: true,
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Required' : null,
                ),
                const SizedBox(height: Sizes.xl),

                if (auth.error != null)
                  Padding(
                    padding: const EdgeInsets.only(bottom: Sizes.sm),
                    child: Text(auth.error!,
                        style: const TextStyle(color: error, fontSize: 13)),
                  ),

                ElevatedButton(
                  onPressed: auth.loading ? null : _submit,
                  child: auth.loading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: white),
                        )
                      : const Text('Sign in'),
                ),
                const SizedBox(height: Sizes.xl),

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text("Don't have an account? ",
                        style: Theme.of(context)
                            .textTheme
                            .bodySmall
                            ?.copyWith(color: grey1)),
                    GestureDetector(
                      onTap: () => Navigator.of(context)
                          .pushReplacementNamed('/register'),
                      child: Text('Register',
                          style: TextStyle(
                              color: secondary, fontWeight: FontWeight.w600)),
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
