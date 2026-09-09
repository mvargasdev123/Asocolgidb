import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/theme/app_colors.dart';
import '../../domain/models/expediente_model.dart';
import '../bloc/expedientes_bloc.dart';
import '../bloc/expedientes_event.dart';
import '../bloc/expedientes_state.dart';
import '../../../members/presentation/widgets/comments_section_widget.dart';

class ExpedienteDetailPage extends StatefulWidget {
  final ExpedienteModel expediente;

  const ExpedienteDetailPage({super.key, required this.expediente});

  @override
  State<ExpedienteDetailPage> createState() => _ExpedienteDetailPageState();
}

class _ExpedienteDetailPageState extends State<ExpedienteDetailPage> {
  late String _currentEstado;

  final List<String> _estados = [
    'En tramite',
    'Favorable',
    'Requerimento',
    'Archivado',
    'Denegado',
    'Recurso',
  ];

  @override
  void initState() {
    super.initState();
    _currentEstado = widget.expediente.estado;
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
        title: Text('Expediente: ${widget.expediente.numeroRegistro}'),
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
            } else if (state.successMessage != null) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text(state.successMessage!), backgroundColor: Colors.green),
              );
            }
          },
          builder: (context, state) {
            return LayoutBuilder(
              builder: (context, constraints) {
                final isWide = constraints.maxWidth > 850;
                if (isWide) {
                  return Padding(
                    padding: const EdgeInsets.all(20),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(flex: 5, child: _buildLeftPanel(context)),
                        const SizedBox(width: 20),
                        Expanded(flex: 5, child: _buildRightPanel(context)),
                      ],
                    ),
                  );
                } else {
                  return SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        _buildLeftPanel(context),
                        const SizedBox(height: 20),
                        _buildRightPanel(context),
                      ],
                    ),
                  );
                }
              },
            );
          },
        ),
      ),
    );
  }

  Widget _buildLeftPanel(BuildContext context) {
    final estadoColor = _getEstadoColor(_currentEstado);

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.92),
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.06),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Detalles del Trámite',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.primaryBlue),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                decoration: BoxDecoration(
                  color: estadoColor,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Text(
                  _currentEstado,
                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
                ),
              ),
            ],
          ),
          const Divider(height: 24),
          _buildInfoRow('Nº Registro', widget.expediente.numeroRegistro),
          const SizedBox(height: 10),
          _buildInfoRow('Persona', widget.expediente.personaNombre ?? 'Voluntario'),
          const SizedBox(height: 10),
          _buildInfoRow('Tipo Trámite', widget.expediente.tipoTramite),
          const SizedBox(height: 10),
          _buildInfoRow('Representante Legal', widget.expediente.representanteLegal ?? 'Sin asignar'),
          if (widget.expediente.numeroExpedienteAsignado != null && widget.expediente.numeroExpedienteAsignado!.isNotEmpty) ...[
            const SizedBox(height: 10),
            _buildInfoRow('Nº Exp. Asignado', widget.expediente.numeroExpedienteAsignado!),
          ],
          if (widget.expediente.consultorioJuridico != null && widget.expediente.consultorioJuridico!.isNotEmpty) ...[
            const SizedBox(height: 10),
            _buildInfoRow('Consultorio Jurídico', widget.expediente.consultorioJuridico!),
          ],
          const SizedBox(height: 10),
          _buildInfoRow('Aporte Social', widget.expediente.aporteSocial),
          const SizedBox(height: 10),
          _buildInfoRow('Solicitante Extranjería', widget.expediente.solicitanteExtranjeria ? 'Sí' : 'No'),
          const SizedBox(height: 10),
          _buildInfoRow('Antecedentes Apostillados', widget.expediente.antecedentesTraducidosYApostillados ? 'Sí' : 'No'),
          const SizedBox(height: 10),
          _buildInfoRow('Fecha Presentación', widget.expediente.fechaPresentacion),
          if (widget.expediente.fechaResolucion != null && widget.expediente.fechaResolucion!.isNotEmpty) ...[
            const SizedBox(height: 10),
            _buildInfoRow('Fecha Resolución', widget.expediente.fechaResolucion!),
          ],
          const SizedBox(height: 28),
          const Text(
            'Gestión de Estado',
            style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 14),
          Wrap(
            spacing: 10,
            runSpacing: 10,
            children: _estados.map((est) {
              final isSelected = _currentEstado == est;
              return ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: isSelected ? AppColors.primaryBlue : Colors.grey.shade100,
                  foregroundColor: isSelected ? Colors.white : Colors.black87,
                  elevation: isSelected ? 2 : 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                    side: BorderSide(
                      color: isSelected ? AppColors.primaryBlue : Colors.grey.shade300,
                    ),
                  ),
                ),
                onPressed: () {
                  setState(() {
                    _currentEstado = est;
                  });
                  context.read<ExpedientesBloc>().add(
                        UpdateExpedienteStatusEvent(
                          idExpediente: widget.expediente.id,
                          nuevoEstado: est,
                        ),
                      );
                },
                child: Text(
                  est,
                  style: TextStyle(
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  Widget _buildRightPanel(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.92),
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.06),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: CommentsSectionWidget(idPersona: widget.expediente.idPersona),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Row(
      children: [
        SizedBox(
          width: 140,
          child: Text(
            label,
            style: TextStyle(color: Colors.grey.shade700, fontSize: 14),
          ),
        ),
        Expanded(
          child: Text(
            value,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
          ),
        ),
      ],
    );
  }
}
