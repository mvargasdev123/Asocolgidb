import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/theme/app_colors.dart';
import '../bloc/excel_bloc.dart';
import '../bloc/excel_event.dart';
import '../bloc/excel_state.dart';

class ExportDialog extends StatefulWidget {
  const ExportDialog({super.key});

  @override
  State<ExportDialog> createState() => _ExportDialogState();
}

class _ExportDialogState extends State<ExportDialog> {
  String _selectedOption = 'completa';

  final List<Map<String, String>> _options = [
    {
      'id': 'completa',
      'title': 'Base de Datos Completa',
      'subtitle': 'Exporta las 4 pestañas: BD, ASO, EXP y VOL',
      'icon': 'dataset',
    },
    {
      'id': 'asociados',
      'title': 'Solo Asociados',
      'subtitle': 'Exporta pestañas BD y ASO relativas a miembros',
      'icon': 'people',
    },
    {
      'id': 'voluntarios',
      'title': 'Solo Voluntarios',
      'subtitle': 'Exporta pestañas BD y VOL relativas a voluntarios',
      'icon': 'volunteer_activism',
    },
    {
      'id': 'expedientes',
      'title': 'Solo Expedientes',
      'subtitle': 'Exporta la pestaña EXP de trámites legales',
      'icon': 'folder_special',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: 520,
        padding: const EdgeInsets.all(24),
        child: BlocConsumer<ExcelBloc, ExcelState>(
          listener: (context, state) {
            if (state.status == ExcelStatus.exportSuccess) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(state.successMessage ?? 'Enviado al correo'),
                  backgroundColor: Colors.green.shade700,
                ),
              );
              Navigator.of(context).pop();
            } else if (state.status == ExcelStatus.failure) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(state.errorMessage ?? 'Error al exportar'),
                  backgroundColor: Colors.red.shade700,
                ),
              );
            }
          },
          builder: (context, state) {
            final isLoading = state.status == ExcelStatus.loading;

            return Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: AppColors.primaryBlue.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.mark_email_read_outlined,
                        color: AppColors.primaryBlue,
                        size: 26,
                      ),
                    ),
                    const SizedBox(width: 14),
                    const Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Exportar Base de Datos Excel',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: AppColors.primaryBlue,
                            ),
                          ),
                          Text(
                            'Descarga directa a tu equipo o envío al correo oficial',
                            style: TextStyle(fontSize: 12, color: Colors.black54),
                          ),
                        ],
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.close),
                      onPressed: isLoading ? null : () => Navigator.of(context).pop(),
                    ),
                  ],
                ),
                const Divider(height: 24),
                const Text(
                  'Seleccione el alcance de la exportación:',
                  style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                ),
                const SizedBox(height: 12),
                Column(
                  children: _options.map((opt) {
                    final isSelected = _selectedOption == opt['id'];
                    return Container(
                      margin: const EdgeInsets.only(bottom: 8),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? AppColors.primaryBlue.withOpacity(0.06)
                            : Colors.grey.shade50,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                          color: isSelected
                              ? AppColors.primaryBlue
                              : Colors.grey.shade300,
                          width: isSelected ? 1.5 : 1,
                        ),
                      ),
                      child: RadioListTile<String>(
                        value: opt['id']!,
                        groupValue: _selectedOption,
                        onChanged: isLoading
                            ? null
                            : (val) {
                                if (val != null) {
                                  setState(() => _selectedOption = val);
                                }
                              },
                        activeColor: AppColors.primaryBlue,
                        title: Text(
                          opt['title']!,
                          style: TextStyle(
                            fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                            color: isSelected ? AppColors.primaryBlue : Colors.black87,
                            fontSize: 14,
                          ),
                        ),
                        subtitle: Text(
                          opt['subtitle']!,
                          style: const TextStyle(fontSize: 12),
                        ),
                      ),
                    );
                  }).toList(),
                ),
                const SizedBox(height: 16),
                if (isLoading)
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Row(
                      children: [
                        SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        ),
                        SizedBox(width: 14),
                        Expanded(
                          child: Text(
                            'Procesando archivo Excel en el servidor...',
                            style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
                          ),
                        ),
                      ],
                    ),
                  )
                else
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      TextButton(
                        onPressed: () => Navigator.of(context).pop(),
                        child: const Text('Cancelar'),
                      ),
                      const SizedBox(width: 8),
                      OutlinedButton.icon(
                        icon: const Icon(Icons.send_rounded, size: 18),
                        label: const Text('Enviar a Correo'),
                        style: OutlinedButton.styleFrom(
                          foregroundColor: AppColors.primaryBlue,
                          side: const BorderSide(color: AppColors.primaryBlue),
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        onPressed: () {
                          context.read<ExcelBloc>().add(
                                ExportarExcelEvent(_selectedOption),
                              );
                        },
                      ),
                      const SizedBox(width: 8),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.download_rounded, size: 18),
                        label: const Text('Descargar Directo'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primaryBlue,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        onPressed: () {
                          context.read<ExcelBloc>().add(
                                DescargarExcelDirectoEvent(_selectedOption),
                              );
                        },
                      ),
                    ],
                  ),
              ],
            );
          },
        ),
      ),
    );
  }
}
