import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../domain/entities/person.dart';
import '../providers/person_list_provider.dart';

class PersonCard extends ConsumerWidget {
  final PersonEntity person;

  const PersonCard({super.key, required this.person});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Dismissible(
      key: Key('person_${person.id}'),
      direction: DismissDirection.endToStart, // Deslizar de derecha a izquierda
      
      // Fondo que se ve mientras se desliza la tarjeta (Fondo Rojo con icono de basura)
      background: Container(
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 20.0),
        color: Colors.redAccent,
        margin: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
        child: const Icon(Icons.delete_sweep, color: Colors.white, size: 30),
      ),
      
      // Confirmación de borrado
      confirmDismiss: (direction) async {
        return await showDialog<bool>(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text("Confirmar Eliminación"),
              content: Text("¿Estás seguro de que deseas eliminar permanentemente a ${person.fullName}?"),
              actions: [
                TextButton(
                  onPressed: () => Navigator.of(context).pop(false),
                  child: const Text("Cancelar", style: TextStyle(color: Colors.grey)),
                ),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
                  onPressed: () => Navigator.of(context).pop(true),
                  child: const Text("Eliminar", style: TextStyle(color: Colors.white)),
                ),
              ],
            );
          },
        );
      },
      
      // Acción al finalizar el borrado
      onDismissed: (direction) {
        // Llamamos a la función de eliminar en el provider
        ref.read(personListProvider.notifier).deletePerson(person.id);
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('${person.fullName} ha sido eliminado'), backgroundColor: Colors.teal),
        );
      },
      
      // La tarjeta normal
      child: Card(
        margin: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
        elevation: 1,
        color: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        child: ListTile(
          contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
          
          // Avatar estilizado
          leading: CircleAvatar(
            backgroundColor: Colors.teal.shade50,
            radius: 24,
            child: Text(
              person.fullName.substring(0, 1).toUpperCase(),
              style: TextStyle(color: Colors.teal.shade800, fontWeight: FontWeight.bold, fontSize: 20),
            ),
          ),
          
          title: Text(person.fullName, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 4),
              // Chip del Rol
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: Colors.blue.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.blue.shade100),
                ),
                child: Text(
                  person.role.toString().split('.').last.toUpperCase(),
                  style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.blue.shade800),
                ),
              ),
              const SizedBox(height: 4),
              Text(person.email, style: const TextStyle(fontSize: 12, color: Colors.grey)),
            ],
          ),
          
          trailing: const Icon(Icons.chevron_right, color: Colors.grey),
          
          // Al tocar la tarjeta, vamos a la página de detalles
          onTap: () => context.push('/person/${person.id}'),
        ),
      ),
    );
  }
}
