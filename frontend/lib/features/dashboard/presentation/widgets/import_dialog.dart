import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:file_picker/file_picker.dart';
import '../../../../core/theme/app_colors.dart';
import '../bloc/excel_bloc.dart';
import '../bloc/excel_event.dart';
import '../bloc/excel_state.dart';

class ImportDialog extends StatefulWidget {
  const ImportDialog({super.key});

  @override
  State<ImportDialog> createState() => _ImportDialogState();
}

class _ImportDialogState extends State<ImportDialog> {
  List<int>? _selectedFileBytes;
  String? _selectedFileName;

  // Mapa de decisiones: identificacion -> 'omitir' | 'sobreescribir'
  final Map<String, String> _decisiones = {};

  Future<void> _pickFile() async {
    final result = await FilePicker.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['xlsx', 'xls'],
      withData: true,
    );

    if (result.isNotEmpty) {
      final file = result.first;
      final bytes = await file.readAsBytes();
      if (bytes.isNotEmpty) {
        setState(() {
          _selectedFileBytes = bytes;
          _selectedFileName = file.name;
          _decisiones.clear();
        });

        // Disparar análisis Dry-Run
        if (mounted) {
          context.read<ExcelBloc>().add(
                AnalizarImportacionEvent(
                  bytes: bytes,
                  filename: file.name,
                ),
              );
        }
      }
    }
  }

  void _setDecisionesTodas(List duplicates, String accion) {
    setState(() {
      for (final item in duplicates) {
        final ident = item['identificacion'] as String;
        _decisiones[ident] = accion;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: 680,
        padding: const EdgeInsets.all(24),
        child: BlocConsumer<ExcelBloc, ExcelState>(
          listener: (context, state) {
            if (state.status == ExcelStatus.importSuccess) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(state.successMessage ?? 'Importación completada'),
                  backgroundColor: Colors.green.shade700,
                ),
              );
              Navigator.of(context).pop(true);
            } else if (state.status == ExcelStatus.failure) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(state.errorMessage ?? 'Error al procesar archivo'),
                  backgroundColor: Colors.red.shade700,
                ),
              );
            }
          },
          builder: (context, state) {
            final isLoading = state.status == ExcelStatus.loading;
            final report = state.dryRunReport;
            final duplicates = (report?['duplicados'] as List?) ?? [];
            final errors = (report?['errores'] as List?) ?? [];

            return Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: AppColors.primaryYellow.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.upload_file_rounded,
                        color: Colors.amber,
                        size: 26,
                      ),
                    ),
                    const SizedBox(width: 14),
                    const Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Importación Masiva desde Excel',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: AppColors.primaryBlue,
                            ),
                          ),
                          Text(
                            'Análisis previo (Dry-Run) y resolución de coincidencias',
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
                if (_selectedFileName == null) ...[
                  // Paso 1: Seleccionar archivo
                  Center(
                    child: Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(32),
                      decoration: BoxDecoration(
                        color: Colors.grey.shade50,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.grey.shade300, style: BorderStyle.solid),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.cloud_upload_outlined, size: 48, color: Colors.grey.shade600),
                          const SizedBox(height: 12),
                          const Text(
                            'Selecciona el archivo Excel (.xlsx)',
                            style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 4),
                          const Text(
                            'Debe contener las pestañas BD, ASO, EXP y VOL',
                            style: TextStyle(fontSize: 12, color: Colors.black54),
                          ),
                          const SizedBox(height: 20),
                          ElevatedButton.icon(
                            icon: const Icon(Icons.folder_open),
                            label: const Text('Buscar Archivo'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: AppColors.primaryBlue,
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                            ),
                            onPressed: _pickFile,
                          ),
                        ],
                      ),
                    ),
                  ),
                ] else ...[
                  // Archivo Seleccionado e Info de Dry-Run
                  Row(
                    children: [
                      const Icon(Icons.description, color: AppColors.primaryBlue, size: 20),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          _selectedFileName!,
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                        ),
                      ),
                      TextButton.icon(
                        icon: const Icon(Icons.change_circle_outlined, size: 18),
                        label: const Text('Cambiar'),
                        onPressed: isLoading ? null : _pickFile,
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),
                  if (isLoading)
                    Container(
                      padding: const EdgeInsets.all(24),
                      alignment: Alignment.center,
                      child: const Column(
                        children: [
                          CircularProgressIndicator(),
                          SizedBox(height: 12),
                          Text('Analizando archivo en modo Dry-Run (sin modificar DB)...'),
                        ],
                      ),
                    )
                  else if (report != null) ...[
                    // Tarjetas de Resumen
                    Row(
                      children: [
                        _buildStatChip('Total Filas', '${report['total_filas']}', Colors.blue),
                        const SizedBox(width: 8),
                        _buildStatChip('Nuevos', '${report['nuevos_listos_para_guardar']}', Colors.green),
                        const SizedBox(width: 8),
                        _buildStatChip('Duplicados', '${duplicates.length}', Colors.orange),
                        const SizedBox(width: 8),
                        _buildStatChip('Errores', '${errors.length}', Colors.red),
                      ],
                    ),
                    const SizedBox(height: 16),
                    // Si hay duplicados, mostrar tabla de resolución
                    if (duplicates.isNotEmpty) ...[
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Resolución de Duplicados:',
                            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                          ),
                          Row(
                            children: [
                              TextButton(
                                onPressed: () => _setDecisionesTodas(duplicates, 'omitir'),
                                child: const Text('Omitir Todos', style: TextStyle(fontSize: 12)),
                              ),
                              TextButton(
                                onPressed: () => _setDecisionesTodas(duplicates, 'sobreescribir'),
                                child: const Text('Sobreescribir Todos', style: TextStyle(fontSize: 12)),
                              ),
                            ],
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Container(
                        height: 180,
                        decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey.shade300),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: ListView.separated(
                          itemCount: duplicates.length,
                          separatorBuilder: (_, __) => const Divider(height: 1),
                          itemBuilder: (context, index) {
                            final dup = duplicates[index] as Map<String, dynamic>;
                            final ident = dup['identificacion'] as String;
                            final nombre = dup['nombre_excel'] as String;
                            final fila = dup['fila_excel'];
                            final currentDec = _decisiones[ident] ?? 'sobreescribir';

                            return ListTile(
                              dense: true,
                              title: Text('Fila $fila: $nombre ($ident)'),
                              subtitle: const Text('Ya existe en la base de datos'),
                              trailing: SegmentedButton<String>(
                                selected: {currentDec},
                                onSelectionChanged: (newSelection) {
                                  setState(() {
                                    _decisiones[ident] = newSelection.first;
                                  });
                                },
                                segments: const [
                                  ButtonSegment(
                                    value: 'sobreescribir',
                                    label: Text('Sobreescribir', style: TextStyle(fontSize: 11)),
                                  ),
                                  ButtonSegment(
                                    value: 'omitir',
                                    label: Text('Omitir', style: TextStyle(fontSize: 11)),
                                  ),
                                ],
                              ),
                            );
                          },
                        ),
                      ),
                    ],
                    if (errors.isNotEmpty) ...[
                      const SizedBox(height: 12),
                      Container(
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: Colors.red.shade50,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Errores Detectados:', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold, fontSize: 12)),
                            ...errors.map((err) => Text('• ${err['mensaje']}', style: const TextStyle(fontSize: 11, color: Colors.red))),
                          ],
                        ),
                      ),
                    ],
                  ],
                ],
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    TextButton(
                      onPressed: isLoading ? null : () => Navigator.of(context).pop(),
                      child: const Text('Cancelar'),
                    ),
                    const SizedBox(width: 12),
                    if (_selectedFileBytes != null && report != null)
                      ElevatedButton.icon(
                        icon: const Icon(Icons.check_circle_outline, size: 18),
                        label: const Text('Confirmar Importación'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green.shade700,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                        ),
                        onPressed: isLoading
                            ? null
                            : () {
                                context.read<ExcelBloc>().add(
                                      ConfirmarImportacionEvent(
                                        bytes: _selectedFileBytes!,
                                        filename: _selectedFileName!,
                                        decisiones: _decisiones,
                                      ),
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

  Widget _buildStatChip(String label, String value, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
        decoration: BoxDecoration(
          color: color.withOpacity(0.08),
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          children: [
            Text(
              value,
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: color),
            ),
            Text(
              label,
              style: const TextStyle(fontSize: 11, color: Colors.black54),
            ),
          ],
        ),
      ),
    );
  }
}
