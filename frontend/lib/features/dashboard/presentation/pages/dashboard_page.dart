import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../members/presentation/widgets/registration_drawer.dart';
import '../../../members/presentation/bloc/list/members_list_bloc.dart';
import '../../../members/presentation/bloc/list/members_list_event.dart';
import '../../../members/presentation/bloc/list/members_list_state.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  final _scrollController = ScrollController();
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
    return currentScroll >= (maxScroll * 0.9); // Cargar más al 90% del scroll
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _openDrawer(BuildContext context, {int? memberId}) {
    setState(() {
      _selectedMemberId = memberId;
    });
    // Scaffold.of(context) no funcionará si estamos fuera del builder del body
    // Por eso usamos GlobalKey o dependemos del Builder del FAB o AppBar.
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
          Builder(
            builder: (context) {
              return Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
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
                if (state.status == MembersListStatus.initial ||
                    (state.status == MembersListStatus.loading && state.members.isEmpty)) {
                  return const Center(child: CircularProgressIndicator());
                }

                if (state.status == MembersListStatus.failure && state.members.isEmpty) {
                  return Center(child: Text('Error: ${state.errorMessage}'));
                }

                if (state.members.isEmpty) {
                  return const Center(child: Text('No hay miembros registrados.'));
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
                            '${index + 1}', // Contador
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                        ),
                        title: Text(
                          member['nombre_completo'] ?? 'Sin Nombre',
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        subtitle: Text(member['correo_electronico'] ?? 'Sin correo'),
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
              },
            ),
          );
        },
      ),
    );
  }
}
