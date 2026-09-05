import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/theme/app_colors.dart';
import '../bloc/auth_bloc.dart';
import '../bloc/auth_event.dart';
import '../bloc/auth_state.dart';
import '../widgets/glassmorphic_container.dart';
import '../../../dashboard/presentation/pages/dashboard_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _submit() {
    if (_formKey.currentState!.validate()) {
      context.read<AuthBloc>().add(
        LoginRequested(
          _emailController.text.trim(),
          _passwordController.text.trim(),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final isWideScreen = size.width > 900;

    return Scaffold(
      body: BlocListener<AuthBloc, AuthState>(
        listener: (context, state) {
          if (state.status == AuthStatus.failure &&
              state.errorMessage != null) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Row(
                  children: [
                    const Icon(Icons.error_outline, color: Colors.white),
                    const SizedBox(width: 12),
                    Expanded(child: Text(state.errorMessage!)),
                  ],
                ),
                backgroundColor: AppColors.errorRed,
                behavior: SnackBarBehavior.floating,
                margin: const EdgeInsets.all(24),
              ),
            );
          } else if (state.status == AuthStatus.success) {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (_) => const DashboardPage()),
            );
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Login Exitoso. Redirigiendo...'),
                backgroundColor: Colors.green,
              ),
            );
          } else if (state.isForgotPasswordSuccess) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text(
                  'Se ha enviado un enlace de recuperación al correo administrador.',
                ),
                backgroundColor: AppColors.primaryBlue,
              ),
            );
          }
        },
        child: Container(
          // Si tuviéramos la imagen de fondo con wanted posters, iría aquí.
          // Usaremos un color de fondo base mientras tanto.
          color: AppColors.backgroundWhite,
          child: Row(
            children: [
              // Lado Izquierdo: Branding (Solo en Desktop)
              if (isWideScreen)
                Expanded(
                  flex: 5,
                  child: Container(
                    decoration: const BoxDecoration(
                      image: DecorationImage(
                        image: AssetImage(
                          'assets/imagen-asocolgi/LOGO.jpg.jpeg',
                        ),
                        fit: BoxFit.cover,
                      ),
                    ),
                    child: Container(
                      color: AppColors.primaryBlue.withValues(
                        alpha: 0.85,
                      ), // Overlay azul
                      child: Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              'Bienvenido al Sistema',
                              style: Theme.of(context).textTheme.displayLarge
                                  ?.copyWith(
                                    color: Colors.white,
                                    fontSize: 36,
                                    shadows: [
                                      Shadow(
                                        color: Colors.black.withValues(
                                          alpha: 0.5,
                                        ),
                                        blurRadius: 10,
                                      ),
                                    ],
                                  ),
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Gestión integral de Asocolgi',
                              style: Theme.of(context).textTheme.bodyLarge
                                  ?.copyWith(
                                    color: Colors.white70,
                                    fontSize: 18,
                                  ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),

              // Lado Derecho: Formulario Minimalista
              Expanded(
                flex: 5,
                child: Container(
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(
                      alpha: 0.8,
                    ), // Efecto claro de la derecha
                  ),
                  child: Center(
                    child: SingleChildScrollView(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 48,
                        vertical: 24,
                      ),
                      child: Container(
                        constraints: const BoxConstraints(maxWidth: 420),
                        child: GlassmorphicContainer(
                          padding: const EdgeInsets.all(32),
                          child: Form(
                            key: _formKey,
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                if (!isWideScreen) ...[
                                  Center(
                                    child: Image.asset(
                                      'assets/imagen-asocolgi/Logo.jpeg',
                                      height: 100,
                                      errorBuilder: (_, __, ___) => const Icon(
                                        Icons.group,
                                        size: 80,
                                        color: AppColors.primaryBlue,
                                      ),
                                    ),
                                  ),
                                  const SizedBox(height: 32),
                                ],
                                Text(
                                  'Iniciar Sesión',
                                  style: Theme.of(context)
                                      .textTheme
                                      .displayLarge
                                      ?.copyWith(
                                        fontSize: 28,
                                        color: AppColors.textDark,
                                      ),
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 40),

                                // Email Field
                                TextFormField(
                                  controller: _emailController,
                                  decoration: const InputDecoration(
                                    labelText: 'Correo Electrónico',
                                    prefixIcon: Icon(Icons.email_outlined),
                                  ),
                                  validator: (value) {
                                    if (value == null || value.isEmpty)
                                      return 'Requerido';
                                    if (!value.contains('@'))
                                      return 'Correo inválido';
                                    return null;
                                  },
                                  textInputAction: TextInputAction.next,
                                ),
                                const SizedBox(height: 24),

                                // Password Field
                                BlocBuilder<AuthBloc, AuthState>(
                                  buildWhen: (previous, current) =>
                                      previous.obscurePassword !=
                                      current.obscurePassword,
                                  builder: (context, state) {
                                    return TextFormField(
                                      controller: _passwordController,
                                      obscureText: state.obscurePassword,
                                      decoration: InputDecoration(
                                        labelText: 'Contraseña',
                                        prefixIcon: const Icon(
                                          Icons.lock_outline,
                                        ),
                                        suffixIcon: IconButton(
                                          icon: Icon(
                                            state.obscurePassword
                                                ? Icons.visibility_off
                                                : Icons.visibility,
                                            color: AppColors.textLight,
                                          ),
                                          onPressed: () {
                                            context.read<AuthBloc>().add(
                                              const TogglePasswordVisibility(),
                                            );
                                          },
                                        ),
                                      ),
                                      validator: (value) {
                                        if (value == null || value.isEmpty)
                                          return 'Requerido';
                                        return null;
                                      },
                                      onFieldSubmitted: (_) => _submit(),
                                    );
                                  },
                                ),
                                const SizedBox(height: 16),

                                // Forgot Password Link
                                Align(
                                  alignment: Alignment.centerRight,
                                  child: TextButton(
                                    onPressed: () {
                                      context.read<AuthBloc>().add(
                                        const ForgotPasswordRequested(),
                                      );
                                    },
                                    child: const Text(
                                      '¿Olvidaste tu contraseña?',
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 32),

                                // Submit Button
                                BlocBuilder<AuthBloc, AuthState>(
                                  builder: (context, state) {
                                    return AnimatedContainer(
                                      duration: const Duration(
                                        milliseconds: 300,
                                      ),
                                      curve: Curves.easeInOut,
                                      height: 56,
                                      child: ElevatedButton(
                                        onPressed:
                                            state.status == AuthStatus.loading
                                            ? null
                                            : _submit,
                                        style: ElevatedButton.styleFrom(
                                          shape: RoundedRectangleBorder(
                                            borderRadius: BorderRadius.circular(
                                              12,
                                            ),
                                          ),
                                        ),
                                        child:
                                            state.status == AuthStatus.loading
                                            ? const SizedBox(
                                                height: 24,
                                                width: 24,
                                                child:
                                                    CircularProgressIndicator(
                                                      color: Colors.white,
                                                      strokeWidth: 2,
                                                    ),
                                              )
                                            : const Text(
                                                'Ingresar',
                                                style: TextStyle(
                                                  fontSize: 16,
                                                  fontWeight: FontWeight.bold,
                                                ),
                                              ),
                                      ),
                                    );
                                  },
                                ),

                                const SizedBox(height: 24),
                                // Subrayado amarillo estético
                                Center(
                                  child: Container(
                                    width: 60,
                                    height: 4,
                                    decoration: BoxDecoration(
                                      color: AppColors.primaryYellow,
                                      borderRadius: BorderRadius.circular(2),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
