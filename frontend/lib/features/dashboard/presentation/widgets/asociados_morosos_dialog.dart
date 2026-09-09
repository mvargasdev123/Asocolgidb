import 'package:flutter/material.dart';
import '../../domain/models/metrics_model.dart';

class AsociadosMorososDialog extends StatelessWidget {
  final AsociadosMorososPendientesModel data;

  const AsociadosMorososDialog({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: 850,
        height: 550,
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: const [
                    Icon(Icons.warning_amber_rounded, color: Colors.redAccent, size: 28),
                    SizedBox(width: 10),
                    Text(
                      'Detalle de Asociados Morosos y Pendientes',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                IconButton(
                  icon: const Icon(Icons.close),
                  onPressed: () => Navigator.of(context).pop(),
                ),
              ],
            ),
            const Divider(height: 24),
            Expanded(
              child: LayoutBuilder(
                builder: (context, constraints) {
                  final isWide = constraints.maxWidth > 600;
                  if (isWide) {
                    return Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(child: _buildColumn(context, 'Asociados Morosos', data.morosos, Colors.red.shade700, Colors.red.shade50)),
                        const VerticalDivider(width: 32),
                        Expanded(child: _buildColumn(context, 'Asociados Pendientes', data.pendientes, Colors.amber.shade800, Colors.amber.shade50)),
                      ],
                    );
                  } else {
                    return DefaultTabController(
                      length: 2,
                      child: Column(
                        children: [
                          const TabBar(
                            tabs: [
                              Tab(text: 'Morosos'),
                              Tab(text: 'Pendientes'),
                            ],
                          ),
                          Expanded(
                            child: TabBarView(
                              children: [
                                _buildColumn(context, 'Asociados Morosos', data.morosos, Colors.red.shade700, Colors.red.shade50),
                                _buildColumn(context, 'Asociados Pendientes', data.pendientes, Colors.amber.shade800, Colors.amber.shade50),
                              ],
                            ),
                          ),
                        ],
                      ),
                    );
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildColumn(BuildContext context, String title, List<PersonaMetricSummary> list, Color primaryColor, Color bgColor) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: primaryColor.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                title,
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: primaryColor),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: primaryColor,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  '${list.length}',
                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Expanded(
            child: list.isEmpty
                ? Center(
                    child: Text(
                      'No hay registros en esta categoría.',
                      style: TextStyle(color: Colors.grey.shade600, fontStyle: FontStyle.italic),
                    ),
                  )
                : ListView.separated(
                    itemCount: list.length,
                    separatorBuilder: (_, __) => const SizedBox(height: 8),
                    itemBuilder: (context, index) {
                      final item = list[index];
                      return Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(8),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.04),
                              blurRadius: 4,
                              offset: const Offset(0, 2),
                            ),
                          ],
                        ),
                        child: Row(
                          children: [
                            CircleAvatar(
                              backgroundColor: primaryColor.withOpacity(0.1),
                              child: Icon(Icons.person, color: primaryColor),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    item.nombreCompleto,
                                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                                  ),
                                  Text(
                                    'DNI/NIE: ${item.numeroIdentificacion}',
                                    style: TextStyle(fontSize: 12, color: Colors.grey.shade700),
                                  ),
                                  if (item.correoElectronico != null)
                                    Text(
                                      item.correoElectronico!,
                                      style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                                    ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
