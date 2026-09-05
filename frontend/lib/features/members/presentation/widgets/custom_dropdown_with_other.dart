import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';

class CustomDropdownWithOther extends StatefulWidget {
  final String label;
  final IconData icon;
  final List<String> options;
  final String? initialValue;
  final void Function(String) onChanged;

  const CustomDropdownWithOther({
    super.key,
    required this.label,
    required this.icon,
    required this.options,
    required this.onChanged,
    this.initialValue,
  });

  @override
  State<CustomDropdownWithOther> createState() =>
      _CustomDropdownWithOtherState();
}

class _CustomDropdownWithOtherState extends State<CustomDropdownWithOther> {
  String? _selectedValue;
  bool _isOther = false;
  final TextEditingController _otherController = TextEditingController();

  @override
  void initState() {
    super.initState();
    if (widget.initialValue != null) {
      if (widget.options.contains(widget.initialValue)) {
        _selectedValue = widget.initialValue;
      } else {
        _selectedValue = 'Otro';
        _isOther = true;
        _otherController.text = widget.initialValue!;
      }
    }
  }

  @override
  void dispose() {
    _otherController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        DropdownButtonFormField<String>(
          value: _selectedValue,
          isExpanded: true,
          decoration: InputDecoration(
            labelText: widget.label,
            prefixIcon: Icon(widget.icon),
          ),
          items: [
            ...widget.options.map(
              (e) => DropdownMenuItem(value: e, child: Text(e)),
            ),
            const DropdownMenuItem(
              value: 'Otro',
              child: Text('Otro (Especificar)'),
            ),
          ],
          onChanged: (val) {
            setState(() {
              _selectedValue = val;
              _isOther = val == 'Otro';
            });
            if (!_isOther && val != null) {
              widget.onChanged(val);
            }
          },
        ),
        if (_isOther) ...[
          const SizedBox(height: 8),
          TextFormField(
            controller: _otherController,
            decoration: InputDecoration(
              labelText: 'Especifique ${widget.label.toLowerCase()}',
              prefixIcon: const Icon(Icons.edit),
            ),
            onChanged: widget.onChanged,
            validator: (value) {
              if (value == null || value.isEmpty)
                return 'Requerido si selecciona Otro';
              return null;
            },
          ),
        ],
      ],
    );
  }
}
