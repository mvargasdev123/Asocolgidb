class Identificacion {
  final String tipoDocumento;
  final String numeroIdentificacion; // Obligatorio
  final String? nacionalidad;

  Identificacion({
    required this.tipoDocumento,
    required this.numeroIdentificacion,
    this.nacionalidad,
  });

  Map<String, dynamic> toJson() => {
    'tipo_documento': tipoDocumento,
    'numero_identificacion': numeroIdentificacion,
    'nacionalidad': nacionalidad,
  };
}

class DatosPersonales {
  final String nombreCompleto; // Obligatorio
  final String? fechaNacimiento;
  final String? fechaAtencion;
  final String? telefonoPrincipal;
  final String? genero;
  final String? correoElectronico;
  final String? direccionResidencia;
  final String? codigoPostal;
  final String? ciudad;

  DatosPersonales({
    required this.nombreCompleto,
    this.fechaNacimiento,
    this.fechaAtencion,
    this.telefonoPrincipal,
    this.genero,
    this.correoElectronico,
    this.direccionResidencia,
    this.codigoPostal,
    this.ciudad,
  });

  Map<String, dynamic> toJson() => {
    'nombre_completo': nombreCompleto,
    'fecha_nacimiento': fechaNacimiento,
    'fecha_atencion': fechaAtencion,
    'telefono_principal': telefonoPrincipal,
    'genero': genero,
    'correo_electronico': correoElectronico,
    'direccion_residencia': direccionResidencia,
    'codigo_postal': codigoPostal,
    'ciudad': ciudad,
  };
}

class SituacionSocial {
  final String? situacionAdmin;
  final int? unidadFamiliar;
  final String? madreSoltera;
  final String? violenciaGenero;
  final String? nivelEducativo;

  SituacionSocial({
    this.situacionAdmin,
    this.unidadFamiliar,
    this.madreSoltera,
    this.violenciaGenero,
    this.nivelEducativo,
  });

  Map<String, dynamic> toJson() => {
    'situacion_admin': situacionAdmin,
    'unidad_familiar': unidadFamiliar,
    'madre_soltera': madreSoltera,
    'violencia_genero': violenciaGenero,
    'nivel_educativo': nivelEducativo,
  };
}

class LegalAcogida {
  final bool? tienePadron;
  final String? fechaPadron;
  final String? motivoConsulta;
  final String? derivacion;
  final String? tecnicaAcogida;
  final bool? autorizaDatos;
  final bool? autorizaImagen;

  LegalAcogida({
    this.tienePadron,
    this.fechaPadron,
    this.motivoConsulta,
    this.derivacion,
    this.tecnicaAcogida,
    this.autorizaDatos,
    this.autorizaImagen,
  });

  Map<String, dynamic> toJson() => {
    'tiene_padron': tienePadron,
    'fecha_padron': fechaPadron,
    'motivo_consulta': motivoConsulta,
    'derivacion': derivacion,
    'tecnica_acogida': tecnicaAcogida,
    'autoriza_datos': autorizaDatos,
    'autoriza_imagen': autorizaImagen,
  };
}

class ContactoEmergencia {
  final String? nombre;
  final String? parentesco;
  final String? telefono;

  ContactoEmergencia({this.nombre, this.parentesco, this.telefono});

  Map<String, dynamic> toJson() => {
    'nombre': nombre,
    'parentesco': parentesco,
    'telefono': telefono,
  };
}

class DatosAsociado {
  final String? metodoPago;
  final String? estadoMembresia;
  final String? estadoPago;
  final bool? autorizaWhatsapp;
  final String? fechaVinculacion;

  DatosAsociado({
    this.metodoPago,
    this.estadoMembresia,
    this.estadoPago,
    this.autorizaWhatsapp,
    this.fechaVinculacion,
  });

  Map<String, dynamic> toJson() => {
    'metodo_pago': metodoPago,
    'estado_membresia': estadoMembresia,
    'estado_pago': estadoPago,
    'autoriza_whatsapp': autorizaWhatsapp,
    'fecha_vinculacion': fechaVinculacion,
  };
}

class DatosVoluntario {
  final String? cargo;
  final String? campoAccion;
  final String? tipo; // Opcional
  final int? horasSemana;
  final String? urlDoc; // Opcional
  final String? urlCv; // Opcional
  final String? fechaVinculacion;
  final bool? cartaCompromisoFirmada;
  final bool? formularioInscripcion;

  DatosVoluntario({
    this.cargo,
    this.campoAccion,
    this.tipo,
    this.horasSemana,
    this.urlDoc,
    this.urlCv,
    this.fechaVinculacion,
    this.cartaCompromisoFirmada,
    this.formularioInscripcion,
  });

  Map<String, dynamic> toJson() => {
    'cargo': cargo,
    'campo_accion': campoAccion,
    'tipo': tipo,
    'horas_semana': horasSemana,
    'url_doc': urlDoc,
    'url_cv': urlCv,
    'fecha_vinculacion': fechaVinculacion,
    'carta_compromiso_firmada': cartaCompromisoFirmada,
    'formulario_inscripcion': formularioInscripcion,
  };
}

class MemberRegistrationRequest {
  final Identificacion identificacion;
  final DatosPersonales datosPersonales;
  final SituacionSocial situacionSocial;
  final LegalAcogida legalAcogida;
  final ContactoEmergencia contactoEmergencia;
  final bool esAsociado;
  final DatosAsociado? datosAsociado;
  final bool esVoluntario;
  final DatosVoluntario? datosVoluntario;

  MemberRegistrationRequest({
    required this.identificacion,
    required this.datosPersonales,
    required this.situacionSocial,
    required this.legalAcogida,
    required this.contactoEmergencia,
    required this.esAsociado,
    this.datosAsociado,
    required this.esVoluntario,
    this.datosVoluntario,
  });

  Map<String, dynamic> toJson() => {
    'identificacion': identificacion.toJson(),
    'datos_personales': datosPersonales.toJson(),
    'situacion_social': situacionSocial.toJson(),
    'legal_acogida': legalAcogida.toJson(),
    'contacto_emergencia': contactoEmergencia.toJson(),
    'es_asociado': esAsociado,
    'datos_asociado': datosAsociado?.toJson(),
    'es_voluntario': esVoluntario,
    'datos_voluntario': datosVoluntario?.toJson(),
  };
}
