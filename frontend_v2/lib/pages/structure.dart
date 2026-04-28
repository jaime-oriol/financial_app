/// Estructura principal: scaffold con bottom navigation de 5 tabs.
/// Ref: Solution Design, wireframes — bottom nav: Home, Budget, Learn, Goals, Profile.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../constants/style.dart';
import 'budget/budget_page.dart';
import 'dashboard/dashboard_page.dart';
import 'goals/goals_page.dart';
import 'lessons/lessons_page.dart';
import 'profile/profile_page.dart';

class Structure extends ConsumerStatefulWidget {
  const Structure({super.key});

  @override
  ConsumerState<Structure> createState() => _StructureState();
}

class _StructureState extends ConsumerState<Structure> {
  final List<String> _titles = ['', 'Budget', 'Learn', 'Goals', 'Profile'];
  final List<Widget> _pages = const [
    DashboardPage(),
    BudgetPage(),
    LessonsPage(),
    GoalsPage(),
    ProfilePage(),
  ];

  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      // Dashboard tiene su propio header, las demas usan AppBar
      appBar: _selectedIndex == 0
          ? null
          : AppBar(title: Text(_titles[_selectedIndex])),
      body: _pages[_selectedIndex],
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          boxShadow: [
            BoxShadow(
              color: primary.withValues(alpha: 0.08),
              blurRadius: 8,
              offset: const Offset(0, -2),
            ),
          ],
        ),
        child: BottomNavigationBar(
          currentIndex: _selectedIndex,
          onTap: (index) => setState(() => _selectedIndex = index),
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.home_outlined),
              activeIcon: Icon(Icons.home),
              label: 'Home',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.account_balance_wallet_outlined),
              activeIcon: Icon(Icons.account_balance_wallet),
              label: 'Budget',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.menu_book_outlined),
              activeIcon: Icon(Icons.menu_book),
              label: 'Learn',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.flag_outlined),
              activeIcon: Icon(Icons.flag),
              label: 'Goals',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.person_outline),
              activeIcon: Icon(Icons.person),
              label: 'Profile',
            ),
          ],
        ),
      ),
    );
  }
}
