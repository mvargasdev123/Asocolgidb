abstract class MembersListEvent {}

class LoadInitialMembers extends MembersListEvent {}

class LoadMoreMembers extends MembersListEvent {}

class RefreshMembers extends MembersListEvent {}

class RemoveMemberFromList extends MembersListEvent {
  final int memberId;
  RemoveMemberFromList(this.memberId);
}

class FilterMembers extends MembersListEvent {
  final String? query;
  final String? genero;
  final String? rol;
  final String? situacionAdmin;

  FilterMembers({
    this.query,
    this.genero,
    this.rol,
    this.situacionAdmin,
  });
}

