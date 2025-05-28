import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

class QueueScreen extends StatefulWidget {
  const QueueScreen({super.key});

  @override
  State<QueueScreen> createState() => _QueueScreenState();
}

class _QueueScreenState extends State<QueueScreen> {
  String driverName = '';
  String phoneNumber = '';
  String address = '';
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchProfile();
  }

  Future<void> _fetchProfile() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final phone = prefs.getString('loginIdentifier');
      final token = prefs.getString('accessToken');

      if (phone != null && token != null) {
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
            setState(() {
              driverName = user['employee']['Fname'] ?? '';
              phoneNumber = user['phone_number']?.toString() ?? '';
              address = user['employee']['address'] ?? '';
              isLoading = false;
            });
          }
        } else {
          debugPrint('Failed to fetch profile: ${userResponse.statusCode}');
          setState(() => isLoading = false);
        }
      }
    } catch (e) {
      debugPrint('Error fetching profile: $e');
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final qrData = jsonEncode({
      'name': driverName,
      'phone': phoneNumber,
      'address': address,
    });

    return Scaffold(
      appBar: EappBar(
        showBackArrow: true,
        title: Text('Take Queue',
            style: Theme.of(context).textTheme.headlineMedium),
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(Esizes.defaultSpace),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const SizedBox(height: 20),
                  Card(
                    elevation: 6,
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16)),
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: Column(
                        children: [
                          Text('Driver Info',
                              style: Theme.of(context).textTheme.headlineSmall),
                          const SizedBox(height: 10),
                          _buildInfoRow('Name', driverName, context),
                          _buildInfoRow('Phone Number', phoneNumber, context),
                          _buildInfoRow('Address', address, context),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 40),
                  Text('Your QR Code',
                      style: Theme.of(context).textTheme.headlineSmall),
                  const SizedBox(height: 20),
                  QrImageView(
                    data: qrData,
                    version: QrVersions.auto,
                    size: 200.0,
                    backgroundColor: Colors.white,
                  ),
                ],
              ),
            ),
    );
  }

  Widget _buildInfoRow(String label, String value, BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text('$label:', style: Theme.of(context).textTheme.bodyMedium),
          Text(value, style: Theme.of(context).textTheme.titleSmall),
        ],
      ),
    );
  }
}
