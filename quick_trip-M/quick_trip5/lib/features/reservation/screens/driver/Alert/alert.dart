import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AlertScreen extends StatefulWidget {
  const AlertScreen({super.key});

  @override
  State<AlertScreen> createState() => _AlertScreenState();
}

class _AlertScreenState extends State<AlertScreen> {
  final _formKey = GlobalKey<FormState>();
  final _alertController = TextEditingController();

  Future<void> _sendAlert() async {
    if (!_formKey.currentState!.validate()) return;

    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('accessToken');
      final phone = prefs.getString('loginIdentifier');

      // 1. Fetch current user to get sender ID
      final userResponse = await http.get(
        Uri.parse('http://127.0.0.1:8000/api/getUser/$phone'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (userResponse.statusCode == 200) {
        final List userData = jsonDecode(userResponse.body);
        if (userData.isNotEmpty) {
          final user = userData[0];
          final senderId = user['id'];

          // 2. Fetch all staffs and find the first active subadmin
          final staffsResponse = await http.get(
            Uri.parse('http://127.0.0.1:8000/api/staffs/'),
            headers: {
              'Authorization': 'Bearer $token',
              'Content-Type': 'application/json',
            },
          );

          if (staffsResponse.statusCode == 200) {
            final List staffs = jsonDecode(staffsResponse.body);
            final subadmin = staffs.firstWhere(
              (u) => u['user_type'] == 's' && u['is_active'] == true,
              orElse: () => null,
            );

            if (subadmin != null) {
              final receiverId = subadmin['id'];

              // 3. Send message to backend
              final alertResponse = await http.post(
                Uri.parse('http://127.0.0.1:8000/api/messages/'),
                headers: {
                  'Authorization': 'Bearer $token',
                  'Content-Type': 'application/json',
                },
                body: jsonEncode({
                  'sender': senderId,
                  'receiver': receiverId,
                  'content': _alertController.text.trim(),
                }),
              );

              if (alertResponse.statusCode == 201 ||
                  alertResponse.statusCode == 200) {
                Get.snackbar(
                    'Alert Sent', 'Your message has been sent to the subadmin.',
                    snackPosition: SnackPosition.TOP);
                _alertController.clear();
              } else {
                Get.snackbar('Error', 'Failed to send alert.',
                    snackPosition: SnackPosition.TOP,
                    backgroundColor: Colors.red);
              }
            } else {
              Get.snackbar('Error', 'No active subadmin found.',
                  snackPosition: SnackPosition.TOP,
                  backgroundColor: Colors.red);
            }
          } else {
            Get.snackbar('Error', 'Failed to fetch staffs.',
                snackPosition: SnackPosition.TOP, backgroundColor: Colors.red);
          }
        }
      } else {
        Get.snackbar('Error', 'Failed to get user info.',
            snackPosition: SnackPosition.TOP, backgroundColor: Colors.red);
      }
    } catch (e) {
      Get.snackbar('Error', 'An error occurred: $e',
          snackPosition: SnackPosition.TOP, backgroundColor: Colors.red);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: EappBar(
        showBackArrow: true,
        title: Text('Send Alert',
            style: Theme.of(context).textTheme.headlineMedium),
      ),
      body: Padding(
        padding: const EdgeInsets.all(Esizes.defaultSpace),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Write your alert message below:',
                  style: Theme.of(context).textTheme.bodyLarge),
              const SizedBox(height: Esizes.spacebtwItems),

              // Alert TextField
              TextFormField(
                controller: _alertController,
                maxLines: 6,
                decoration: InputDecoration(
                  hintText: 'Enter your alert message...',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return 'Alert message cannot be empty.';
                  }
                  return null;
                },
              ),

              const SizedBox(height: Esizes.spacebtwSections),

              // Send Button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () async => await _sendAlert(),
                  child: const Text('Send Alert'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
