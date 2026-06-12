import '../entities/person.dart';

/// Un "Repositorio" en la capa de Dominio es solo un "Contrato" o "Promesa".
/// ¿Qué es?: Es como un menú de un restaurante. Te dice qué platos hay (funciones),
/// pero no te dice cómo se cocinan en la cocina.
/// ¿Por qué?: Porque la capa de Presentación (la pantalla) solo necesita saber
/// qué puede pedir (ej. "dame la lista de personas"), sin importarle si vienen
/// de Internet, de una base de datos local, o de una paloma mensajera.
/// Esto hace que el código sea muy fácil de probar y cambiar en el futuro.
abstract class PersonRepository {
  
  /// Función para obtener una lista de personas.
  Future<List<PersonEntity>> getPersons();

  /// Función para obtener el detalle de una sola persona.
  Future<PersonEntity> getPersonDetail(int personId);

  /// Función para registrar una nueva persona.
  /// Toma un PersonCreateEntity y devuelve la PersonEntity completa con ID.
  Future<PersonEntity> createPerson(PersonCreateEntity personToCreate);

  /// Función para dar de baja/eliminar a una persona.
  Future<void> deletePerson(int personId);

  /// Función para cambiar (ascender o descender) el rol de una persona.
  Future<void> changePersonRole(int personId, PersonRole newRole);
}
