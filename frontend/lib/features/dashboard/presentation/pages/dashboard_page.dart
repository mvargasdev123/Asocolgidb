import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../members/presentation/widgets/registration_drawer.dart';
import '../../../members/presentation/bloc/list/members_list_bloc.dart';
import '../../../members/presentation/bloc/list/members_list_event.dart';
import '../../../members/presentation/bloc/list/members_list_state.dart';
import 'dashboard_metrics_view.dart';
import '../widgets/export_dialog.dart';
import '../widgets/import_dialog.dart';
import '../../../expedientes/presentation/pages/expedientes_list_page.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  final _scrollController = ScrollController();
  final _searchController = TextEditingController();
  int? _selectedMemberId;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
  }

  void _onScroll() {
    if (_isBottom) {
      context.read<MembersListBloc>().add(LoadMoreMembers());
    }
  }

  bool get _isBottom {
    if (!_scrollController.hasClients) return false;
    final maxScroll = _scrollController.position.maxScrollExtent;
    final currentScroll = _scrollController.offset;
    return currentScroll >= (maxScroll * 0.9);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    _searchController.dispose();
    super.dispose();
  }

  void _openDrawer(BuildContext context, {int? memberId}) {
    setState(() {
      _selectedMemberId = memberId;
    });
  }

  String _getRoleTag(Map<String, dynamic> member) {
    final bool esAsociado = member['es_asociado'] == true || member['datos_asociado'] != null;
    final bool esVoluntario = member['es_voluntario'] == true || member['datos_voluntario'] != null;

    if (esAsociado && esVoluntario) return 'AMBOS';
    if (esAsociado) return 'ASOCIADO';
    if (esVoluntario) return 'VOLUNTARIO';
    return 'EXTERNO';
  }

  Color _getRoleColor(String tag) {
    switch (tag) {
      case 'AMBOS':
        return Colors.purple.shade100;
      case 'ASOCIADO':
        return Colors.blue.shade100;
      case 'VOLUNTARIO':
        return Colors.amber.shade100;
      default:
        return Colors.grey.shade300;
    }
  }

  Widget _buildFilterSection(BuildContext context, MembersListState state) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.9),
        boxShadow: const [
          BoxShadow(
            color: Colors.black12,
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _searchController,
                  decoration: InputDecoration(
                    hintText: 'Buscar por nombre o documento...',
                    prefixIcon: const Icon(Icons.search, color: AppColors.primaryBlue),
                    suffixIcon: _searchController.text.isNotEmpty
                        ? IconButton(
                            icon: const Icon(Icons.clear, size: 20),
                            onPressed: () {
                              _searchController.clear();
                              context.read<MembersListBloc>().add(
                                    FilterMembers(query: ''),
                                  );
                            },
                          )
                        : null,
                    isDense: true,
                    contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10),
                      borderSide: BorderSide(color: Colors.grey.shade300),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10),
                      borderSide: const BorderSide(color: AppColors.primaryBlue, width: 2),
                    ),
                    filled: true,
                    fillColor: Colors.grey.shade50,
                  ),
                  onChanged: (val) {
                    context.read<MembersListBloc>().add(FilterMembers(query: val));
                  },
                ),
              ),
              if (state.hasActiveFilters) ...[
                const SizedBox(width: 8),
                Tooltip(
                  message: 'Limpiar Filtros',
                  child: TextButton.icon(
                    style: TextButton.styleFrom(
                      foregroundColor: AppColors.errorRed,
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                    ),
                    icon: const Icon(Icons.filter_alt_off, size: 18),
                    label: const Text('Limpiar'),
                    onPressed: () {
                      _searchController.clear();
                      context.read<MembersListBloc>().add(
                            FilterMembers(
                              query: '',
                              genero: 'TODOS',
                              rol: 'TODOS',
                              situacionAdmin: 'TODAS',
                            ),
                          );
                    },
                  ),
                ),
              ],
            ],
          ),
          const SizedBox(height: 10),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: [
                // Filtro Género
                _buildDropdownFilter(
                  label: 'Género',
                  value: state.generoFilter ?? 'TODOS',
                  items: const [
                    DropdownMenuItem(value: 'TODOS', child: Text('Género: Todos')),
                    DropdownMenuItem(value: 'Hombres', child: Text('Hombres')),
                    DropdownMenuItem(value: 'Mujeres', child: Text('Mujeres')),
                  ],
                  onChanged: (val) {
                    if (val != null) {
                      context.read<MembersListBloc>().add(FilterMembers(genero: val));
                    }
                  },
                ),
                const SizedBox(width: 10),
                // Filtro Rol
                _buildDropdownFilter(
                  label: 'Rol',
                  value: state.rolFilter ?? 'TODOS',
                  items: const [
                    DropdownMenuItem(value: 'TODOS', child: Text('Rol: Todos')),
                    DropdownMenuItem(value: 'Asociados', child: Text('Asociados')),
                    DropdownMenuItem(value: 'Voluntarios', child: Text('Voluntarios')),
                    DropdownMenuItem(value: 'Externos', child: Text('Externos')),
                  ],
                  onChanged: (val) {
                    if (val != null) {
                      context.read<MembersListBloc>().add(FilterMembers(rol: val));
                    }
                  },
                ),
                const SizedBox(width: 10),
                // Filtro Situación Admin
                _buildDropdownFilter(
                  label: 'Situación',
                  value: state.situacionAdminFilter ?? 'TODAS',
                  items: const [
                    DropdownMenuItem(value: 'TODAS', child: Text('Situación: Todas')),
                    DropdownMenuItem(value: 'Regulares', child: Text('Regulares')),
                    DropdownMenuItem(value: 'Irregulares', child: Text('Irregulares')),
                    DropdownMenuItem(value: 'En trámite', child: Text('En trámite')),
                  ],
                  onChanged: (val) {
                    if (val != null) {
                      context.read<MembersListBloc>().add(FilterMembers(situacionAdmin: val));
                    }
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDropdownFilter({
    required String label,
    required String value,
    required List<DropdownMenuItem<String>> items,
    required ValueChanged<String?> onChanged,
  }) {
    final bool isFiltered = value != 'TODOS' && value != 'TODAS';
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10),
      decoration: BoxDecoration(
        color: isFiltered ? AppColors.primaryBlue.withOpacity(0.1) : Colors.grey.shade100,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: isFiltered ? AppColors.primaryBlue : Colors.grey.shade300,
        ),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: value,
          items: items,
          onChanged: onChanged,
          isDense: true,
          style: TextStyle(
            fontSize: 13,
            fontWeight: isFiltered ? FontWeight.bold : FontWeight.normal,
            color: isFiltered ? AppColors.primaryBlue : Colors.black87,
          ),
          icon: Icon(
            Icons.arrow_drop_down,
            color: isFiltered ? AppColors.primaryBlue : Colors.grey.shade700,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      endDrawer: RegistrationDrawer(memberId: _selectedMemberId),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Image.asset(
          'assets/imagen-asocolgi/Logo-de-asocolgi.jpeg',
          height: 45,
        ),
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
            onPressed: () async {
              final result = await showDialog<bool>(
                context: context,
                builder: (_) => const ImportDialog(),
              );
              if (result == true && context.mounted) {
                context.read<MembersListBloc>().add(LoadInitialMembers());
              }
            },
          ),
          const SizedBox(width: 8),
          TextButton.icon(
            icon: const Icon(Icons.bar_chart, color: AppColors.primaryBlue),
            label: const Text(
              'Métricas',
              style: TextStyle(color: AppColors.primaryBlue, fontWeight: FontWeight.bold),
            ),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const DashboardMetricsView()),
              );
            },
          ),
          const SizedBox(width: 8),
          TextButton.icon(
            icon: const Icon(Icons.folder, color: Colors.purple),
            label: const Text(
              'Expedientes',
              style: TextStyle(color: Colors.purple, fontWeight: FontWeight.bold),
            ),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const ExpedientesListPage()),
              );
            },
          ),
          const SizedBox(width: 12),
          Builder(
            builder: (context) {
              return Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 8,
                  vertical: 8,
                ),
                child: ElevatedButton.icon(
                  icon: const Icon(Icons.add, size: 18),
                  label: const Text('Registrar Miembro'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryBlue,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  onPressed: () {
                    _openDrawer(context, memberId: null);
                    Scaffold.of(context).openEndDrawer();
                  },
                ),
              );
            },
          ),
          const SizedBox(width: 16),
        ],
      ),
      body: Builder(
        builder: (scaffoldContext) {
          return Container(
            decoration: const BoxDecoration(
              image: DecorationImage(
                image: AssetImage('assets/imagen-asocolgi/plantilla_baja.jpeg'),
                fit: BoxFit.cover,
              ),
            ),
            child: BlocBuilder<MembersListBloc, MembersListState>(
              builder: (context, state) {
                return Column(
                  children: [
                    _buildFilterSection(context, state),
                    Expanded(
                      child: _buildMemberListContent(scaffoldContext, state),
                    ),
                  ],
                );
              },
            ),
          );
        },
      ),
    );
  }

  Widget _buildMemberListContent(BuildContext scaffoldContext, MembersListState state) {
    if (state.status == MembersListStatus.initial ||
        (state.status == MembersListStatus.loading && state.members.isEmpty)) {
      return const Center(child: CircularProgressIndicator());
    }

    if (state.status == MembersListStatus.failure && state.members.isEmpty) {
      return Center(
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.9),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text('Error: ${state.errorMessage}'),
        ),
      );
    }

    if (state.members.isEmpty) {
      return Center(
        child: Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.9),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.search_off, size: 48, color: Colors.grey),
              const SizedBox(height: 8),
              const Text(
                'No se encontraron miembros con los filtros seleccionados.',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
              if (state.hasActiveFilters) ...[
                const SizedBox(height: 12),
                ElevatedButton.icon(
                  icon: const Icon(Icons.filter_alt_off),
                  label: const Text('Limpiar Filtros'),
                  onPressed: () {
                    _searchController.clear();
                    context.read<MembersListBloc>().add(
                          FilterMembers(
                            query: '',
                            genero: 'TODOS',
                            rol: 'TODOS',
                            situacionAdmin: 'TODAS',
                          ),
                        );
                  },
                ),
              ],
            ],
          ),
        ),
      );
    }

    return ListView.builder(
      controller: _scrollController,
      padding: const EdgeInsets.all(16),
      itemCount: state.hasReachedMax
          ? state.members.length
          : state.members.length + 1,
      itemBuilder: (context, index) {
        if (index >= state.members.length) {
          return const Center(
            child: Padding(
              padding: EdgeInsets.all(16),
              child: CircularProgressIndicator(),
            ),
          );
        }

        final member = state.members[index];
        final roleTag = _getRoleTag(member);
        final roleColor = _getRoleColor(roleTag);

        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          child: ListTile(
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 8,
            ),
            leading: CircleAvatar(
              backgroundColor: Colors.grey.shade200,
              child: Text(
                '${index + 1}',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
            title: Text(
              member['nombre_completo'] ?? 'Sin Nombre',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            subtitle: Text(
              '${member['correo_electronico'] ?? 'Sin correo'} | Doc: ${member['numero_documento'] ?? 'N/A'}',
            ),
            trailing: Container(
              padding: const EdgeInsets.symmetric(
                horizontal: 12,
                vertical: 6,
              ),
              decoration: BoxDecoration(
                color: roleColor,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Text(
                roleTag,
                style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            onTap: () {
              _openDrawer(context, memberId: member['id'] as int?);
              Scaffold.of(scaffoldContext).openEndDrawer();
            },
          ),
        );
      },
    );
  }
}

