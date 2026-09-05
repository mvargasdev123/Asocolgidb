import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'core/theme/app_theme.dart';
import 'core/network/token_storage.dart';
import 'core/network/dio_client.dart';
import 'features/auth/data/repositories/auth_repository_impl.dart';
import 'features/auth/domain/repositories/auth_repository.dart';
import 'features/auth/presentation/bloc/auth_bloc.dart';
import 'features/auth/presentation/pages/login_page.dart';
import 'features/members/data/repositories/member_repository_impl.dart';
import 'features/members/domain/repositories/member_repository.dart';
import 'features/members/data/repositories/comentario_repository_impl.dart';
import 'features/members/domain/repositories/comentario_repository.dart';
import 'features/members/presentation/bloc/list/members_list_bloc.dart';
import 'features/members/presentation/bloc/list/members_list_event.dart';

void main() {
  runApp(const AsocolgiApp());
}

class AsocolgiApp extends StatelessWidget {
  const AsocolgiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiRepositoryProvider(
      providers: [
        RepositoryProvider<TokenStorage>(
          create: (context) => TokenStorage(),
        ),
        RepositoryProvider<DioClient>(
          create: (context) => DioClient(tokenStorage: context.read<TokenStorage>()),
        ),
        RepositoryProvider<AuthRepository>(
          create: (context) => AuthRepositoryImpl(dio: context.read<DioClient>().dio),
        ),
        RepositoryProvider<MemberRepository>(
          create: (context) => MemberRepositoryImpl(dio: context.read<DioClient>().dio),
        ),
        RepositoryProvider<ComentarioRepository>(
          create: (context) => ComentarioRepositoryImpl(dio: context.read<DioClient>().dio),
        ),
      ],
      child: MultiBlocProvider(
        providers: [
          BlocProvider(
            create: (context) => AuthBloc(
              authRepository: context.read<AuthRepository>(),
              tokenStorage: context.read<TokenStorage>(),
            ),
          ),
          BlocProvider(
            create: (context) => MembersListBloc(
              memberRepository: context.read<MemberRepository>(),
            )..add(LoadInitialMembers()),
          ),
        ],
        child: MaterialApp(
          title: 'Asocolgi',
          debugShowCheckedModeBanner: false,
          theme: AppTheme.lightTheme,
          home: const LoginPage(),
        ),
      ),
    );
  }
}
