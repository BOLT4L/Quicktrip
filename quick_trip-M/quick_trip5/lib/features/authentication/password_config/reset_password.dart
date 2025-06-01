import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/utils/constants/sizes.dart';

class ChangePasswordScreen extends StatefulWidget {
  const ChangePasswordScreen({super.key});

  @override
  State<ChangePasswordScreen> createState() => _ChangePasswordScreenState();
}

class _ChangePasswordScreenState extends State<ChangePasswordScreen> {
  final _formKey = GlobalKey<FormState>();
  final _currentPasswordController = TextEditingController();
  final _newPasswordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  bool _obscureCurrent = true;
  bool _obscureNew = true;
  bool _obscureConfirm = true;

  void _submit() {
    if (_formKey.currentState!.validate()) {
      // Add backend logic here
      Get.snackbar('Success', 'Password updated successfully!',
          snackPosition: SnackPosition.TOP);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: EappBar(
        showBackArrow: true,
        title: Text('Change Password', style: Theme.of(context).textTheme.headlineMedium),
      ),
      body: Padding(
        padding: const EdgeInsets.all(Esizes.defaultSpace),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              /// Current Password
              TextFormField(
                controller: _currentPasswordController,
                obscureText: _obscureCurrent,
                decoration: InputDecoration(
                  labelText: 'Current Password',
                  suffixIcon: IconButton(
                    icon: Icon(_obscureCurrent ? Icons.visibility_off : Icons.visibility),
                    onPressed: () => setState(() => _obscureCurrent = !_obscureCurrent),
                  ),
                ),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Please enter current password' : null,
              ),
              const SizedBox(height: Esizes.spacebtwinputFields),

              /// New Password
              TextFormField(
                controller: _newPasswordController,
                obscureText: _obscureNew,
                decoration: InputDecoration(
                  labelText: 'New Password',
                  suffixIcon: IconButton(
                    icon: Icon(_obscureNew ? Icons.visibility_off : Icons.visibility),
                    onPressed: () => setState(() => _obscureNew = !_obscureNew),
                  ),
                  // helperText: 'Use at least 6 characters, include number & symbol',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) return 'Please enter new password';
                  if (value.length < 6) return 'Password must be at least 6 characters';
                  if (!RegExp(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[\W_]).+$').hasMatch(value)) {
                    return 'Include letters, numbers & symbols';
                  }
                  return null;
                },
              ),
              const SizedBox(height: Esizes.spacebtwinputFields),

              /// Confirm Password
              TextFormField(
                controller: _confirmPasswordController,
                obscureText: _obscureConfirm,
                decoration: InputDecoration(
                  labelText: 'Confirm New Password',
                  suffixIcon: IconButton(
                    icon: Icon(_obscureConfirm ? Icons.visibility_off : Icons.visibility),
                    onPressed: () => setState(() => _obscureConfirm = !_obscureConfirm),
                  ),
                ),
                validator: (value) =>
                    value != _newPasswordController.text ? 'Passwords do not match' : null,
              ),
              const SizedBox(height: Esizes.spacebtwSections),

              /// Submit Button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _submit,
                  child: const Text('Update Password'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
