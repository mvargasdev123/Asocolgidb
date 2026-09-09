import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../domain/repositories/member_repository.dart';
import 'members_list_event.dart';
import 'members_list_state.dart';

class MembersListBloc extends Bloc<MembersListEvent, MembersListState> {
  final MemberRepository _memberRepository;
  final int _limit = 10;

  MembersListBloc({required MemberRepository memberRepository})
      : _memberRepository = memberRepository,
        super(const MembersListState()) {
    on<LoadInitialMembers>(_onLoadInitialMembers);
    on<LoadMoreMembers>(_onLoadMoreMembers);
    on<RefreshMembers>(_onRefreshMembers);
    on<RemoveMemberFromList>(_onRemoveMemberFromList);
    on<FilterMembers>(_onFilterMembers);
  }

  Future<void> _onLoadInitialMembers(
    LoadInitialMembers event,
    Emitter<MembersListState> emit,
  ) async {
    if (state.status == MembersListStatus.loading) return;
    emit(state.copyWith(status: MembersListStatus.loading));
    try {
      final members = await _memberRepository.getMembers(
        limit: _limit,
        query: state.searchQuery.isEmpty ? null : state.searchQuery,
        genero: state.generoFilter,
        rol: state.rolFilter,
        situacionAdmin: state.situacionAdminFilter,
      );
      emit(state.copyWith(
        status: MembersListStatus.success,
        members: members,
        hasReachedMax: members.length < _limit,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: MembersListStatus.failure,
        errorMessage: e.toString(),
      ));
    }
  }

  Future<void> _onLoadMoreMembers(
    LoadMoreMembers event,
    Emitter<MembersListState> emit,
  ) async {
    if (state.hasReachedMax || state.status != MembersListStatus.success) return;

    try {
      if (state.members.isEmpty) return;
      final lastId = state.members.last['id'] as int?;
      if (lastId == null) return;

      final moreMembers = await _memberRepository.getMembers(
        lastId: lastId,
        limit: _limit,
        query: state.searchQuery.isEmpty ? null : state.searchQuery,
        genero: state.generoFilter,
        rol: state.rolFilter,
        situacionAdmin: state.situacionAdminFilter,
      );
      
      if (moreMembers.isEmpty) {
        emit(state.copyWith(hasReachedMax: true));
      } else {
        emit(state.copyWith(
          status: MembersListStatus.success,
          members: List.of(state.members)..addAll(moreMembers),
          hasReachedMax: moreMembers.length < _limit,
        ));
      }
    } catch (e) {
      emit(state.copyWith(
        status: MembersListStatus.failure,
        errorMessage: e.toString(),
      ));
    }
  }

  Future<void> _onRefreshMembers(
    RefreshMembers event,
    Emitter<MembersListState> emit,
  ) async {
    emit(state.copyWith(status: MembersListStatus.loading, hasReachedMax: false, members: []));
    try {
      final members = await _memberRepository.getMembers(
        limit: _limit,
        query: state.searchQuery.isEmpty ? null : state.searchQuery,
        genero: state.generoFilter,
        rol: state.rolFilter,
        situacionAdmin: state.situacionAdminFilter,
      );
      emit(state.copyWith(
        status: MembersListStatus.success,
        members: members,
        hasReachedMax: members.length < _limit,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: MembersListStatus.failure,
        errorMessage: e.toString(),
      ));
    }
  }

  Future<void> _onFilterMembers(
    FilterMembers event,
    Emitter<MembersListState> emit,
  ) async {
    final newQuery = event.query ?? state.searchQuery;
    final clearGenero = event.genero == 'TODOS';
    final newGenero = clearGenero ? null : (event.genero ?? state.generoFilter);

    final clearRol = event.rol == 'TODOS';
    final newRol = clearRol ? null : (event.rol ?? state.rolFilter);

    final clearSituacion = event.situacionAdmin == 'TODAS';
    final newSituacion = clearSituacion ? null : (event.situacionAdmin ?? state.situacionAdminFilter);

    emit(state.copyWith(
      status: MembersListStatus.loading,
      members: [],
      hasReachedMax: false,
      searchQuery: newQuery,
      generoFilter: newGenero,
      clearGenero: clearGenero,
      rolFilter: newRol,
      clearRol: clearRol,
      situacionAdminFilter: newSituacion,
      clearSituacionAdmin: clearSituacion,
    ));

    try {
      final members = await _memberRepository.getMembers(
        limit: _limit,
        query: newQuery.isEmpty ? null : newQuery,
        genero: newGenero,
        rol: newRol,
        situacionAdmin: newSituacion,
      );
      emit(state.copyWith(
        status: MembersListStatus.success,
        members: members,
        hasReachedMax: members.length < _limit,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: MembersListStatus.failure,
        errorMessage: e.toString(),
      ));
    }
  }

  void _onRemoveMemberFromList(
    RemoveMemberFromList event,
    Emitter<MembersListState> emit,
  ) {
    if (state.status == MembersListStatus.success) {
      final updatedMembers = state.members.where((m) => m['id'] != event.memberId).toList();
      emit(state.copyWith(members: updatedMembers));
    }
  }
}
