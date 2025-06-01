import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:iconsax/iconsax.dart';
import 'package:quick_trip/features/authentication/password_config/forget_password.dart';
import 'package:quick_trip/features/authentication/signup_widgets/signup.dart';
import 'package:quick_trip/navigation_menu_user.dart';
import 'package:quick_trip/navigation_menu_driver.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/constants/text_strings.dart';
import "../../AuthService.dart";
import 'package:shared_preferences/shared_preferences.dart';

class ELoginForm extends StatefulWidget {
  final String userType;

  const ELoginForm({super.key, required this.userType});

  @override
  State<ELoginForm> createState() => _ELoginFormState();
}

class _ELoginFormState extends State<ELoginForm> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController emailController;
  late TextEditingController passwordController;
  bool isPasswordVisible = false;

  @override
  void initState() {
    super.initState();
    emailController = TextEditingController();
    passwordController = TextEditingController();
  }

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  void _showError(String message) {
    Get.snackbar(
      "Login Failed",
      message,
      backgroundColor: Colors.red.withOpacity(0.7),
      colorText: Colors.white,
      snackPosition: SnackPosition.BOTTOM,
      duration: const Duration(seconds: 3),
    );
  }

  String? _validateEmailOrPlate(String? value) {
    if (value == null || value.trim().isEmpty) {
      return widget.userType == "User"
          ? "Please enter your phone number"
          : "Please enter your plate number";
    }

    if (widget.userType == "User") {
      // Validate phone number format (10 digits only)
      final phoneRegExp = RegExp(r'^\d{10}$');
      if (!phoneRegExp.hasMatch(value.trim())) {
        return "Phone number must be 10 digits";
      }
    }

    return null;
  }

  String? _validatePassword(String? value) {
    if (value == null || value.trim().isEmpty) {
      return "Please enter your password";
    }
    return null;
  }

  void _onLogin() async {
    if (_formKey.currentState!.validate()) {
      final emailOrPlate = emailController.text.trim();
      final password = passwordController.text.trim();

      // Show loading indicator
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (_) => const Center(child: CircularProgressIndicator()),
      );

      try {
        Map<String, dynamic> response;

        if (widget.userType == "User") {
          response = await AuthService.userLogin(emailOrPlate, password);
        } else {
          response = await AuthService.driverLogin(emailOrPlate, password);
        }

        Navigator.of(context).pop(); // Close loading dialog

        // ✅ Check for access token
        final accessToken = response['access'];
if (accessToken != null && accessToken is String) {
  // 🔐 Store access token and phone/plate
  SharedPreferences prefs = await SharedPreferences.getInstance();
  await prefs.setString('accessToken', accessToken);
  await prefs.setString('loginIdentifier', emailOrPlate); // phone or plate

  if (widget.userType == "User") {
    Get.to(() => const NavigationMenu());
  } else {
    Get.to(() => const NavigationMenuDriver());
  }
}

      } catch (e) {
        Navigator.of(context).pop(); // Close loading dialog
        _showError("Login error: ${e.toString()}");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Padding(
        padding: const EdgeInsets.all(Esizes.spacebtwItems),
        child: Column(
          children: [
            /// Email or Plate Number
            TextFormField(
              controller: emailController,
              keyboardType: widget.userType == "User"
                  ? TextInputType.phone
                  : TextInputType.text,
              decoration: InputDecoration(
                prefixIcon: const Icon(Iconsax.user),
                labelText:
                    widget.userType == "User" ? Etext.phoneNo : Etext.plateNo,
              ),
              validator: _validateEmailOrPlate,
            ),
            const SizedBox(height: Esizes.spacebtwinputFields),

            /// Password
            TextFormField(
              controller: passwordController,
              obscureText: !isPasswordVisible,
              decoration: InputDecoration(
                prefixIcon: const Icon(Iconsax.password_check),
                labelText: Etext.password,
                suffixIcon: IconButton(
                  icon: Icon(
                    isPasswordVisible ? Iconsax.eye : Iconsax.eye_slash,
                  ),
                  onPressed: () {
                    setState(() {
                      isPasswordVisible = !isPasswordVisible;
                    });
                  },
                ),
              ),
              validator: _validatePassword,
            ),

            const SizedBox(height: Esizes.spacebtwinputFields / 2),

            /// Forget Password
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton(
                  onPressed: () => Get.to(() => const ForgetPassword()),
                  child: Text(Etext.forgetPassword),
                ),
              ],
            ),

            const SizedBox(height: Esizes.spacebtwSections),

            /// Sign In Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _onLogin,
                child: Text(widget.userType == "User"
                    ? Etext.signIn
                    : Etext.driversignIn),
              ),
            ),

            const SizedBox(height: Esizes.spacebtwItems),

            /// Create Account (User only)
            if (widget.userType == "User")
              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  onPressed: () => Get.to(() => const SignupScreen()),
                  child: const Text(Etext.createA),
                ),
              ),

            const SizedBox(height: Esizes.spacebtwinputFields),
          ],
        ),
      ),
    );
  }
}
