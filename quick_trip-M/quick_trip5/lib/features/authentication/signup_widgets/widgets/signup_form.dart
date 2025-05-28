import 'package:quick_trip/features/authentication/signup_widgets/verify_phone.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/constants/text_strings.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:iconsax/iconsax.dart';

class EsignupForm extends StatefulWidget {
  const EsignupForm({super.key});

  @override
  State<EsignupForm> createState() => _EsignupFormState();
}

class _EsignupFormState extends State<EsignupForm> {
  final _formKey = GlobalKey<FormState>();
  final _faydaController = TextEditingController();
  final _phoneController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  bool _isPasswordVisible = false;
  bool _isConfirmPasswordVisible = false;

  @override
  void dispose() {
    _faydaController.dispose();
    _phoneController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);

    return Form(
      key: _formKey,
      child: Column(
        children: [
          /// Fayda Number
          TextFormField(
            controller: _faydaController,
            decoration: const InputDecoration(
              labelText: Etext.faydaNumber,
              prefixIcon: Icon(Iconsax.user_edit),
            ),
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Please enter Fayda number';
              }
              return null;
            },
          ),
          const SizedBox(height: Esizes.spacebtwinputFields),

          /// Phone Number
          TextFormField(
            controller: _phoneController,
            keyboardType: TextInputType.phone,
            decoration: const InputDecoration(
              labelText: Etext.phoneNo,
              prefixIcon: Icon(Iconsax.call),
            ),
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Please enter phone number';
              }
              if (!RegExp(r'^\d{10}$').hasMatch(value)) {
                return 'Phone number must be 10 digits';
              }
              return null;
            },
          ),
          const SizedBox(height: Esizes.spacebtwinputFields),

          /// Password
          TextFormField(
            controller: _passwordController,
            obscureText: !_isPasswordVisible,
            decoration: InputDecoration(
              labelText: Etext.password,
              prefixIcon: const Icon(Iconsax.password_check),
              suffixIcon: IconButton(
                icon: Icon(_isPasswordVisible ? Iconsax.eye : Iconsax.eye_slash),
                onPressed: () {
                  setState(() => _isPasswordVisible = !_isPasswordVisible);
                },
              ),
              // helperText: 'Use at least 6 characters with letters, numbers, and symbols',
            ),
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Please enter password';
              }
              if (value.length < 6) {
                return 'Password must be at least 6 characters';
              }
              if (!RegExp(r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[\W_]).+$').hasMatch(value)) {
                return 'Use letters, numbers & special characters';
              }
              return null;
            },
          ),

          const SizedBox(height: Esizes.spacebtwinputFields),

          /// Confirm Password
          TextFormField(
            controller: _confirmPasswordController,
            obscureText: !_isConfirmPasswordVisible,
            decoration: InputDecoration(
              labelText: 'Confirm Password',
              prefixIcon: const Icon(Iconsax.lock),
              suffixIcon: IconButton(
                icon: Icon(
                  _isConfirmPasswordVisible ? Iconsax.eye : Iconsax.eye_slash,
                ),
                onPressed: () {
                  setState(() => _isConfirmPasswordVisible = !_isConfirmPasswordVisible);
                },
              ),
            ),
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Please confirm your password';
              }
              if (value != _passwordController.text) {
                return 'Passwords do not match';
              }
              return null;
            },
          ),

          const SizedBox(height: Esizes.spacebtwSections),

          /// Sign Up Button
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {
                if (_formKey.currentState!.validate()) {
                  Get.to(() => const VerifyPhoneNo());
                }
              },
              child: const Text(Etext.createA),
            ),
          ),
        ],
      ),
    );
  }
}




