import 'package:http/http.dart' as http;
import 'dart:convert';

class AuthService {
  static const String baseUrl =
      'http://127.0.0.1:8000'; // Replace with your API URL

  // User login
  static Future<Map<String, dynamic>> userLogin(
      String phone, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/token'),
      body: jsonEncode({
        'phone': phone,
        'password': password,
      }),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to login: ${response.body}');
    }
  }

  // Driver login
  static Future<Map<String, dynamic>> driverLogin(
      String plate, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/token'),
      body: jsonEncode({
        'phone_number': plate,
        'password': password,
      }),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to login: ${response.body}');
    }
  }
}
