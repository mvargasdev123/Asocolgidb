abstract class MembersListEvent {}

class LoadInitialMembers extends MembersListEvent {}

class LoadMoreMembers extends MembersListEvent {}

class RefreshMembers extends MembersListEvent {}

class RemoveMemberFromList extends MembersListEvent {
  final int memberId;
  RemoveMemberFromList(this.memberId);
}
