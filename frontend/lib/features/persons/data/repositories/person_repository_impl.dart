import '../../domain/entities/person.dart';
import '../../domain/repositories/person_repository.dart';
import '../datasources/person_remote_data_source.dart';

/// Esta es la "Implementación" del Contrato o Promesa (Repository).
/// ¿Recuerdas que PersonRepository en la capa de Dominio era solo un menú vacío?
/// Bueno, esta clase es el chef en la cocina que de verdad prepara la comida.
/// 
/// ¿Por qué hacerlo así?: Porque a la pantalla no le importa si traemos los datos de 
/// Internet o de un archivo guardado en el teléfono. Al usar un "Contrato" y luego 
/// su "Implementación", escondemos la complejidad de Internet (el DataSource) 
/// detrás de esta pared de la cocina.
class PersonRepositoryImpl implements PersonRepository {
  
  /// El trabajador que sabe cómo hablar con FastAPI por Internet.
  final PersonRemoteDataSource remoteDataSource;

  /// El Constructor de la cocina (Repository). Necesita tener al trabajador (DataSource) listo.
  PersonRepositoryImpl({required this.remoteDataSource});

  /// Cumplimos la primera promesa del menú: Traer la lista de personas.
  /// La palabra clave '@override' significa: "Estoy sobreescribiendo/cumpliendo
  /// la regla vacía que estaba en el menú original".
  @override
  Future<List<PersonEntity>> getPersons() async {
    // Le pedimos al trabajador que vaya a Internet y nos traiga los modelos JSON procesados.
    final models = await remoteDataSource.fetchPersons();
    
    // Como un PersonModel ES una PersonEntity (porque lo creamos usando la palabra 'extends'),
    // podemos devolver la lista tranquilamente. El dominio recibe lo que esperaba.
    return models;
  }

  @override
  Future<PersonEntity> getPersonDetail(int personId) async {
    return await remoteDataSource.fetchPersonDetail(personId);
  }

  @override
  Future<PersonEntity> createPerson(PersonCreateEntity personToCreate) async {
    // Al usar await, el modelo JSON se devuelve como Entidad pura
    return await remoteDataSource.createPerson(personToCreate);
  }

  @override
  Future<void> deletePerson(int personId) async {
    await remoteDataSource.deletePerson(personId);
  }

  /// Cumplimos la segunda promesa del menú: Cambiar el rol.
  @override
  Future<void> changePersonRole(int personId, PersonRole newRole) async {
    // Simplemente delegamos la tarea pesada de hablar por la red a nuestro trabajador (DataSource).
    await remoteDataSource.updatePersonRole(personId, newRole);
  }
}
