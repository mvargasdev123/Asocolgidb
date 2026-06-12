import 'package:dio/dio.dart';
import '../models/person_model.dart';
import '../../domain/entities/person.dart';

/// Un "DataSource" (Fuente de Datos) es el trabajador que sabe exactamente
/// a qué puerta del servidor (endpoint de FastAPI) debe ir a tocar para pedir información.
/// 
/// En este caso, es el "Remote" (Remoto) porque va a Internet (o a la red local).
class PersonRemoteDataSource {
  
  /// El cartero (ApiClient) que configuramos antes en 'core/api'.
  final Dio client;

  /// Constructor. Le pasamos el cartero ya listo para usarse.
  PersonRemoteDataSource({required this.client});

  /// Función para ir al servidor y pedir la lista completa de personas.
  /// ¿Qué hace?: Va a la dirección '/persons' en el servidor de Python,
  /// trae la lista de datos en crudo (JSON) y la convierte en una lista de PersonModel.
  Future<List<PersonModel>> fetchPersons() async {
    try {
      // Vamos al endpoint real de FastAPI: /personas
      final response = await client.get('/personas');
      
      // Extraemos la lista de datos del paquete
      final List<dynamic> dataList = response.data as List<dynamic>;
      
      // Convertimos cada elemento "crudo" de la lista en un objeto 'PersonModel'
      // hermoso y ordenado que nuestra app puede entender usando '.map' y '.toList'.
      return dataList.map((json) => PersonModel.fromJson(json)).toList();
    } catch (e) {
      throw Exception('Error al obtener personas del servidor: $e');
    }
  }

  /// Trae el detalle de UNA sola persona por su ID.
  Future<PersonModel> fetchPersonDetail(int personId) async {
    try {
      final response = await client.get('/personas/$personId');
      return PersonModel.fromJson(response.data as Map<String, dynamic>);
    } catch (e) {
      throw Exception('Error al obtener detalle de la persona: $e');
    }
  }

  /// Crea una nueva persona enviando un POST a FastAPI.
  Future<PersonModel> createPerson(PersonCreateEntity personToCreate) async {
    try {
      final dataJson = PersonModel.createToJson(personToCreate);
      final response = await client.post('/personas/', data: dataJson);
      // FastAPI devuelve la persona recién creada con su ID
      return PersonModel.fromJson(response.data as Map<String, dynamic>);
    } catch (e) {
      throw Exception('Error al crear persona: $e');
    }
  }

  /// Elimina una persona por su ID.
  Future<void> deletePerson(int personId) async {
    try {
      await client.delete('/personas/$personId');
    } catch (e) {
      throw Exception('Error al eliminar persona: $e');
    }
  }

  /// Asciende a una persona al rol seleccionado, inyectando datos por defecto
  /// para satisfacer los estrictos esquemas de validación de FastAPI.
  Future<void> updatePersonRole(int personId, PersonRole newRole) async {
    if (newRole == PersonRole.externo) return; // Externo no requiere endpoint
    
    final dateStr = DateTime.now().toIso8601String().split('T')[0];
    
    try {
      if (newRole == PersonRole.voluntario) {
        await client.post('/roles/ascender/voluntario/$personId', data: {
          "area_voluntariado": "General (Asignación rápida)",
          "horas_disponibles": 10,
          "fecha_inicio": dateStr
        });
      } else if (newRole == PersonRole.asociado) {
        await client.post('/roles/ascender/asociado/$personId', data: {
          "tramites": "Ingreso estándar MVP",
          "fecha_inicio": dateStr
        });
      } else if (newRole == PersonRole.contratado) {
        await client.post('/roles/ascender/contratado/$personId', data: {
          "funcion": "Asignación inicial",
          "horas_contratadas": 40,
          "fecha_inicio": dateStr
        });
      }
    } catch (e) {
      throw Exception('Error al asignar el rol a la persona: $e');
    }
  }
}
