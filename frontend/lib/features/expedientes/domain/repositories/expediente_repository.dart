import '../models/expediente_model.dart';

abstract class ExpedienteRepository {
  Future<List<ExpedienteModel>> getExpedientes({String? estado});
  Future<List<ExpedienteModel>> getExpedientesPersona(int idPersona);
  Future<ExpedienteModel> getExpedienteById(int idExpediente);
  Future<ExpedienteModel> createExpediente({
    required int idPersona,
    required String tipoTramite,
    required String fechaPresentacion,
    String? numeroExpedienteAsignado,
    String? representanteLegal,
    String? consultorioJuridico,
    String aporteSocial = 'Sí',
    bool solicitanteExtranjeria = false,
    bool antecedentesTraducidosYApostillados = false,
    String? fechaResolucion,
  });
  Future<ExpedienteModel> updateExpedienteStatus({
    required int idExpediente,
    required String estado,
  });
  Future<void> deleteExpediente(int idExpediente);
}
