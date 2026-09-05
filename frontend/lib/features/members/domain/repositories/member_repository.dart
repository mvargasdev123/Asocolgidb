import '../models/member_registration_request.dart';

abstract class MemberRepository {
  Future<void> registerMember(MemberRegistrationRequest request);
  Future<List<Map<String, dynamic>>> getMembers({int? lastId, int limit = 10});
  Future<Map<String, dynamic>> getMemberDetails(int id);
  Future<void> updateMember(int id, Map<String, dynamic> data);
  Future<void> deleteMember(int id);
}
