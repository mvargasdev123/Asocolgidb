import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../domain/repositories/comentario_repository.dart';
import 'comentarios_event.dart';
import 'comentarios_state.dart';

class ComentariosBloc extends Bloc<ComentariosEvent, ComentariosState> {
  final ComentarioRepository _repository;

  ComentariosBloc({required ComentarioRepository repository})
      : _repository = repository,
        super(const ComentariosState()) {
    on<LoadComentarios>(_onLoadComentarios);
    on<AddComentario>(_onAddComentario);
    on<UpdateComentario>(_onUpdateComentario);
    on<DeleteComentario>(_onDeleteComentario);
  }

  Future<void> _onLoadComentarios(
    LoadComentarios event,
    Emitter<ComentariosState> emit,
  ) async {
    emit(state.copyWith(status: ComentariosStatus.loading, errorMessage: null));
    try {
      final list = await _repository.getComentarios(event.idPersona);
      emit(state.copyWith(
        status: ComentariosStatus.loaded,
        comentarios: list,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: ComentariosStatus.failure,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onAddComentario(
    AddComentario event,
    Emitter<ComentariosState> emit,
  ) async {
    emit(state.copyWith(isSubmitting: true, errorMessage: null));
    try {
      await _repository.createComentario(
        event.idPersona,
        event.texto,
        event.tipo,
        fechaCreacion: event.fechaCreacion,
      );
      final list = await _repository.getComentarios(event.idPersona);
      emit(state.copyWith(
        status: ComentariosStatus.loaded,
        comentarios: list,
        isSubmitting: false,
      ));
    } catch (e) {
      emit(state.copyWith(
        isSubmitting: false,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onUpdateComentario(
    UpdateComentario event,
    Emitter<ComentariosState> emit,
  ) async {
    emit(state.copyWith(isSubmitting: true, errorMessage: null));
    try {
      await _repository.updateComentario(
        event.idComentario,
        texto: event.texto,
        tipo: event.tipo,
        fechaCreacion: event.fechaCreacion,
      );
      final list = await _repository.getComentarios(event.idPersona);
      emit(state.copyWith(
        status: ComentariosStatus.loaded,
        comentarios: list,
        isSubmitting: false,
      ));
    } catch (e) {
      emit(state.copyWith(
        isSubmitting: false,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }

  Future<void> _onDeleteComentario(
    DeleteComentario event,
    Emitter<ComentariosState> emit,
  ) async {
    emit(state.copyWith(isSubmitting: true, errorMessage: null));
    try {
      await _repository.deleteComentario(event.idComentario);
      final list = await _repository.getComentarios(event.idPersona);
      emit(state.copyWith(
        status: ComentariosStatus.loaded,
        comentarios: list,
        isSubmitting: false,
      ));
    } catch (e) {
      emit(state.copyWith(
        isSubmitting: false,
        errorMessage: e.toString().replaceAll('Exception: ', ''),
      ));
    }
  }
}
