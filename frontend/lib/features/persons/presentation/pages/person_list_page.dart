import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../domain/entities/person.dart';
import '../providers/person_list_provider.dart';
import '../widgets/person_card.dart';

class PersonListPage extends ConsumerWidget {
  const PersonListPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // 1. Observamos la lista filtrada, no la original.
    final asyncPersons = ref.watch(filteredPersonListProvider);
    
    // 2. Observamos los valores de los filtros para dibujar la UI.
    final currentRoleFilter = ref.watch(roleFilterProvider);

    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA), // Fondo profesional limpio
      appBar: AppBar(
        title: const Text('Directorio Asocolgi', style: TextStyle(fontWeight: FontWeight.bold)),
        centerTitle: true,
        backgroundColor: Colors.white,
        surfaceTintColor: Colors.white,
        elevation: 0.5,
      ),
      body: Column(
        children: [
          // ---- SECCIÓN DE BUSCADOR Y FILTROS ----
          Container(
            padding: const EdgeInsets.all(16.0),
            color: Colors.white,
            child: Column(
              children: [
                // Barra de búsqueda elegante
                TextField(
                  onChanged: (value) => ref.read(searchQueryProvider.notifier).state = value,
                  decoration: InputDecoration(
                    hintText: 'Buscar por nombre...',
                    prefixIcon: const Icon(Icons.search, color: Colors.teal),
                    filled: true,
                    fillColor: Colors.grey.shade100,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                    contentPadding: const EdgeInsets.symmetric(vertical: 0),
                  ),
                ),
                const SizedBox(height: 12),
                
                // Chips de Filtro horizontales
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      _buildFilterChip(context, ref, 'Todos', null, currentRoleFilter),
                      const SizedBox(width: 8),
                      _buildFilterChip(context, ref, 'Contratados', PersonRole.contratado, currentRoleFilter),
                      const SizedBox(width: 8),
                      _buildFilterChip(context, ref, 'Asociados', PersonRole.asociado, currentRoleFilter),
                      const SizedBox(width: 8),
                      _buildFilterChip(context, ref, 'Voluntarios', PersonRole.voluntario, currentRoleFilter),
                    ],
                  ),
                ),
              ],
            ),
          ),
          
          // ---- LISTA DE RESULTADOS ----
          Expanded(
            child: asyncPersons.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (error, stack) => Center(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.error_outline, color: Colors.redAccent, size: 48),
                      const SizedBox(height: 16),
                      const Text('No se pudo conectar al servidor.', style: TextStyle(fontWeight: FontWeight.bold)),
                      Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: Colors.grey)),
                    ],
                  ),
                ),
              ),
              data: (persons) {
                if (persons.isEmpty) {
                  return const Center(
                    child: Text('No hay personas que coincidan con la búsqueda.', style: TextStyle(color: Colors.grey)),
                  );
                }
                
                return ListView.builder(
                  padding: const EdgeInsets.only(top: 8, bottom: 80), // Margen inferior para el FAB
                  itemCount: persons.length,
                  itemBuilder: (context, index) {
                    return PersonCard(person: persons[index]);
                  },
                );
              },
            ),
          ),
        ],
      ),
      
      // ---- BOTÓN FLOTANTE (FAB) ----
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.push('/create'),
        icon: const Icon(Icons.person_add_alt_1),
        label: const Text('Registrar'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
      ),
    );
  }

  /// Función auxiliar para crear los chips de filtrado.
  Widget _buildFilterChip(BuildContext context, WidgetRef ref, String label, PersonRole? role, PersonRole? currentFilter) {
    final isSelected = role == currentFilter;
    return ChoiceChip(
      label: Text(label),
      selected: isSelected,
      onSelected: (selected) {
        // Actualizamos el proveedor de filtro
        ref.read(roleFilterProvider.notifier).state = role;
      },
      selectedColor: Colors.teal.shade100,
      labelStyle: TextStyle(
        color: isSelected ? Colors.teal.shade900 : Colors.black87,
        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
      ),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
    );
  }
}
