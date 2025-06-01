import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/utils/constants/sizes.dart';

class AlertScreen extends StatefulWidget {
  const AlertScreen({super.key});

  @override
  State<AlertScreen> createState() => _AlertScreenState();
}

class _AlertScreenState extends State<AlertScreen> {
  final _formKey = GlobalKey<FormState>();
  final _alertController = TextEditingController();

  void _sendAlert() {
    if (_formKey.currentState!.validate()) {
      // TODO: Send alert to bus station via API or backend integration
      Get.snackbar('Alert Sent', 'Your message has been sent to the station.',
          snackPosition: SnackPosition.TOP);
      _alertController.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: EappBar(
        showBackArrow: true,
        title: Text('Send Alert', style: Theme.of(context).textTheme.headlineMedium),
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
                  onPressed: _sendAlert,
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










