import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/entities/person.dart';
import 'person_dependency_providers.dart';

/// ---- ESTADO DEL BUSCADOR Y FILTROS ----
/// Guarda el texto que el usuario escribe en la barra de búsqueda.
final searchQueryProvider = StateProvider<String>((ref) => '');

/// Guarda el filtro de rol seleccionado (null = Todos).
final roleFilterProvider = StateProvider<PersonRole?>((ref) => null);

/// ---- CEREBRO PRINCIPAL (FUENTE DE VERDAD) ----
class PersonListNotifier extends StateNotifier<AsyncValue<List<PersonEntity>>> {
  final ref;

  PersonListNotifier(this.ref) : super(const AsyncValue.loading()) {
    fetchPersons();
  }

  Future<void> fetchPersons() async {
    state = const AsyncValue.loading();
    try {
      final repository = ref.read(personRepositoryProvider);
      final List<PersonEntity> persons = await repository.getPersons();
      state = AsyncValue.data(persons);
    } catch (e, stackTrace) {
      state = AsyncValue.error(e, stackTrace);
    }
  }

  Future<void> createPerson(PersonCreateEntity person) async {
    try {
      final repository = ref.read(personRepositoryProvider);
      
      // 1. Crear a la persona en la base de datos (Backend)
      final createdPerson = await repository.createPerson(person);
      
      // 2. Si el rol deseado no es el por defecto (Externo), lo ascendemos automáticamente
      if (person.role != PersonRole.externo) {
        await repository.changePersonRole(createdPerson.id, person.role);
      }
      
      // 3. Recargamos la lista
      await fetchPersons();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> deletePerson(int personId) async {
    try {
      final repository = ref.read(personRepositoryProvider);
      await repository.deletePerson(personId);
      await fetchPersons(); // Recargamos lista
    } catch (e) {
      rethrow;
    }
  }

  Future<void> changeRole(int personId, PersonRole newRole) async {
    try {
      final repository = ref.read(personRepositoryProvider);
      await repository.changePersonRole(personId, newRole);
      await fetchPersons();
    } catch (e) {
      rethrow;
    }
  }
}

final personListProvider = StateNotifierProvider<PersonListNotifier, AsyncValue<List<PersonEntity>>>((ref) {
  return PersonListNotifier(ref);
});

/// ---- CEREBRO CALCULADO (LISTA FILTRADA) ----
/// Este Provider observa a los 3 (la lista de personas, el buscador y el filtro)
/// y cada vez que uno de ellos cambia, recalcula la lista filtrada automáticamente.
final filteredPersonListProvider = Provider<AsyncValue<List<PersonEntity>>>((ref) {
  final personsState = ref.watch(personListProvider);
  final query = ref.watch(searchQueryProvider).toLowerCase();
  final roleFilter = ref.watch(roleFilterProvider);

  // Si la lista original está cargando o en error, simplemente pasamos ese estado.
  return personsState.whenData((persons) {
    return persons.where((p) {
      // 1. Filtro por búsqueda de nombre
      final matchesQuery = p.fullName.toLowerCase().contains(query);
      
      // 2. Filtro por rol (si roleFilter es null, significa "Todos")
      final matchesRole = roleFilter == null || p.role == roleFilter;
      
      return matchesQuery && matchesRole;
    }).toList();
  });
});
