import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/theme/app_colors.dart';
import '../../domain/models/comentario_model.dart';
import '../../domain/repositories/comentario_repository.dart';
import '../bloc/comentarios/comentarios_bloc.dart';
import '../bloc/comentarios/comentarios_event.dart';
import '../bloc/comentarios/comentarios_state.dart';

class CommentsSectionWidget extends StatelessWidget {
  final int idPersona;

  const CommentsSectionWidget({super.key, required this.idPersona});

  @override
  Widget build(BuildContext context) {
    return BlocProvider<ComentariosBloc>(
      create: (context) => ComentariosBloc(
        repository: context.read<ComentarioRepository>(),
      )..add(LoadComentarios(idPersona)),
      child: _CommentsSectionContent(idPersona: idPersona),
    );
  }
}

class _CommentsSectionContent extends StatefulWidget {
  final int idPersona;

  const _CommentsSectionContent({required this.idPersona});

  @override
  State<_CommentsSectionContent> createState() => _CommentsSectionContentState();
}

class _CommentsSectionContentState extends State<_CommentsSectionContent> {
  bool _isExpanded = true;
  String _selectedTipo = 'Persona';
  final TextEditingController _commentTextController = TextEditingController();
  final TextEditingController _fechaController = TextEditingController();

  final List<String> _categorias = [
    'Persona',
    'Voluntario',
    'Asociado',
    'Expediente',
  ];

  @override
  void initState() {
    super.initState();
    final now = DateTime.now();
    _fechaController.text =
        "${now.year}-${now.month.toString().padLeft(2, '0')}-${now.day.toString().padLeft(2, '0')}";
  }

  @override
  void dispose() {
    _commentTextController.dispose();
    _fechaController.dispose();
    super.dispose();
  }

  Future<void> _selectDate(
    BuildContext context,
    TextEditingController controller,
  ) async {
    DateTime initial = DateTime.tryParse(controller.text) ?? DateTime.now();
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: initial,
      firstDate: DateTime(1900),
      lastDate: DateTime(2100),
    );
    if (picked != null) {
      controller.text =
          "${picked.year}-${picked.month.toString().padLeft(2, '0')}-${picked.day.toString().padLeft(2, '0')}";
    }
  }

  Color _getBadgeColor(String tipo) {
    switch (tipo.toLowerCase()) {
      case 'persona':
        return const Color(0xFF2196F3); // Blue
      case 'voluntario':
        return const Color(0xFFFFB300); // Amber / Yellow
      case 'asociado':
        return const Color(0xFF4CAF50); // Green
      case 'expediente':
        return const Color(0xFF9C27B0); // Purple
      default:
        return const Color(0xFF757575); // Grey fallback
    }
  }

  Color _getBadgeBackgroundColor(String tipo) {
    switch (tipo.toLowerCase()) {
      case 'persona':
        return const Color(0xFFE3F2FD);
      case 'voluntario':
        return const Color(0xFFFFF8E1);
      case 'asociado':
        return const Color(0xFFE8F5E9);
      case 'expediente':
        return const Color(0xFFF3E5F5);
      default:
        return const Color(0xFFF5F5F5);
    }
  }

  void _addComment() {
    final text = _commentTextController.text.trim();
    if (text.isEmpty) return;

    DateTime? customDate = DateTime.tryParse(_fechaController.text);

    context.read<ComentariosBloc>().add(
          AddComentario(
            idPersona: widget.idPersona,
            texto: text,
            tipo: _selectedTipo,
            fechaCreacion: customDate,
          ),
        );
    _commentTextController.clear();
  }

  void _showEditDialog(ComentarioModel comentario) {
    final editController = TextEditingController(text: comentario.texto);
    final dtLocal = comentario.fechaCreacion.toLocal();
    final editFechaController = TextEditingController(
      text: "${dtLocal.year}-${dtLocal.month.toString().padLeft(2, '0')}-${dtLocal.day.toString().padLeft(2, '0')}",
    );
    String editTipo = comentario.tipo;

    showDialog(
      context: context,
      builder: (dialogCtx) => StatefulBuilder(
        builder: (context, setDialogState) {
          return AlertDialog(
            title: const Text('Actualizar Comentario'),
            content: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: DropdownButtonFormField<String>(
                          value: editTipo,
                          decoration: const InputDecoration(
                            labelText: 'Categoría',
                            border: OutlineInputBorder(),
                            contentPadding: EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                          ),
                          items: _categorias
                              .map((cat) => DropdownMenuItem(
                                    value: cat,
                                    child: Text(cat),
                                  ))
                              .toList(),
                          onChanged: (val) {
                            if (val != null) {
                              setDialogState(() => editTipo = val);
                            }
                          },
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: TextField(
                          controller: editFechaController,
                          readOnly: true,
                          decoration: InputDecoration(
                            labelText: 'Fecha',
                            border: const OutlineInputBorder(),
                            contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                            suffixIcon: IconButton(
                              icon: const Icon(Icons.calendar_today, size: 18),
                              onPressed: () async {
                                await _selectDate(context, editFechaController);
                                setDialogState(() {});
                              },
                            ),
                          ),
                          onTap: () async {
                            await _selectDate(context, editFechaController);
                            setDialogState(() {});
                          },
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: editController,
                    minLines: 2,
                    maxLines: 5,
                    decoration: const InputDecoration(
                      labelText: 'Texto del comentario',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ],
              ),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(dialogCtx),
                child: const Text('Cancelar'),
              ),
              ElevatedButton(
                onPressed: () {
                  final newText = editController.text.trim();
                  DateTime? newDate = DateTime.tryParse(editFechaController.text);
                  if (newText.isNotEmpty) {
                    this.context.read<ComentariosBloc>().add(
                          UpdateComentario(
                            idComentario: comentario.id,
                            idPersona: widget.idPersona,
                            texto: newText,
                            tipo: editTipo,
                            fechaCreacion: newDate,
                          ),
                        );
                  }
                  Navigator.pop(dialogCtx);
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryBlue,
                ),
                child: const Text('Guardar', style: TextStyle(color: Colors.white)),
              ),
            ],
          );
        },
      ),
    );
  }

  void _confirmDelete(ComentarioModel comentario) {
    showDialog(
      context: context,
      builder: (dialogCtx) => AlertDialog(
        title: const Text('Eliminar Comentario'),
        content: const Text('¿Estás seguro de que deseas eliminar este comentario?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogCtx),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppColors.errorRed),
            onPressed: () {
              Navigator.pop(dialogCtx);
              context.read<ComentariosBloc>().add(
                    DeleteComentario(
                      idComentario: comentario.id,
                      idPersona: widget.idPersona,
                    ),
                  );
            },
            child: const Text('Eliminar', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(top: 24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey.shade300),
      ),
      child: Column(
        children: [
          // Header / Accordion Switcher
          InkWell(
            onTap: () => setState(() => _isExpanded = !_isExpanded),
            borderRadius: const BorderRadius.vertical(top: Radius.circular(8)),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
              decoration: BoxDecoration(
                color: Colors.grey.shade100,
                borderRadius: BorderRadius.vertical(
                  top: const Radius.circular(8),
                  bottom: Radius.circular(_isExpanded ? 0 : 8),
                ),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Row(
                    children: [
                      Icon(Icons.comment_outlined, color: AppColors.primaryBlue),
                      SizedBox(width: 10),
                      Text(
                        'Gestión de Comentarios',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: AppColors.textDark,
                        ),
                      ),
                    ],
                  ),
                  Icon(
                    _isExpanded
                        ? Icons.keyboard_arrow_up
                        : Icons.keyboard_arrow_down,
                    color: Colors.grey.shade700,
                  ),
                ],
              ),
            ),
          ),

          if (_isExpanded)
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: BlocBuilder<ComentariosBloc, ComentariosState>(
                builder: (context, state) {
                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Auto-Expanding Input + Category Dropdown
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.grey.shade50,
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.grey.shade300),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Text(
                                  'Categoría:',
                                  style: TextStyle(
                                    fontWeight: FontWeight.w600,
                                    fontSize: 13,
                                  ),
                                ),
                                const SizedBox(width: 8),
                                SizedBox(
                                  width: 130,
                                  child: DropdownButtonFormField<String>(
                                    value: _selectedTipo,
                                    isDense: true,
                                    decoration: const InputDecoration(
                                      contentPadding: EdgeInsets.symmetric(
                                          horizontal: 10, vertical: 8),
                                      border: OutlineInputBorder(),
                                    ),
                                    items: _categorias
                                        .map((cat) => DropdownMenuItem(
                                              value: cat,
                                              child: Text(
                                                cat,
                                                style: const TextStyle(fontSize: 13),
                                              ),
                                            ))
                                        .toList(),
                                    onChanged: (val) {
                                      if (val != null) {
                                        setState(() => _selectedTipo = val);
                                      }
                                    },
                                  ),
                                ),
                                const SizedBox(width: 12),
                                const Text(
                                  'Fecha:',
                                  style: TextStyle(
                                    fontWeight: FontWeight.w600,
                                    fontSize: 13,
                                  ),
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: SizedBox(
                                    height: 38,
                                    child: TextField(
                                      controller: _fechaController,
                                      readOnly: true,
                                      style: const TextStyle(fontSize: 13),
                                      decoration: InputDecoration(
                                        contentPadding: const EdgeInsets.symmetric(
                                            horizontal: 10, vertical: 8),
                                        border: const OutlineInputBorder(),
                                        suffixIcon: IconButton(
                                          icon: const Icon(Icons.calendar_today, size: 16),
                                          padding: EdgeInsets.zero,
                                          constraints: const BoxConstraints(),
                                          onPressed: () => _selectDate(context, _fechaController),
                                        ),
                                      ),
                                      onTap: () => _selectDate(context, _fechaController),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 10),
                            TextField(
                              controller: _commentTextController,
                              minLines: 2,
                              maxLines: 5,
                              decoration: const InputDecoration(
                                hintText: 'Escribe un nuevo comentario...',
                                hintStyle: TextStyle(fontSize: 13),
                                border: OutlineInputBorder(),
                                contentPadding: EdgeInsets.all(12),
                              ),
                            ),
                            const SizedBox(height: 10),
                            Align(
                              alignment: Alignment.centerRight,
                              child: ElevatedButton.icon(
                                onPressed: state.isSubmitting ? null : _addComment,
                                icon: state.isSubmitting
                                    ? const SizedBox(
                                        width: 16,
                                        height: 16,
                                        child: CircularProgressIndicator(
                                          strokeWidth: 2,
                                          color: Colors.white,
                                        ),
                                      )
                                    : const Icon(Icons.add_comment, size: 18),
                                label: const Text('Agregar Comentario'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: const Color(0xFF4CAF50),
                                  foregroundColor: Colors.white,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 20),

                      // Comments List Section
                      if (state.status == ComentariosStatus.loading)
                        const Center(
                          child: Padding(
                            padding: EdgeInsets.all(24.0),
                            child: CircularProgressIndicator(),
                          ),
                        )
                      else if (state.comentarios.isEmpty)
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(20),
                          decoration: BoxDecoration(
                            color: Colors.grey.shade50,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: Colors.grey.shade200),
                          ),
                          child: const Center(
                            child: Text(
                              'No hay comentarios.',
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.grey,
                                fontStyle: FontStyle.italic,
                              ),
                            ),
                          ),
                        )
                      else
                        ListView.separated(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: state.comentarios.length,
                          separatorBuilder: (context, index) =>
                              const SizedBox(height: 10),
                          itemBuilder: (context, index) {
                            final comment = state.comentarios[index];
                            final dt = comment.fechaCreacion.toLocal();
                            final formattedDate =
                                '${dt.day.toString().padLeft(2, '0')}/${dt.month.toString().padLeft(2, '0')}/${dt.year} ${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
                            final badgeColor = _getBadgeColor(comment.tipo);
                            final badgeBg = _getBadgeBackgroundColor(comment.tipo);

                            return Container(
                              padding: const EdgeInsets.all(14),
                              decoration: BoxDecoration(
                                color: Colors.white,
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(
                                    color: badgeColor.withOpacity(0.3)),
                                boxShadow: [
                                  BoxShadow(
                                    color: Colors.black.withOpacity(0.02),
                                    blurRadius: 4,
                                    offset: const Offset(0, 2),
                                  ),
                                ],
                              ),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    children: [
                                      // Category Badge
                                      Container(
                                        padding: const EdgeInsets.symmetric(
                                            horizontal: 10, vertical: 4),
                                        decoration: BoxDecoration(
                                          color: badgeBg,
                                          borderRadius:
                                              BorderRadius.circular(12),
                                          border: Border.all(color: badgeColor),
                                        ),
                                        child: Text(
                                          comment.tipo.toUpperCase(),
                                          style: TextStyle(
                                            color: badgeColor,
                                            fontWeight: FontWeight.bold,
                                            fontSize: 11,
                                          ),
                                        ),
                                      ),
                                      Row(
                                        children: [
                                          Text(
                                            formattedDate,
                                            style: const TextStyle(
                                              fontSize: 12,
                                              color: Colors.grey,
                                            ),
                                          ),
                                          const SizedBox(width: 8),
                                          IconButton(
                                            icon: const Icon(Icons.edit_outlined,
                                                size: 18, color: Colors.blue),
                                            tooltip: 'Editar Comentario',
                                            constraints: const BoxConstraints(),
                                            padding: EdgeInsets.zero,
                                            onPressed: () =>
                                                _showEditDialog(comment),
                                          ),
                                          const SizedBox(width: 8),
                                          IconButton(
                                            icon: const Icon(
                                                Icons.delete_outline,
                                                size: 18,
                                                color: Colors.red),
                                            tooltip: 'Eliminar Comentario',
                                            constraints: const BoxConstraints(),
                                            padding: EdgeInsets.zero,
                                            onPressed: () =>
                                                _confirmDelete(comment),
                                          ),
                                        ],
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 10),
                                  Text(
                                    comment.texto,
                                    style: const TextStyle(
                                      fontSize: 14,
                                      color: AppColors.textDark,
                                      height: 1.4,
                                    ),
                                  ),
                                ],
                              ),
                            );
                          },
                        ),
                    ],
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}
