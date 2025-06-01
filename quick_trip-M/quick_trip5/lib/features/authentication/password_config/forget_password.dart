import 'dart:async';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:iconsax/iconsax.dart';
import 'package:quick_trip/features/authentication/password_config/reset_password.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/constants/text_strings.dart';

class ForgetPassword extends StatefulWidget {
  const ForgetPassword({super.key});

  @override
  State<ForgetPassword> createState() => _ForgetPasswordState();
}

class _ForgetPasswordState extends State<ForgetPassword> {
  final _formKey = GlobalKey<FormState>();
  final _codeController = TextEditingController();

  int _secondsLeft = 0;
  Timer? _resendTimer;

  void _submitCode() {
    if (_formKey.currentState!.validate()) {
      Get.off(() => const ChangePasswordScreen());
    }
  }

  void _startResendTimer() {
    setState(() => _secondsLeft = 30);
    _resendTimer?.cancel();

    _resendTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_secondsLeft == 0) {
        timer.cancel();
      } else {
        setState(() => _secondsLeft--);
      }
    });
  }

  @override
  void dispose() {
    _resendTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Padding(
        padding: const EdgeInsets.all(Esizes.defaultSpace),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(Etext.passTitle, style: Theme.of(context).textTheme.headlineMedium),
              const SizedBox(height: Esizes.spacebtwItems),
              Text(Etext.passSubTitle, style: Theme.of(context).textTheme.labelMedium),
              const SizedBox(height: Esizes.spacebtwItems),

              // Code input
              TextFormField(
                controller: _codeController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: Etext.code,
                  prefixIcon: Icon(Iconsax.direct_right),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) return 'Please enter the code';
                  if (value.length < 4) return 'Enter at least 4 digits';
                  return null;
                },
              ),
              const SizedBox(height: Esizes.spacebtwItems),

              // Resend code button
              Align(
                alignment: Alignment.centerRight,
                child: TextButton(
                  onPressed: _secondsLeft == 0 ? _startResendTimer : null,
                  child: Text(
                    _secondsLeft == 0
                        ? 'Resend Code'
                        : 'Resend in $_secondsLeft s',
                    style: TextStyle(
                      color: _secondsLeft == 0 ? Colors.blue : Colors.grey,
                    ),
                  ),
                ),
              ),

              const SizedBox(height: Esizes.spacebtwSections),

              // Submit button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _submitCode,
                  child: const Text(Etext.submit),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
