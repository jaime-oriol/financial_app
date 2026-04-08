/// Provider de categorias: carga las 6 categorias seed del backend.
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../model/category.dart';
import '../services/api_client.dart';
import 'auth_provider.dart';

/// Lista de categorias cargadas del backend
final categoriesProvider = FutureProvider<List<Category>>((ref) async {
  final api = ref.watch(apiClientProvider);
  final data = await api.get('/categories') as List;
  return data.map((e) => Category.fromJson(e)).toList();
});
