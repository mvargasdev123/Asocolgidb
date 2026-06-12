import 'package:go_router/go_router.dart';

import '../../features/persons/presentation/pages/person_list_page.dart';
import '../../features/persons/presentation/pages/person_create_page.dart';
import '../../features/persons/presentation/pages/person_detail_page.dart';

/// Configurador principal de las rutas (navegación) de la app.
/// Usamos GoRouter porque es declarativo y amigable con la web.
final GoRouter appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const PersonListPage(),
    ),
    GoRoute(
      path: '/create',
      builder: (context, state) => const PersonCreatePage(),
    ),
    GoRoute(
      path: '/person/:id',
      builder: (context, state) {
        // Extraemos el ID de la URL
        final idStr = state.pathParameters['id'];
        final personId = int.tryParse(idStr ?? '0') ?? 0;
        return PersonDetailPage(personId: personId);
      },
    ),
  ],
);
