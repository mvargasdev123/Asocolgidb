import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/theme/app_colors.dart';
import '../bloc/expedientes_bloc.dart';
import '../bloc/expedientes_event.dart';
import '../bloc/expedientes_state.dart';
import '../../domain/models/expediente_model.dart';
import 'expediente_detail_page.dart';

class ExpedientesListPage extends StatefulWidget {
  const ExpedientesListPage({super.key});

  @override
  State<ExpedientesListPage> createState() => _ExpedientesListPageState();
}

class _ExpedientesListPageState extends State<ExpedientesListPage> {
  final List<String> _estados = [
    'Todos',
    'En tramite',
    'Favorable',
    'Requerimento',
    'Archivado',
    'Denegado',
    'Recurso'
  ];

  String _filtroSeleccionado = 'Todos';

  @override
  void initState() {
    super.initState();
    context.read<ExpedientesBloc>().add(LoadExpedientes());
  }

  Color _getEstadoColor(String estado) {
    switch (estado) {
      case 'En tramite':
        return Colors.blue.shade700;
      case 'Favorable':
        return Colors.green.shade600;
      case 'Requerimento':
        return Colors.amber.shade700;
      case 'Archivado':
        return Colors.grey.shade600;
      case 'Denegado':
        return Colors.red.shade600;
      case 'Recurso':
        return Colors.purple.shade600;
      default:
        return Colors.blue.shade700;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gestión de Expedientes'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
        elevation: 1,
      ),
      body: Container(
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/imagen-asocolgi/plantilla_baja.jpeg'),
            fit: BoxFit.cover,
          ),
        ),
        child: BlocConsumer<ExpedientesBloc, ExpedientesState>(
          listener: (context, state) {
            if (state.errorMessage != null) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text(state.errorMessage!), backgroundColor: Colors.red),
              );
            }
          },
          builder: (context, state) {
            final expedientes = state.expedientes;
            final totalExpedientes = expedientes.length;
            final expedientesActivos = expedientes.where((e) => e.estado == 'En tramite').length;

            return Column(
              children: [
                // Top KPI Cards
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Expanded(
                        child: _buildTopKpiCard(
                          title: 'Total Expedientes',
                          count: '$totalExpedientes',
                          icon: Icons.folder,
                          iconColor: Colors.blue.shade700,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: _buildTopKpiCard(
                          title: 'Expedientes Activos',
                          count: '$expedientesActivos',
                          icon: Icons.folder_open,
                          iconColor: Colors.blue.shade400,
                        ),
                      ),
                    ],
                  ),
                ),

                // Filter Chips Row
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Row(
                    children: _estados.map((est) {
                      final isSelected = _filtroSeleccionado == est;
                      return Padding(
                        padding: const EdgeInsets.only(right: 8),
                        child: ChoiceChip(
                          label: Text(est),
                          selected: isSelected,
                          selectedColor: AppColors.primaryBlue,
                          labelStyle: TextStyle(
                            color: isSelected ? Colors.white : Colors.black87,
                            fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                          ),
                          onSelected: (selected) {
                            if (selected) {
                              setState(() {
                                _filtroSeleccionado = est;
                              });
                              final queryEstado = est == 'Todos' ? null : est;
                              context.read<ExpedientesBloc>().add(LoadExpedientes(estado: queryEstado));
                            }
                          },
                        ),
                      );
                    }).toList(),
                  ),
                ),
                const SizedBox(height: 16),

                // Expedientes List
                Expanded(
                  child: state.status == ExpedientesStatus.loading
                      ? const Center(child: CircularProgressIndicator())
                      : expedientes.isEmpty
                          ? const Center(
                              child: Text(
                                'No se encontraron expedientes.',
                                style: TextStyle(fontSize: 16, fontStyle: FontStyle.italic),
                              ),
                            )
                          : ListView.builder(
                              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                              itemCount: expedientes.length,
                              itemBuilder: (context, index) {
                                final exp = expedientes[index];
                                return Card(
                                  margin: const EdgeInsets.only(bottom: 12),
                                  elevation: 3,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: ListTile(
                                    contentPadding: const EdgeInsets.all(16),
                                    leading: CircleAvatar(
                                      backgroundColor: Colors.blue.shade50,
                                      child: Icon(Icons.person, color: Colors.blue.shade800),
                                    ),
                                    title: Text(
                                      exp.personaNombre ?? 'Voluntario',
                                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                                    ),
                                    subtitle: Padding(
                                      padding: const EdgeInsets.only(top: 4),
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Text('Trámite: ${exp.tipoTramite}', style: const TextStyle(fontSize: 14)),
                                          Text('Nº Registro: ${exp.numeroRegistro}', style: TextStyle(fontSize: 12, color: Colors.grey.shade700)),
                                        ],
                                      ),
                                    ),
                                    trailing: Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                                      decoration: BoxDecoration(
                                        color: _getEstadoColor(exp.estado),
                                        borderRadius: BorderRadius.circular(20),
                                      ),
                                      child: Text(
                                        exp.estado,
                                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
                                      ),
                                    ),
                                    onTap: () async {
                                      final bloc = context.read<ExpedientesBloc>();
                                      await Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (_) => ExpedienteDetailPage(expediente: exp),
                                        ),
                                      );
                                      if (!mounted) return;
                                      bloc.add(LoadExpedientes(
                                        estado: _filtroSeleccionado == 'Todos' ? null : _filtroSeleccionado,
                                      ));
                                    },
                                  ),
                                );
                              },
                            ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildTopKpiCard({
    required String title,
    required String count,
    required IconData icon,
    required Color iconColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.9),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 6,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: iconColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, color: iconColor, size: 28),
          ),
          const SizedBox(width: 14),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: TextStyle(fontSize: 12, color: Colors.grey.shade600)),
              Text(count, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            ],
          ),
        ],
      ),
    );
  }
}
