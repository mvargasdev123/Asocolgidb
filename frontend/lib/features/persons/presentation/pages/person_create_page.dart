import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../domain/entities/person.dart';
import '../providers/person_list_provider.dart';

class PersonCreatePage extends ConsumerStatefulWidget {
  const PersonCreatePage({super.key});

  @override
  ConsumerState<PersonCreatePage> createState() => _PersonCreatePageState();
}

class _PersonCreatePageState extends ConsumerState<PersonCreatePage> {
  final _formKey = GlobalKey<FormState>();
  
  String _name = '';
  int _idTipoDocumento = 1; // 1 = CC por default (Simulado)
  String _numeroDocumento = '';
  String _email = '';
  DateTime? _birthDate;
  String _address = '';
  
  bool _proteccionDatos = false;
  bool _manejoImagen = false;
  DateTime? _fechaIngreso = DateTime.now(); // Por defecto hoy
  
  PersonRole _role = PersonRole.externo;
  String _notes = '';
  
  bool _isLoading = false;

  void _submit() async {
    if (!_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Por favor, revisa los campos en rojo.')));
      return;
    }
    if (_birthDate == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Por favor selecciona la fecha de nacimiento.')));
      return;
    }
    
    _formKey.currentState!.save();
    setState(() => _isLoading = true);
    
    try {
      final newPerson = PersonCreateEntity(
        fullName: _name,
        email: _email,
        birthDate: _birthDate!,
        address: _address,
        idTipoDocumento: _idTipoDocumento,
        numeroDocumento: _numeroDocumento,
        proteccionDatos: _proteccionDatos,
        manejoImagen: _manejoImagen,
        fechaIngreso: _fechaIngreso,
        role: _role,
        notes: _notes,
      );
      
      await ref.read(personListProvider.notifier).createPerson(newPerson);
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text('Persona registrada con éxito', style: TextStyle(color: Colors.white)), 
          backgroundColor: Colors.teal
        ));
        context.pop();
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString()), backgroundColor: Colors.redAccent));
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Registrar Nuevo Miembro'),
        backgroundColor: Colors.white,
        elevation: 0.5,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _buildSectionCard(
                title: 'Información Personal',
                icon: Icons.person_outline,
                children: [
                  _buildTextField('Nombre Completo', Icons.badge_outlined, (val) => _name = val, required: true),
                  const SizedBox(height: 16),
                  _buildTextField('Correo Electrónico', Icons.email_outlined, (val) => _email = val, required: true, isEmail: true),
                  const SizedBox(height: 16),
                  _buildDatePicker('Fecha de Nacimiento', _birthDate, (date) => setState(() => _birthDate = date), Icons.cake_outlined),
                  const SizedBox(height: 16),
                  _buildTextField('Dirección', Icons.home_outlined, (val) => _address = val, required: false),
                ],
              ),
              
              _buildSectionCard(
                title: 'Identificación',
                icon: Icons.credit_card_outlined,
                children: [
                  DropdownButtonFormField<int>(
                    initialValue: _idTipoDocumento,
                    decoration: _buildInputDecoration('Tipo de Documento', Icons.assignment_ind_outlined),
                    items: const [
                      DropdownMenuItem(value: 1, child: Text('Cédula de Ciudadanía')),
                      DropdownMenuItem(value: 2, child: Text('Tarjeta de Identidad')),
                      DropdownMenuItem(value: 3, child: Text('Cédula de Extranjería')),
                    ],
                    onChanged: (val) => setState(() => _idTipoDocumento = val!),
                  ),
                  const SizedBox(height: 16),
                  _buildTextField('Número de Documento', Icons.numbers_outlined, (val) => _numeroDocumento = val, required: true),
                ],
              ),
              
              _buildSectionCard(
                title: 'Términos y Asignación',
                icon: Icons.gavel_outlined,
                children: [
                  _buildDatePicker('Fecha de Ingreso', _fechaIngreso, (date) => setState(() => _fechaIngreso = date), Icons.calendar_month_outlined),
                  const SizedBox(height: 16),
                  DropdownButtonFormField<PersonRole>(
                    initialValue: _role,
                    decoration: _buildInputDecoration('Rol en Asocolgi', Icons.work_outline),
                    items: PersonRole.values.map((r) => DropdownMenuItem(
                      value: r, 
                      child: Text(r.toString().split('.').last.toUpperCase()),
                    )).toList(),
                    onChanged: (val) => setState(() => _role = val!),
                  ),
                  const SizedBox(height: 16),
                  CheckboxListTile(
                    title: const Text('Autoriza Tratamiento de Datos'),
                    value: _proteccionDatos,
                    onChanged: (val) => setState(() => _proteccionDatos = val!),
                    activeColor: Colors.teal,
                    controlAffinity: ListTileControlAffinity.leading,
                    contentPadding: EdgeInsets.zero,
                  ),
                  CheckboxListTile(
                    title: const Text('Autoriza Uso de Imagen'),
                    value: _manejoImagen,
                    onChanged: (val) => setState(() => _manejoImagen = val!),
                    activeColor: Colors.teal,
                    controlAffinity: ListTileControlAffinity.leading,
                    contentPadding: EdgeInsets.zero,
                  ),
                ],
              ),
              
              _buildSectionCard(
                title: 'Comentarios / Notas',
                icon: Icons.notes_outlined,
                children: [
                  TextFormField(
                    decoration: _buildInputDecoration('Escribe notas adicionales aquí...', Icons.comment_outlined),
                    maxLines: 5,
                    onSaved: (val) => _notes = val ?? '',
                  ),
                ],
              ),
              
              const SizedBox(height: 20),
              
              SizedBox(
                height: 55,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _submit,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.teal,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  child: _isLoading 
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text('GUARDAR REGISTRO', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, letterSpacing: 1)),
                ),
              ),
              const SizedBox(height: 40),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionCard({required String title, required IconData icon, required List<Widget> children}) {
    return Card(
      margin: const EdgeInsets.only(bottom: 20),
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                Icon(icon, color: Colors.teal),
                const SizedBox(width: 10),
                Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black87)),
              ],
            ),
            const Divider(height: 30),
            ...children,
          ],
        ),
      ),
    );
  }

  Widget _buildTextField(String label, IconData icon, Function(String) onSaved, {bool required = false, bool isEmail = false}) {
    return TextFormField(
      decoration: _buildInputDecoration(label, icon),
      keyboardType: isEmail ? TextInputType.emailAddress : TextInputType.text,
      validator: (value) {
        if (required && (value == null || value.trim().isEmpty)) return 'Este campo es obligatorio';
        if (isEmail && value != null && value.isNotEmpty && !value.contains('@')) return 'Ingresa un correo válido';
        return null;
      },
      onSaved: (val) => onSaved(val ?? ''),
    );
  }

  Widget _buildDatePicker(String label, DateTime? currentDate, Function(DateTime) onPicked, IconData icon) {
    return InkWell(
      onTap: () async {
        final picked = await showDatePicker(
          context: context,
          initialDate: currentDate ?? DateTime.now().subtract(const Duration(days: 365 * 18)),
          firstDate: DateTime(1900),
          lastDate: DateTime.now().add(const Duration(days: 365)), // Por si es fecha ingreso futura
        );
        if (picked != null) onPicked(picked);
      },
      child: InputDecorator(
        decoration: _buildInputDecoration(label, icon),
        child: Text(
          currentDate == null ? 'Seleccionar fecha' : "${currentDate.day}/${currentDate.month}/${currentDate.year}",
          style: TextStyle(color: currentDate == null ? Colors.grey.shade600 : Colors.black87, fontSize: 16),
        ),
      ),
    );
  }

  InputDecoration _buildInputDecoration(String label, IconData icon) {
    return InputDecoration(
      labelText: label,
      prefixIcon: Icon(icon, color: Colors.teal),
      filled: true,
      fillColor: Colors.grey.shade50,
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide(color: Colors.grey.shade300)),
      enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide(color: Colors.grey.shade300)),
      focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Colors.teal, width: 2)),
    );
  }
}
