import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/theme/app_colors.dart';
import '../../domain/models/member_registration_request.dart';
import '../../domain/repositories/member_repository.dart';
import '../../data/repositories/member_repository_impl.dart';
import '../bloc/registration/registration_bloc.dart';
import '../bloc/registration/registration_event.dart';
import '../bloc/registration/registration_state.dart';
import '../bloc/list/members_list_bloc.dart';
import '../bloc/list/members_list_event.dart';
import 'custom_dropdown_with_other.dart';
import 'section_header.dart';
import 'comments_section_widget.dart';

class RegistrationDrawer extends StatelessWidget {
  final int? memberId;
  const RegistrationDrawer({super.key, this.memberId});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      width: 550, // Ligeramente más ancho para la grilla
      child: BlocProvider<RegistrationBloc>(
        create: (context) {
          final bloc = RegistrationBloc(repository: context.read<MemberRepository>());
          if (memberId != null) {
            bloc.add(LoadMemberForEdit(memberId!));
          }
          return bloc;
        },
        child: _RegistrationForm(memberId: memberId),
      ),
    );
  }
}

class _RegistrationForm extends StatefulWidget {
  final int? memberId;
  const _RegistrationForm({this.memberId});

  @override
  State<_RegistrationForm> createState() => _RegistrationFormState();
}

class _RegistrationFormState extends State<_RegistrationForm> {
  final _formKey = GlobalKey<FormState>();
  bool _dataLoaded = false;

  // Controladores de Identificación
  String _tipoDoc = 'NIF/NIE';
  final _numIdentController = TextEditingController();
  String _nacionalidad = 'España';

  // Controladores de Datos Personales
  final _nombreController = TextEditingController();
  final _fechaNacController = TextEditingController();
  String _genero = 'M';
  final _correoController = TextEditingController();
  final _dirController = TextEditingController();
  final _cpController = TextEditingController();
  final _ciudadController = TextEditingController();

  // Controladores Situacion Social
  String _sitAdmin = 'Regular';
  final _unidadFamiliarController = TextEditingController();
  String _madreSoltera = 'No';
  String _violenciaGenero = 'No';
  String _nivelEducativo = 'Grado Medio';

  // Legal Acogida
  bool _tienePadron = false;
  final _fechaPadronController = TextEditingController();
  String _motivoConsulta = 'Otro';
  String _derivacion = 'Otro';
  String _tecnicaAcogida = 'Otro';
  bool _autorizaDatos = false;
  bool _autorizaImagen = false;

  // Contacto Emergencia
  final _emergenciaNombre = TextEditingController();
  final _emergenciaParentesco = TextEditingController();
  final _emergenciaTelefono = TextEditingController();

  // Asociado
  String _metodoPago = 'Efectivo';
  String _estadoMembresia = 'Activo';
  String _estadoPago = 'Al día';
  bool _autorizaWhatsapp = false;

  // Voluntario
  final _volCargo = TextEditingController();
  final _volCampo = TextEditingController();
  final _volTipo = TextEditingController();
  final _volHoras = TextEditingController();
  final _volUrlDoc = TextEditingController();
  final _volUrlCv = TextEditingController();
  bool _volCarta = false;
  bool _volFormulario = false;

  void _populateFromData(Map<String, dynamic> data) {
    if (_dataLoaded) return;
    _dataLoaded = true;
    setState(() {
      _numIdentController.text = data['numero_identificacion'] ?? '';
      _nombreController.text = data['nombre_completo'] ?? '';
      _fechaNacController.text = data['fecha_nacimiento'] ?? '';

      // Normalizar Género para evitar errores de DropdownButton
      final g = data['genero'];
      if (g == 'Masculino' || g == 'Hombre') {
        _genero = 'H';
      } else if (g == 'Femenino' || g == 'Mujer') {
        _genero = 'M';
      } else if (['M', 'H', 'LGTBI'].contains(g)) {
        _genero = g;
      } else {
        _genero = 'M';
      }

      _correoController.text = data['correo_electronico'] ?? '';
      _dirController.text = data['direccion_residencia'] ?? '';
      _cpController.text = data['codigo_postal'] ?? '';

      final sa = data['situacion_admin'];
      if (['Regular', 'Irregular', 'En tramite'].contains(sa)) {
        _sitAdmin = sa;
      }

      _unidadFamiliarController.text = data['unidad_familiar']?.toString() ?? '';

      final ms = data['madre_soltera'];
      if (['Si', 'No', 'N/A'].contains(ms)) _madreSoltera = ms;

      final vg = data['violencia_genero'];
      if (['Si', 'No', 'N/A'].contains(vg)) _violenciaGenero = vg;

      _tienePadron = data['tiene_padron'] == true;
      _fechaPadronController.text = data['fecha_padron'] ?? '';
      _autorizaDatos = data['autoriza_datos'] == true;
      _autorizaImagen = data['autoriza_imagen'] == true;
      _emergenciaNombre.text = data['contacto_emergencia_nombre'] ?? '';
      _emergenciaParentesco.text = data['contacto_emergencia_parentesco'] ?? '';
      _emergenciaTelefono.text = data['contacto_emergencia_telefono'] ?? '';

      if (data['datos_asociado'] is Map) {
        final da = data['datos_asociado'] as Map<String, dynamic>;
        final mp = da['metodo_pago'];
        if (['Efectivo', 'Transferencia'].contains(mp)) _metodoPago = mp;
        final em = da['estado_membresia'];
        if (['Activo', 'Inactivo', 'Renovado'].contains(em)) _estadoMembresia = em;
        final ep = da['estado_pago'];
        if (['Al día', 'Moroso'].contains(ep)) _estadoPago = ep;
        _autorizaWhatsapp = da['autoriza_whatsapp'] == true;
      }

      if (data['datos_voluntario'] is Map) {
        final dv = data['datos_voluntario'] as Map<String, dynamic>;
        _volCargo.text = dv['cargo'] ?? '';
        _volCampo.text = dv['campo_accion'] ?? '';
        _volTipo.text = dv['tipo'] ?? '';
        _volHoras.text = dv['horas_semana']?.toString() ?? '';
        _volUrlDoc.text = dv['url_doc'] ?? '';
        _volUrlCv.text = dv['url_cv'] ?? '';
        _volCarta = dv['carta_compromiso_firmada'] == true;
        _volFormulario = dv['formulario_inscripcion'] == true;
      }
    });
  }

  @override
  void dispose() {
    _numIdentController.dispose();
    _nombreController.dispose();
    _fechaNacController.dispose();
    _correoController.dispose();
    _dirController.dispose();
    _cpController.dispose();
    _ciudadController.dispose();
    _unidadFamiliarController.dispose();
    _fechaPadronController.dispose();
    _emergenciaNombre.dispose();
    _emergenciaParentesco.dispose();
    _emergenciaTelefono.dispose();
    _volCargo.dispose();
    _volCampo.dispose();
    _volTipo.dispose();
    _volHoras.dispose();
    _volUrlDoc.dispose();
    _volUrlCv.dispose();
    super.dispose();
  }

  Future<void> _selectDate(
    BuildContext context,
    TextEditingController controller,
  ) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(1900),
      lastDate: DateTime(2100),
    );
    if (picked != null) {
      setState(() {
        controller.text =
            "${picked.year}-${picked.month.toString().padLeft(2, '0')}-${picked.day.toString().padLeft(2, '0')}";
      });
    }
  }

  void _submit() {
    if (_formKey.currentState!.validate()) {
      final state = context.read<RegistrationBloc>().state;

      final request = MemberRegistrationRequest(
        identificacion: Identificacion(
          tipoDocumento: _tipoDoc,
          numeroIdentificacion: _numIdentController.text.trim(),
          nacionalidad: _nacionalidad,
        ),
        datosPersonales: DatosPersonales(
          nombreCompleto: _nombreController.text.trim(),
          fechaNacimiento: _fechaNacController.text.isNotEmpty
              ? _fechaNacController.text
              : null,
          genero: _genero,
          correoElectronico: _correoController.text.isNotEmpty
              ? _correoController.text
              : null,
          direccionResidencia: _dirController.text.isNotEmpty
              ? _dirController.text
              : null,
          codigoPostal: _cpController.text.isNotEmpty
              ? _cpController.text
              : null,
          ciudad: _ciudadController.text.isNotEmpty
              ? _ciudadController.text
              : null,
        ),
        situacionSocial: SituacionSocial(
          situacionAdmin: _sitAdmin,
          unidadFamiliar: int.tryParse(_unidadFamiliarController.text),
          madreSoltera: _madreSoltera,
          violenciaGenero: _violenciaGenero,
          nivelEducativo: _nivelEducativo,
        ),
        legalAcogida: LegalAcogida(
          tienePadron: _tienePadron,
          fechaPadron: _tienePadron && _fechaPadronController.text.isNotEmpty
              ? _fechaPadronController.text
              : null,
          motivoConsulta: _motivoConsulta,
          derivacion: _derivacion,
          tecnicaAcogida: _tecnicaAcogida,
          autorizaDatos: _autorizaDatos,
          autorizaImagen: _autorizaImagen,
        ),
        contactoEmergencia: ContactoEmergencia(
          nombre: _emergenciaNombre.text.isNotEmpty
              ? _emergenciaNombre.text
              : null,
          parentesco: _emergenciaParentesco.text.isNotEmpty
              ? _emergenciaParentesco.text
              : null,
          telefono: _emergenciaTelefono.text.isNotEmpty
              ? _emergenciaTelefono.text
              : null,
        ),
        esAsociado: state.isAsociado,
        datosAsociado: state.isAsociado
            ? DatosAsociado(
                metodoPago: _metodoPago,
                estadoMembresia: _estadoMembresia,
                estadoPago: _estadoPago,
                autorizaWhatsapp: _autorizaWhatsapp,
              )
            : null,
        esVoluntario: state.isVoluntario,
        datosVoluntario: state.isVoluntario
            ? DatosVoluntario(
                cargo: _volCargo.text.isNotEmpty ? _volCargo.text : null,
                campoAccion: _volCampo.text.isNotEmpty ? _volCampo.text : null,
                tipo: _volTipo.text.isNotEmpty ? _volTipo.text : null,
                horasSemana: int.tryParse(_volHoras.text),
                urlDoc: _volUrlDoc.text.isNotEmpty ? _volUrlDoc.text : null,
                urlCv: _volUrlCv.text.isNotEmpty ? _volUrlCv.text : null,
                cartaCompromisoFirmada: _volCarta,
                formularioInscripcion: _volFormulario,
              )
            : null,
      );

      if (widget.memberId != null) {
        context.read<RegistrationBloc>().add(
              UpdateRegistration(widget.memberId!, request),
            );
      } else {
        context.read<RegistrationBloc>().add(SubmitRegistration(request));
      }
    }
  }

  void _confirmDelete(BuildContext mainContext) {
    showDialog(
      context: mainContext,
      builder: (dialogCtx) => AlertDialog(
        title: const Text('Confirmar Eliminación'),
        content: const Text(
          '¿Estás seguro de que deseas eliminar este miembro? Esta acción realizará un borrado lógico y el usuario ya no aparecerá en el listado activo.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogCtx),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppColors.errorRed),
            onPressed: () {
              Navigator.pop(dialogCtx);
              mainContext.read<RegistrationBloc>().add(
                    DeleteMemberRequested(widget.memberId!),
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
    return BlocListener<RegistrationBloc, RegistrationState>(
      listener: (context, state) {
        if (state.status == RegistrationStatus.editLoaded && state.memberData != null) {
          _populateFromData(state.memberData!);
        } else if (state.status == RegistrationStatus.failureConflict) {
          showDialog(
            context: context,
            builder: (_) => AlertDialog(
              title: const Text('Conflicto'),
              content: Text(state.errorMessage ?? 'Esta persona ya existe'),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Cerrar'),
                ),
              ],
            ),
          );
        } else if (state.status == RegistrationStatus.success) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(widget.memberId != null
                  ? 'Miembro actualizado correctamente'
                  : 'Registro Exitoso'),
              backgroundColor: Colors.green,
            ),
          );
          // Refrescar la lista de miembros en tiempo real
          context.read<MembersListBloc>().add(LoadInitialMembers());
          Navigator.pop(context);
        } else if (state.status == RegistrationStatus.deleteSuccess) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Miembro eliminado exitosamente'),
              backgroundColor: Colors.orange,
            ),
          );
          // Refrescar la lista de miembros en tiempo real
          context.read<MembersListBloc>().add(LoadInitialMembers());
          Navigator.pop(context);
        } else if (state.status == RegistrationStatus.failureGeneric) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Error: ${state.errorMessage}'),
              backgroundColor: AppColors.errorRed,
            ),
          );
        }
      },
      child: Column(
        children: [
          // Header Azul
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
            color: AppColors.primaryBlue,
            child: Row(
              children: [
                Icon(
                  widget.memberId != null ? Icons.edit : Icons.person_add,
                  color: Colors.white,
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Text(
                    widget.memberId != null
                        ? 'Editar Miembro #${widget.memberId}'
                        : 'Nuevo Registro Principal',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close, color: Colors.white),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),
          ),

          // Formulario
          Expanded(
            child: Form(
              key: _formKey,
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(24),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // 1. IDENTIFICACIÓN
                    const SectionHeader(
                      title: '1. IDENTIFICACIÓN',
                      icon: Icons.badge,
                    ),
                    Row(
                      children: [
                        Expanded(
                          child: CustomDropdownWithOther(
                            label: 'Tipo Doc',
                            icon: Icons.badge_outlined,
                            options: const ['NIF/NIE', 'Pasaporte'],
                            initialValue: _tipoDoc,
                            onChanged: (val) => _tipoDoc = val,
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          flex: 2,
                          child: TextFormField(
                            controller: _numIdentController,
                            decoration: const InputDecoration(
                              labelText: 'Número Identificación *',
                              prefixIcon: Icon(Icons.tag),
                            ),
                            validator: (val) =>
                                val == null || val.isEmpty ? 'Requerido' : null,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    CustomDropdownWithOther(
                      label: 'Nacionalidad',
                      icon: Icons.flag,
                      options: const [
                        'España',
                        'Colombia',
                        'Ecuador',
                        'Perú',
                        'Venezuela',
                      ],
                      initialValue: _nacionalidad,
                      onChanged: (val) => _nacionalidad = val,
                    ),

                    // 2. DATOS PERSONALES
                    const SectionHeader(
                      title: '2. DATOS PERSONALES',
                      icon: Icons.person,
                    ),
                    TextFormField(
                      controller: _nombreController,
                      decoration: const InputDecoration(
                        labelText: 'Nombre Completo *',
                        prefixIcon: Icon(Icons.person_outline),
                      ),
                      validator: (val) =>
                          val == null || val.isEmpty ? 'Requerido' : null,
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        Expanded(
                          child: TextFormField(
                            controller: _fechaNacController,
                            readOnly: true,
                            decoration: const InputDecoration(
                              labelText: 'Fecha Nacimiento',
                              prefixIcon: Icon(Icons.calendar_today),
                            ),
                            onTap: () =>
                                _selectDate(context, _fechaNacController),
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: DropdownButtonFormField<String>(
                            value: _genero,
                            decoration: const InputDecoration(
                              labelText: 'Género',
                              prefixIcon: Icon(Icons.wc),
                            ),
                            items: const [
                              DropdownMenuItem(value: 'M', child: Text('M')),
                              DropdownMenuItem(value: 'H', child: Text('H')),
                              DropdownMenuItem(
                                value: 'LGTBI',
                                child: Text('LGTBI'),
                              ),
                            ],
                            onChanged: (val) => setState(() => _genero = val!),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _correoController,
                      decoration: const InputDecoration(
                        labelText: 'Correo Electrónico',
                        prefixIcon: Icon(Icons.email),
                      ),
                    ),

                    // 3. SITUACIÓN SOCIAL
                    const SectionHeader(
                      title: '3. SITUACIÓN SOCIAL',
                      icon: Icons.family_restroom,
                    ),
                    Row(
                      children: [
                        Expanded(
                          flex: 2,
                          child: CustomDropdownWithOther(
                            label: 'Situación Administrativa',
                            icon: Icons.gavel,
                            options: const [
                              'Regular',
                              'Irregular',
                              'En tramite',
                            ],
                            initialValue: _sitAdmin,
                            onChanged: (val) => _sitAdmin = val,
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: TextFormField(
                            controller: _unidadFamiliarController,
                            keyboardType: TextInputType.number,
                            decoration: const InputDecoration(
                              labelText: 'Unidad Familiar',
                              prefixIcon: Icon(Icons.group),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        Expanded(
                          child: DropdownButtonFormField<String>(
                            value: _madreSoltera,
                            decoration: const InputDecoration(
                              labelText: 'Madre Soltera',
                            ),
                            items: ['Si', 'No', 'N/A']
                                .map(
                                  (e) => DropdownMenuItem(
                                    value: e,
                                    child: Text(e),
                                  ),
                                )
                                .toList(),
                            onChanged: (val) =>
                                setState(() => _madreSoltera = val!),
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: DropdownButtonFormField<String>(
                            value: _violenciaGenero,
                            decoration: const InputDecoration(
                              labelText: 'Violencia Género',
                            ),
                            items: ['Si', 'No', 'N/A']
                                .map(
                                  (e) => DropdownMenuItem(
                                    value: e,
                                    child: Text(e),
                                  ),
                                )
                                .toList(),
                            onChanged: (val) =>
                                setState(() => _violenciaGenero = val!),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    CustomDropdownWithOther(
                      label: 'Nivel Educativo',
                      icon: Icons.school,
                      options: const [
                        'Sin estudios',
                        'Primaria',
                        'Grado Medio',
                        'Universidad',
                      ],
                      initialValue: _nivelEducativo,
                      onChanged: (val) => _nivelEducativo = val,
                    ),

                    // 4. LEGAL / ACOGIDA
                    const SectionHeader(
                      title: '4. LEGAL / ACOGIDA',
                      icon: Icons.gavel,
                    ),
                    SwitchListTile(
                      title: const Text('¿Tiene Padrón?'),
                      value: _tienePadron,
                      activeColor: AppColors.primaryBlue,
                      onChanged: (val) {
                        setState(() {
                          _tienePadron = val;
                          if (!val) _fechaPadronController.clear();
                        });
                      },
                    ),
                    if (_tienePadron)
                      Padding(
                        padding: const EdgeInsets.only(bottom: 16.0),
                        child: TextFormField(
                          controller: _fechaPadronController,
                          readOnly: true,
                          decoration: const InputDecoration(
                            labelText: 'Fecha de Padrón',
                            prefixIcon: Icon(Icons.date_range),
                          ),
                          onTap: () =>
                              _selectDate(context, _fechaPadronController),
                        ),
                      ),

                    CustomDropdownWithOther(
                      label: 'Motivo Consulta',
                      icon: Icons.question_answer,
                      options: const [],
                      initialValue: _motivoConsulta,
                      onChanged: (val) => _motivoConsulta = val,
                    ),
                    const SizedBox(height: 16),
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          child: CustomDropdownWithOther(
                            label: 'Derivación',
                            icon: Icons.alt_route,
                            options: const [],
                            initialValue: _derivacion,
                            onChanged: (val) => _derivacion = val,
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: CustomDropdownWithOther(
                            label: 'Técnica Acogida',
                            icon: Icons.psychology,
                            options: const [],
                            initialValue: _tecnicaAcogida,
                            onChanged: (val) => _tecnicaAcogida = val,
                          ),
                        ),
                      ],
                    ),

                    // 5. CONTACTO DE EMERGENCIA
                    const SectionHeader(
                      title: '5. CONTACTO DE EMERGENCIA',
                      icon: Icons.emergency,
                    ),
                    TextFormField(
                      controller: _emergenciaNombre,
                      decoration: const InputDecoration(
                        labelText: 'Nombre del Contacto',
                        prefixIcon: Icon(Icons.person),
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        Expanded(
                          child: TextFormField(
                            controller: _emergenciaParentesco,
                            decoration: const InputDecoration(
                              labelText: 'Parentesco',
                              prefixIcon: Icon(Icons.family_restroom),
                            ),
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: TextFormField(
                            controller: _emergenciaTelefono,
                            keyboardType: TextInputType.phone,
                            decoration: const InputDecoration(
                              labelText: 'Teléfono',
                              prefixIcon: Icon(Icons.phone),
                            ),
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 32),

                    // 6 y 7
                    BlocBuilder<RegistrationBloc, RegistrationState>(
                      builder: (context, state) {
                        return Column(
                          children: [
                            const SectionHeader(
                              title: '6. ASOCIADO',
                              icon: Icons.card_membership,
                            ),
                            Container(
                              decoration: BoxDecoration(
                                border: Border.all(
                                  color: AppColors.primaryBlue,
                                ),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              padding: const EdgeInsets.all(16),
                              child: Column(
                                children: [
                                  CheckboxListTile(
                                    contentPadding: EdgeInsets.zero,
                                    title: const Text(
                                      'Registrar como Asociado',
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    value: state.isAsociado,
                                    onChanged: (val) => context
                                        .read<RegistrationBloc>()
                                        .add(ToggleAsociado(val ?? false)),
                                    activeColor: AppColors.primaryBlue,
                                  ),
                                  if (state.isAsociado) ...[
                                    const SizedBox(height: 16),
                                    Row(
                                      children: [
                                        Expanded(
                                          child:
                                              DropdownButtonFormField<String>(
                                                value: _estadoMembresia,
                                                decoration:
                                                    const InputDecoration(
                                                      labelText:
                                                          'Estado Membresía',
                                                    ),
                                                items:
                                                    [
                                                          'Activo',
                                                          'Inactivo',
                                                          'Renovado',
                                                        ]
                                                        .map(
                                                          (e) =>
                                                              DropdownMenuItem(
                                                                value: e,
                                                                child: Text(e),
                                                              ),
                                                        )
                                                        .toList(),
                                                onChanged: (val) => setState(
                                                  () => _estadoMembresia = val!,
                                                ),
                                              ),
                                        ),
                                        const SizedBox(width: 16),
                                        Expanded(
                                          child:
                                              DropdownButtonFormField<String>(
                                                value: _estadoPago,
                                                decoration:
                                                    const InputDecoration(
                                                      labelText: 'Estado Pago',
                                                    ),
                                                items: ['Al día', 'Moroso']
                                                    .map(
                                                      (e) => DropdownMenuItem(
                                                        value: e,
                                                        child: Text(e),
                                                      ),
                                                    )
                                                    .toList(),
                                                onChanged: (val) => setState(
                                                  () => _estadoPago = val!,
                                                ),
                                              ),
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: 16),
                                    DropdownButtonFormField<String>(
                                      value: _metodoPago,
                                      decoration: const InputDecoration(
                                        labelText: 'Método de Pago',
                                      ),
                                      items: ['Efectivo', 'Transferencia']
                                          .map(
                                            (e) => DropdownMenuItem(
                                              value: e,
                                              child: Text(e),
                                            ),
                                          )
                                          .toList(),
                                      onChanged: (val) => _metodoPago = val!,
                                    ),
                                    SwitchListTile(
                                      contentPadding: EdgeInsets.zero,
                                      title: const Text(
                                        'Autoriza recibir WhatsApp',
                                      ),
                                      value: _autorizaWhatsapp,
                                      activeColor: AppColors.primaryBlue,
                                      onChanged: (val) => setState(
                                        () => _autorizaWhatsapp = val,
                                      ),
                                    ),
                                  ],
                                ],
                              ),
                            ),

                            const SizedBox(height: 24),

                            const SectionHeader(
                              title: '7. VOLUNTARIO',
                              icon: Icons.volunteer_activism,
                            ),
                            Container(
                              decoration: BoxDecoration(
                                border: Border.all(
                                  color: AppColors.primaryYellow,
                                ),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              padding: const EdgeInsets.all(16),
                              child: Column(
                                children: [
                                  CheckboxListTile(
                                    contentPadding: EdgeInsets.zero,
                                    title: const Text(
                                      'Registrar como Voluntario',
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    value: state.isVoluntario,
                                    onChanged: (val) => context
                                        .read<RegistrationBloc>()
                                        .add(ToggleVoluntario(val ?? false)),
                                    activeColor: AppColors.primaryYellow,
                                  ),
                                  if (state.isVoluntario) ...[
                                    const SizedBox(height: 16),
                                    Row(
                                      children: [
                                        Expanded(
                                          child: TextFormField(
                                            controller: _volCargo,
                                            decoration: const InputDecoration(
                                              labelText: 'Cargo',
                                              prefixIcon: Icon(
                                                Icons.work_outline,
                                              ),
                                            ),
                                          ),
                                        ),
                                        const SizedBox(width: 16),
                                        Expanded(
                                          child: TextFormField(
                                            controller: _volCampo,
                                            decoration: const InputDecoration(
                                              labelText: 'Campo de Acción',
                                              prefixIcon: Icon(
                                                Icons.category_outlined,
                                              ),
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: 16),
                                    Row(
                                      children: [
                                        Expanded(
                                          flex: 2,
                                          child: TextFormField(
                                            controller: _volTipo,
                                            decoration: const InputDecoration(
                                              labelText: 'Tipo (Opcional)',
                                              prefixIcon: Icon(
                                                Icons.label_outline,
                                              ),
                                            ),
                                          ),
                                        ),
                                        const SizedBox(width: 16),
                                        Expanded(
                                          child: TextFormField(
                                            controller: _volHoras,
                                            keyboardType: TextInputType.number,
                                            decoration: const InputDecoration(
                                              labelText: 'Horas / Semana',
                                              prefixIcon: Icon(Icons.schedule),
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: 16),
                                    Row(
                                      children: [
                                        Expanded(
                                          child: TextFormField(
                                            controller: _volUrlDoc,
                                            decoration: const InputDecoration(
                                              labelText: 'URL Doc (Opcional)',
                                              prefixIcon: Icon(Icons.link),
                                            ),
                                          ),
                                        ),
                                        const SizedBox(width: 16),
                                        Expanded(
                                          child: TextFormField(
                                            controller: _volUrlCv,
                                            decoration: const InputDecoration(
                                              labelText: 'URL CV (Opcional)',
                                              prefixIcon: Icon(Icons.link),
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: 16),
                                    CheckboxListTile(
                                      contentPadding: EdgeInsets.zero,
                                      title: const Text(
                                        'Carta Compromiso Firmada',
                                      ),
                                      value: _volCarta,
                                      controlAffinity:
                                          ListTileControlAffinity.leading,
                                      onChanged: (val) =>
                                          setState(() => _volCarta = val!),
                                    ),
                                    CheckboxListTile(
                                      contentPadding: EdgeInsets.zero,
                                      title: const Text(
                                        'Formulario de Inscripción',
                                      ),
                                      value: _volFormulario,
                                      controlAffinity:
                                          ListTileControlAffinity.leading,
                                      onChanged: (val) =>
                                          setState(() => _volFormulario = val!),
                                    ),
                                  ],
                                ],
                              ),
                            ),
                          ],
                        );
                      },
                    ),
                    if (widget.memberId != null) ...[
                      CommentsSectionWidget(idPersona: widget.memberId!),
                    ],
                    const SizedBox(height: 100),
                  ],
                ),
              ),
            ),
          ),

          // Bottom Actions
          Container(
            padding: const EdgeInsets.all(16),
            decoration: const BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.black12,
                  blurRadius: 4,
                  offset: Offset(0, -2),
                ),
              ],
            ),
            child: BlocBuilder<RegistrationBloc, RegistrationState>(
              builder: (context, state) {
                return Row(
                  children: [
                    if (widget.memberId != null) ...[
                      IconButton(
                        icon: const Icon(Icons.delete_forever, color: Colors.red),
                        tooltip: 'Eliminar Miembro',
                        onPressed: () => _confirmDelete(context),
                      ),
                      const SizedBox(width: 8),
                    ],
                    Expanded(
                      child: OutlinedButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text('Cancelar'),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      flex: 2,
                      child: ElevatedButton(
                        onPressed: state.status == RegistrationStatus.loading
                            ? null
                            : _submit,
                        child: state.status == RegistrationStatus.loading
                            ? const SizedBox(
                                height: 20,
                                width: 20,
                                child: CircularProgressIndicator(
                                  color: Colors.white,
                                  strokeWidth: 2,
                                ),
                              )
                            : Text(widget.memberId != null ? 'Guardar Cambios' : 'Guardar Miembro'),
                      ),
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
