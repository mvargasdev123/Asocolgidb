import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/theme/app_colors.dart';
import '../bloc/metrics_bloc.dart';
import '../bloc/metrics_event.dart';
import '../bloc/metrics_state.dart';
import '../widgets/asociados_morosos_dialog.dart';
import '../widgets/export_dialog.dart';
import '../widgets/import_dialog.dart';
import '../../../expedientes/presentation/pages/expedientes_list_page.dart';

class DashboardMetricsView extends StatefulWidget {
  const DashboardMetricsView({super.key});

  @override
  State<DashboardMetricsView> createState() => _DashboardMetricsViewState();
}

class _DashboardMetricsViewState extends State<DashboardMetricsView> {
  @override
  void initState() {
    super.initState();
    context.read<MetricsBloc>().add(LoadMetricsEvent());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard de Métricas'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
        elevation: 1,
        actions: [
          TextButton.icon(
            icon: const Icon(Icons.download_rounded, color: Colors.teal),
            label: const Text(
              'Descargar BD',
              style: TextStyle(color: Colors.teal, fontWeight: FontWeight.bold),
            ),
            onPressed: () {
              showDialog(
                context: context,
                builder: (_) => const ExportDialog(),
              );
            },
          ),
          const SizedBox(width: 8),
          TextButton.icon(
            icon: const Icon(Icons.upload_file_rounded, color: Colors.amber),
            label: const Text(
              'Importar BD',
              style: TextStyle(color: Colors.amber, fontWeight: FontWeight.bold),
            ),
            onPressed: () {
              showDialog(
                context: context,
                builder: (_) => const ImportDialog(),
              );
            },
          ),
          const SizedBox(width: 12),
        ],
      ),
      body: Container(
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/imagen-asocolgi/plantilla_baja.jpeg'),
            fit: BoxFit.cover,
          ),
        ),
        child: BlocBuilder<MetricsBloc, MetricsState>(
          builder: (context, state) {
            if (state.status == MetricsStatus.loading) {
              return const Center(child: CircularProgressIndicator());
            }

            if (state.status == MetricsStatus.failure || state.summary == null) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('Error al cargar métricas: ${state.errorMessage ?? "Error desconocido"}'),
                    const SizedBox(height: 12),
                    ElevatedButton(
                      onPressed: () => context.read<MetricsBloc>().add(LoadMetricsEvent()),
                      child: const Text('Reintentar'),
                    ),
                  ],
                ),
              );
            }

            final summary = state.summary!;

            return SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Resumen General',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: AppColors.primaryBlue),
                  ),
                  const SizedBox(height: 16),

                  // KPI Cards Grid/Row
                  Wrap(
                    spacing: 16,
                    runSpacing: 16,
                    children: [
                      _buildKpiCard(
                        title: 'Total Personas',
                        count: '${summary.totalPersonas}',
                        icon: Icons.groups,
                        iconColor: Colors.blue.shade700,
                      ),
                      _buildKpiCard(
                        title: 'Expedientes',
                        count: '${summary.totalExpedientes}',
                        icon: Icons.folder,
                        iconColor: Colors.purple.shade600,
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => const ExpedientesListPage()),
                          );
                        },
                      ),
                      _buildKpiCard(
                        title: 'Asociados Activos',
                        count: '${summary.asociadosActivos}',
                        icon: Icons.verified_user,
                        iconColor: Colors.green.shade600,
                      ),
                      _buildKpiCard(
                        title: 'Asociados Morosos/Pendientes',
                        count: '${summary.asociadosMorososCount + summary.asociadosPendientesCount}',
                        icon: Icons.warning_amber_rounded,
                        iconColor: (summary.asociadosMorososCount + summary.asociadosPendientesCount) > 0
                            ? Colors.red.shade600
                            : Colors.grey.shade600,
                        borderColor: (summary.asociadosMorososCount + summary.asociadosPendientesCount) > 0
                            ? Colors.red.shade400
                            : null,
                        onTap: () async {
                          context.read<MetricsBloc>().add(LoadMorososPendientesEvent());
                          final morososState = context.read<MetricsBloc>().state;
                          if (morososState.morososPendientes != null) {
                            showDialog(
                              context: context,
                              builder: (_) => AsociadosMorososDialog(data: morososState.morososPendientes!),
                            );
                          } else {
                            // Cargar datos y mostrar
                            final repo = context.read<MetricsBloc>().repository;
                            final res = await repo.getAsociadosMorososYPendientes();
                            if (context.mounted) {
                              showDialog(
                                context: context,
                                builder: (_) => AsociadosMorososDialog(data: res),
                              );
                            }
                          }
                        },
                      ),
                      _buildKpiCard(
                        title: 'Total Voluntarios',
                        count: '${summary.totalVoluntarios}',
                        icon: Icons.volunteer_activism,
                        iconColor: Colors.amber.shade800,
                      ),
                    ],
                  ),
                  const SizedBox(height: 28),

                  // Distribution Box Cards
                  LayoutBuilder(
                    builder: (context, constraints) {
                      final isWide = constraints.maxWidth > 900;
                      return Column(
                        children: [
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Expanded(
                                child: _buildDistributionCard(
                                  'Distribución por Roles',
                                  summary.distribucionRoles,
                                  summary.totalPersonas,
                                  Colors.blue.shade600,
                                ),
                              ),
                              const SizedBox(width: 16),
                              Expanded(
                                child: _buildDistributionCard(
                                  'Situación Administrativa',
                                  summary.situacionAdministrativa,
                                  summary.totalPersonas,
                                  Colors.teal.shade600,
                                ),
                              ),
                              if (isWide) ...[
                                const SizedBox(width: 16),
                                Expanded(
                                  child: _buildDistributionCard(
                                    'Demografía',
                                    summary.demografiaGenero,
                                    summary.totalPersonas,
                                    Colors.indigo.shade600,
                                  ),
                                ),
                              ],
                            ],
                          ),
                          const SizedBox(height: 16),
                          if (!isWide) ...[
                            _buildDistributionCard(
                              'Demografía',
                              summary.demografiaGenero,
                              summary.totalPersonas,
                              Colors.indigo.shade600,
                            ),
                            const SizedBox(height: 16),
                          ],
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Expanded(
                                child: _buildDistributionCard(
                                  'Top 5 Nacionalidades',
                                  summary.nacionalidadesTop5,
                                  summary.totalPersonas,
                                  Colors.purple.shade600,
                                ),
                              ),
                              const SizedBox(width: 16),
                              Expanded(
                                child: _buildDistributionCard(
                                  'Top 5 Ciudades',
                                  summary.ciudadesTop5,
                                  summary.totalPersonas,
                                  Colors.orange.shade600,
                                ),
                              ),
                              if (isWide) ...[
                                const SizedBox(width: 16),
                                Expanded(
                                  child: _buildDistributionCard(
                                    'Top 5 Motivos de Consulta',
                                    summary.motivosConsultaTop5,
                                    summary.totalPersonas,
                                    Colors.pink.shade600,
                                  ),
                                ),
                              ],
                            ],
                          ),
                          if (!isWide) ...[
                            const SizedBox(height: 16),
                            _buildDistributionCard(
                              'Top 5 Motivos de Consulta',
                              summary.motivosConsultaTop5,
                              summary.totalPersonas,
                              Colors.pink.shade600,
                            ),
                          ],
                        ],
                      );
                    },
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _buildKpiCard({
    required String title,
    required String count,
    required IconData icon,
    required Color iconColor,
    Color? borderColor,
    VoidCallback? onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        width: 220,
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.92),
          borderRadius: BorderRadius.circular(12),
          border: borderColor != null ? Border.all(color: borderColor, width: 2) : null,
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 8,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: iconColor.withOpacity(0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(icon, color: iconColor, size: 26),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(fontSize: 11, color: Colors.grey.shade700, fontWeight: FontWeight.w500),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 2),
                  Text(
                    count,
                    style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDistributionCard(String title, Map<String, int> data, int total, Color barColor) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.92),
        borderRadius: BorderRadius.circular(14),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 6,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppColors.primaryBlue),
          ),
          const Divider(height: 20),
          if (data.isEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 12),
              child: Text('Sin datos disponibles', style: TextStyle(fontSize: 13, color: Colors.grey.shade500, fontStyle: FontStyle.italic)),
            )
          else
            ...data.entries.map((entry) {
              final val = entry.value;
              final pct = total > 0 ? (val / total) : 0.0;
              return Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(entry.key, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500)),
                        Text('$val', style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Colors.grey.shade700)),
                      ],
                    ),
                    const SizedBox(height: 4),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(4),
                      child: LinearProgressIndicator(
                        value: pct.clamp(0.0, 1.0),
                        minHeight: 8,
                        backgroundColor: Colors.grey.shade200,
                        valueColor: AlwaysStoppedAnimation<Color>(barColor),
                      ),
                    ),
                  ],
                ),
              );
            }),
        ],
      ),
    );
  }
}
