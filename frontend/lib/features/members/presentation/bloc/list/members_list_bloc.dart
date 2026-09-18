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
    emit(state.copyWith(status: MembersListStatus.loading, isFetchingMore: false));
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
        isFetchingMore: false,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: MembersListStatus.failure,
        errorMessage: e.toString(),
        isFetchingMore: false,
      ));
    }
  }

  Future<void> _onLoadMoreMembers(
    LoadMoreMembers event,
    Emitter<MembersListState> emit,
  ) async {
    if (state.hasReachedMax || state.isFetchingMore || state.status != MembersListStatus.success) return;

    emit(state.copyWith(isFetchingMore: true));

    try {
      if (state.members.isEmpty) {
        emit(state.copyWith(isFetchingMore: false));
        return;
      }
      final lastId = state.members.last['id'] as int?;
      if (lastId == null) {
        emit(state.copyWith(isFetchingMore: false));
        return;
      }

      final moreMembers = await _memberRepository.getMembers(
        lastId: lastId,
        limit: _limit,
        query: state.searchQuery.isEmpty ? null : state.searchQuery,
        genero: state.generoFilter,
        rol: state.rolFilter,
        situacionAdmin: state.situacionAdminFilter,
      );
      
      if (moreMembers.isEmpty) {
        emit(state.copyWith(hasReachedMax: true, isFetchingMore: false));
      } else {
        emit(state.copyWith(
          status: MembersListStatus.success,
          members: List.of(state.members)..addAll(moreMembers),
          hasReachedMax: moreMembers.length < _limit,
          isFetchingMore: false,
        ));
      }
    } catch (e) {
      emit(state.copyWith(
        status: MembersListStatus.failure,
        errorMessage: e.toString(),
        isFetchingMore: false,
      ));
    }
  }

  Future<void> _onRefreshMembers(
    RefreshMembers event,
    Emitter<MembersListState> emit,
  ) async {
    emit(state.copyWith(status: MembersListStatus.loading, hasReachedMax: false, isFetchingMore: false, members: []));
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
        isFetchingMore: false,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: MembersListStatus.failure,
        errorMessage: e.toString(),
        isFetchingMore: false,
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
      isFetchingMore: false,
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
        isFetchingMore: false,
      ));
    } catch (e) {
      emit(state.copyWith(
        status: MembersListStatus.failure,
        errorMessage: e.toString(),
        isFetchingMore: false,
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
