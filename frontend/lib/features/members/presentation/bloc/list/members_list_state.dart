enum MembersListStatus { initial, loading, success, failure }

class MembersListState {
  final MembersListStatus status;
  final List<Map<String, dynamic>> members;
  final bool hasReachedMax;
  final String? errorMessage;

  const MembersListState({
    this.status = MembersListStatus.initial,
    this.members = const [],
    this.hasReachedMax = false,
    this.errorMessage,
  });

  MembersListState copyWith({
    MembersListStatus? status,
    List<Map<String, dynamic>>? members,
    bool? hasReachedMax,
    String? errorMessage,
  }) {
    return MembersListState(
      status: status ?? this.status,
      members: members ?? this.members,
      hasReachedMax: hasReachedMax ?? this.hasReachedMax,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }
}
