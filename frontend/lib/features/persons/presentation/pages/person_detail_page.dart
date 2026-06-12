import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/person_list_provider.dart';

class PersonDetailPage extends ConsumerWidget {
  final int personId;
  const PersonDetailPage({super.key, required this.personId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(personListProvider);
    
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Perfil de Miembro'),
        backgroundColor: Colors.white,
        elevation: 0,
      ),
      body: state.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
        data: (persons) {
          try {
            final person = persons.firstWhere((p) => p.id == personId);
            return SingleChildScrollView(
              child: Column(
                children: [
                  // Cabecera gigante
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.symmetric(vertical: 40),
                    decoration: const BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.only(bottomLeft: Radius.circular(30), bottomRight: Radius.circular(30)),
                    ),
                    child: Column(
                      children: [
                        CircleAvatar(
                          radius: 50,
                          backgroundColor: Colors.teal.shade50,
                          child: Text(
                            person.fullName.substring(0, 1).toUpperCase(),
                            style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: Colors.teal.shade800),
                          ),
                        ),
                        const SizedBox(height: 16),
                        Text(person.fullName, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                          decoration: BoxDecoration(color: Colors.blue.shade50, borderRadius: BorderRadius.circular(20)),
                          child: Text(
                            person.role.toString().split('.').last.toUpperCase(),
                            style: TextStyle(color: Colors.blue.shade800, fontWeight: FontWeight.bold),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),
                  
                  // Información
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: Column(
                      children: [
                        _buildInfoCard(
                          title: 'Datos Personales',
                          icon: Icons.person_outline,
                          children: [
                            _buildDetailRow(Icons.email_outlined, 'Correo Electrónico', person.email),
                            const SizedBox(height: 16),
                            _buildDetailRow(Icons.cake_outlined, 'Fecha de Nacimiento', person.birthDate != null ? "${person.birthDate!.day}/${person.birthDate!.month}/${person.birthDate!.year}" : "No registrada"),
                            const SizedBox(height: 16),
                            _buildDetailRow(Icons.home_outlined, 'Dirección', person.address ?? 'No registrada'),
                          ],
                        ),
                        
                        _buildInfoCard(
                          title: 'Identificación y Asignación',
                          icon: Icons.badge_outlined,
                          children: [
                            _buildDetailRow(Icons.assignment_ind_outlined, 'Tipo Documento', person.tipoDocumento ?? 'No registrado'),
                            const SizedBox(height: 16),
                            _buildDetailRow(Icons.info_outline, 'Detalles', person.biography), // Acá viene la fecha de ingreso
                            const SizedBox(height: 16),
                            _buildDetailRow(Icons.check_circle_outline, 'Estado en Asocolgi', person.isActive ? "Activo" : "Inactivo", color: person.isActive ? Colors.green : Colors.red),
                          ],
                        ),
                        
                        _buildInfoCard(
                          title: 'Permisos',
                          icon: Icons.security_outlined,
                          children: [
                            _buildDetailRow(
                              Icons.privacy_tip_outlined, 
                              'Autoriza Protección de Datos', 
                              person.proteccionDatos ? 'SÍ' : 'NO',
                              color: person.proteccionDatos ? Colors.green : Colors.orange
                            ),
                            const SizedBox(height: 16),
                            _buildDetailRow(
                              Icons.camera_alt_outlined, 
                              'Autoriza Manejo de Imagen', 
                              person.manejoImagen ? 'SÍ' : 'NO',
                              color: person.manejoImagen ? Colors.green : Colors.orange
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 40),
                ],
              ),
            );
          } catch (e) {
            return const Center(child: Text('Persona no encontrada en la memoria.'));
          }
        },
      ),
    );
  }

  Widget _buildInfoCard({required String title, required IconData icon, required List<Widget> children}) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: Colors.teal),
                const SizedBox(width: 8),
                Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.teal)),
              ],
            ),
            const Divider(height: 30),
            ...children,
          ],
        ),
      ),
    );
  }

  Widget _buildDetailRow(IconData icon, String label, String value, {Color? color}) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, color: Colors.grey.shade400, size: 24),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label, style: TextStyle(fontSize: 12, color: Colors.grey.shade600)),
              const SizedBox(height: 4),
              Text(value, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500, color: color ?? Colors.black87)),
            ],
          ),
        ),
      ],
    );
  }
}
