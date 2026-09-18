enum MembersListStatus { initial, loading, success, failure }

class MembersListState {
  final MembersListStatus status;
  final List<Map<String, dynamic>> members;
  final bool hasReachedMax;
  final bool isFetchingMore;
  final String? errorMessage;
  final String searchQuery;
  final String? generoFilter;
  final String? rolFilter;
  final String? situacionAdminFilter;

  const MembersListState({
    this.status = MembersListStatus.initial,
    this.members = const [],
    this.hasReachedMax = false,
    this.isFetchingMore = false,
    this.errorMessage,
    this.searchQuery = '',
    this.generoFilter,
    this.rolFilter,
    this.situacionAdminFilter,
  });

  bool get hasActiveFilters =>
      searchQuery.isNotEmpty ||
      generoFilter != null ||
      rolFilter != null ||
      situacionAdminFilter != null;

  MembersListState copyWith({
    MembersListStatus? status,
    List<Map<String, dynamic>>? members,
    bool? hasReachedMax,
    bool? isFetchingMore,
    String? errorMessage,
    String? searchQuery,
    String? generoFilter,
    bool clearGenero = false,
    String? rolFilter,
    bool clearRol = false,
    String? situacionAdminFilter,
    bool clearSituacionAdmin = false,
  }) {
    return MembersListState(
      status: status ?? this.status,
      members: members ?? this.members,
      hasReachedMax: hasReachedMax ?? this.hasReachedMax,
      isFetchingMore: isFetchingMore ?? this.isFetchingMore,
      errorMessage: errorMessage ?? this.errorMessage,
      searchQuery: searchQuery ?? this.searchQuery,
      generoFilter: clearGenero ? null : (generoFilter ?? this.generoFilter),
      rolFilter: clearRol ? null : (rolFilter ?? this.rolFilter),
      situacionAdminFilter: clearSituacionAdmin ? null : (situacionAdminFilter ?? this.situacionAdminFilter),
    );
  }
}
