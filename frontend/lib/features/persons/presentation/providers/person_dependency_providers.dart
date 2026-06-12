import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/api/api_client.dart';
import '../../data/datasources/person_remote_data_source.dart';
import '../../data/repositories/person_repository_impl.dart';
import '../../domain/repositories/person_repository.dart';

/// ---- ARCHIVO DE "INYECCIÓN DE DEPENDENCIAS" (LOS PROVEEDORES) ----
/// ¿Qué es un Provider en Riverpod?: Imagina que Riverpod es una gran bodega gigante.
/// Un "Provider" es como un estante etiquetado en esa bodega. Cuando cualquier pantalla
/// de nuestra app necesita algo (ej. el cliente de Internet o la cocina/repositorio),
/// simplemente va a la bodega y lo toma de su estante, en lugar de tener que
/// crearlo desde cero cada vez. ¡Ahorra mucha memoria y organiza el código!

/// 1. Estante del Cartero (ApiClient).
/// ¿Qué hace?: Guarda una copia única y global de nuestro cliente de Internet.
/// ¿Por qué 'Provider' a secas?: Porque el cartero es fijo, no cambia de estado.
final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient();
});

/// 2. Estante del Trabajador de Datos (RemoteDataSource).
/// ¿Qué hace?: Toma al cartero del estante 1, se lo entrega al trabajador, y guarda
/// al trabajador listo en este estante 2.
final personRemoteDataSourceProvider = Provider<PersonRemoteDataSource>((ref) {
  // 'ref.read' es la instrucción de "ir a la bodega a buscar algo".
  final apiClient = ref.read(apiClientProvider);
  return PersonRemoteDataSource(client: apiClient.dio);
});

/// 3. Estante de la Cocina / Contrato Final (PersonRepository).
/// ¿Qué hace?: Toma al trabajador del estante 2, se lo entrega al chef de la cocina,
/// y expone la cocina (el Repositorio) para que cualquier pantalla pueda pedir datos.
/// Notar que devolvemos la clase abstracta (PersonRepository) pero instanciamos
/// la implementación real (PersonRepositoryImpl). ¡Así la pantalla nunca sabe el secreto!
final personRepositoryProvider = Provider<PersonRepository>((ref) {
  final remoteDataSource = ref.read(personRemoteDataSourceProvider);
  return PersonRepositoryImpl(remoteDataSource: remoteDataSource);
});
