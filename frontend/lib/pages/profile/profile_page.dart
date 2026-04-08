/// Perfil de usuario: info basica, stats, logout.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../constants/style.dart';
import '../../providers/auth_provider.dart';
import '../../ui/device.dart';
import '../../ui/widgets/default_container.dart';

class ProfilePage extends ConsumerWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ListView(
      padding: const EdgeInsets.all(Sizes.lg),
      children: [
        // Avatar y nombre
        const SizedBox(height: Sizes.lg),
        const CircleAvatar(
          radius: 45,
          backgroundColor: grey3,
          child: Icon(Icons.person, size: 50, color: grey2),
        ),
        const SizedBox(height: Sizes.md),
        Text(
          'My Profile',
          textAlign: TextAlign.center,
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: Sizes.xxl),

        // Stats mock
        Row(
          children: [
            Expanded(child: _statCard(context, '7', 'Day streak')),
            const SizedBox(width: Sizes.sm),
            Expanded(child: _statCard(context, '120', 'XP earned')),
            const SizedBox(width: Sizes.sm),
            Expanded(child: _statCard(context, '2', 'Badges')),
          ],
        ),
        const SizedBox(height: Sizes.xxl),

        // Settings items
        DefaultContainer(
          margin: EdgeInsets.zero,
          padding: EdgeInsets.zero,
          child: Column(
            children: [
              _settingsTile(context, Icons.notifications_outlined, 'Notifications'),
              const Divider(height: 1),
              _settingsTile(context, Icons.language, 'Language'),
              const Divider(height: 1),
              _settingsTile(context, Icons.info_outline, 'About'),
            ],
          ),
        ),
        const SizedBox(height: Sizes.xxl),

        // Logout
        ElevatedButton(
          onPressed: () async {
            await ref.read(authStateProvider.notifier).logout();
            if (context.mounted) {
              Navigator.of(context).pushReplacementNamed('/login');
            }
          },
          style: ElevatedButton.styleFrom(backgroundColor: error),
          child: const Text('Log out'),
        ),
      ],
    );
  }

  Widget _statCard(BuildContext context, String value, String label) {
    return DefaultContainer(
      margin: EdgeInsets.zero,
      child: Column(
        children: [
          Text(value, style: Theme.of(context).textTheme.headlineMedium),
          const SizedBox(height: Sizes.xs),
          Text(label,
              style: Theme.of(context)
                  .textTheme
                  .labelLarge
                  ?.copyWith(color: grey1)),
        ],
      ),
    );
  }

  Widget _settingsTile(BuildContext context, IconData icon, String title) {
    return ListTile(
      leading: Icon(icon, color: secondary),
      title: Text(title, style: Theme.of(context).textTheme.titleSmall),
      trailing: const Icon(Icons.chevron_right, color: grey2),
      onTap: () {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('$title — coming soon')),
        );
      },
    );
  }
}
