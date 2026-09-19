import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'core/theme/app_theme.dart';
import 'core/theme/app_colors.dart';
import 'core/network/token_storage.dart';
import 'core/network/dio_client.dart';
import 'core/network/inactivity_service.dart';
import 'features/auth/data/repositories/auth_repository_impl.dart';
import 'features/auth/domain/repositories/auth_repository.dart';
import 'features/auth/presentation/bloc/auth_bloc.dart';
import 'features/auth/presentation/bloc/auth_event.dart';
import 'features/auth/presentation/bloc/auth_state.dart';
import 'features/auth/presentation/pages/login_page.dart';
import 'features/members/data/repositories/member_repository_impl.dart';
import 'features/members/domain/repositories/member_repository.dart';
import 'features/members/data/repositories/comentario_repository_impl.dart';
import 'features/members/domain/repositories/comentario_repository.dart';
import 'features/members/presentation/bloc/list/members_list_bloc.dart';
import 'features/members/presentation/bloc/list/members_list_event.dart';
import 'features/members/presentation/bloc/registration/registration_bloc.dart';
import 'features/expedientes/data/repositories/expediente_repository_impl.dart';
import 'features/expedientes/domain/repositories/expediente_repository.dart';
import 'features/expedientes/presentation/bloc/expedientes_bloc.dart';
import 'features/dashboard/data/repositories/metrics_repository_impl.dart';
import 'features/dashboard/domain/repositories/metrics_repository.dart';
import 'features/dashboard/presentation/bloc/metrics_bloc.dart';
import 'features/dashboard/data/repositories/excel_repository_impl.dart';
import 'features/dashboard/domain/repositories/excel_repository.dart';
import 'features/dashboard/presentation/bloc/excel_bloc.dart';

final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

void main() {
  runApp(const AsocolgiApp());
}

class AsocolgiApp extends StatefulWidget {
  const AsocolgiApp({super.key});

  @override
  State<AsocolgiApp> createState() => _AsocolgiAppState();
}

class _AsocolgiAppState extends State<AsocolgiApp> {
  bool _isWarningDialogOpen = false;

  void _setupInactivityService() {
    InactivityService().initialize(
      onShowWarning: () {
        if (_isWarningDialogOpen) return;
        final navContext = navigatorKey.currentContext;
        if (navContext != null) {
          _isWarningDialogOpen = true;
          showDialog(
            context: navContext,
            barrierDismissible: false,
            builder: (dialogCtx) => AlertDialog(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              title: const Row(
                children: [
                  Icon(Icons.timer_outlined, color: Colors.orange, size: 28),
                  SizedBox(width: 10),
                  Text('Inactividad Detectada', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                ],
              ),
              content: const Text(
                'Tu sesión expirará en 2 minutos por inactividad.\n\n¿Deseas seguir trabajando y mantener tu sesión activa?',
                style: TextStyle(fontSize: 14),
              ),
              actions: [
                TextButton(
                  onPressed: () {
                    Navigator.of(dialogCtx).pop();
                    _isWarningDialogOpen = false;
                    navContext.read<AuthBloc>().add(const LogoutRequested());
                  },
                  child: const Text('Cerrar Sesión', style: TextStyle(color: Colors.grey)),
                ),
                ElevatedButton.icon(
                  icon: const Icon(Icons.refresh_rounded, size: 18),
                  label: const Text('Mantener Sesión Activa'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryBlue,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                  ),
                  onPressed: () {
                    Navigator.of(dialogCtx).pop();
                    _isWarningDialogOpen = false;
                    InactivityService().recordUserActivity();
                    navContext.read<AuthBloc>().add(const AutoRefreshTokenRequested());
                  },
                ),
              ],
            ),
          ).then((_) {
            _isWarningDialogOpen = false;
          });
        }
      },
      onDismissWarning: () {
        if (_isWarningDialogOpen) {
          final navContext = navigatorKey.currentContext;
          if (navContext != null && Navigator.canPop(navContext)) {
            Navigator.of(navContext, rootNavigator: true).pop();
          }
          _isWarningDialogOpen = false;
        }
      },
      onExpired: () {
        final navContext = navigatorKey.currentContext;
        if (navContext != null) {
          navContext.read<AuthBloc>().add(const SessionExpiredByInactivity());
        }
      },
      onAutoRefresh: () {
        final navContext = navigatorKey.currentContext;
        if (navContext != null) {
          navContext.read<AuthBloc>().add(const AutoRefreshTokenRequested());
        }
      },
    );
  }

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
        RepositoryProvider<ExpedienteRepository>(
          create: (context) => ExpedienteRepositoryImpl(context.read<DioClient>()),
        ),
        RepositoryProvider<MetricsRepository>(
          create: (context) => MetricsRepositoryImpl(context.read<DioClient>()),
        ),
        RepositoryProvider<ExcelRepository>(
          create: (context) => ExcelRepositoryImpl(context.read<DioClient>().dio),
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
          BlocProvider(
            create: (context) => RegistrationBloc(
              repository: context.read<MemberRepository>(),
            ),
          ),
          BlocProvider(
            create: (context) => ExpedientesBloc(
              repository: context.read<ExpedienteRepository>(),
            ),
          ),
          BlocProvider(
            create: (context) => MetricsBloc(
              repository: context.read<MetricsRepository>(),
            ),
          ),
          BlocProvider(
            create: (context) => ExcelBloc(
              context.read<ExcelRepository>(),
            ),
          ),
        ],
        child: Builder(
          builder: (context) {
            _setupInactivityService();

            return Listener(
              behavior: HitTestBehavior.translucent,
              onPointerDown: (_) => InactivityService().recordUserActivity(),
              onPointerMove: (_) => InactivityService().recordUserActivity(),
              onPointerHover: (_) => InactivityService().recordUserActivity(),
              onPointerSignal: (_) => InactivityService().recordUserActivity(),
              child: BlocListener<AuthBloc, AuthState>(
                listener: (context, state) {
                  if (state.status == AuthStatus.sessionExpired) {
                    final navCtx = navigatorKey.currentContext;
                    if (navCtx != null) {
                      ScaffoldMessenger.of(navCtx).showSnackBar(
                        SnackBar(
                          content: Text(
                            state.errorMessage ?? 'Tu sesión ha expirado por inactividad. Por favor inicia sesión de nuevo.',
                          ),
                          backgroundColor: Colors.red.shade800,
                          duration: const Duration(seconds: 5),
                        ),
                      );
                      navigatorKey.currentState?.pushAndRemoveUntil(
                        MaterialPageRoute(builder: (_) => const LoginPage()),
                        (route) => false,
                      );
                    }
                  }
                },
                child: MaterialApp(
                  navigatorKey: navigatorKey,
                  title: 'Asocolgi',
                  debugShowCheckedModeBanner: false,
                  theme: AppTheme.lightTheme,
                  home: const LoginPage(),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
