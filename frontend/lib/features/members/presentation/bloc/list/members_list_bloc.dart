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
  }

  Future<void> _onLoadInitialMembers(
    LoadInitialMembers event,
    Emitter<MembersListState> emit,
  ) async {
    if (state.status == MembersListStatus.loading) return;
    emit(state.copyWith(status: MembersListStatus.loading));
    try {
      final members = await _memberRepository.getMembers(limit: _limit);
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

      final moreMembers = await _memberRepository.getMembers(lastId: lastId, limit: _limit);
      
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
      final members = await _memberRepository.getMembers(limit: _limit);
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
