import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

// -----------------------
// User Model
// -----------------------
class UserProfile {
  final int id;
  final String userType;
  final bool isActive;
  final int phoneNumber;
  final String dateJoined;
  final String name;

  UserProfile({
    required this.id,
    required this.userType,
    required this.isActive,
    required this.phoneNumber,
    required this.dateJoined,
    required this.name,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      name: json['employee']['Fname'],
      id: json['id'],
      userType: json['user_type'],
      isActive: json['is_active'],
      phoneNumber: json['phone_number'],
      dateJoined: json['date_joined'],
    );
  }
}

// -----------------------
// Profile Screen
// -----------------------
class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  UserProfile? _userProfile;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? phoneStr = prefs.getString('loginIdentifier');

    if (phoneStr != null) {
      try {
        SharedPreferences prefs = await SharedPreferences.getInstance();
        String? token = prefs.getString('accessToken'); // Retrieve token

        final url = Uri.parse('http://127.0.0.1:8000/api/getUser/$phoneStr');

        final response = await http.get(
          url,
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json',
          },
        );
        // Check if the response is successful
        if (response.statusCode == 200) {
          final List<dynamic> data = jsonDecode(response.body);
          // If the list is not empty, update the state with the first user's profile data
          // and set loading to false.
          if (data.isNotEmpty) {
            setState(() {
              _userProfile = UserProfile.fromJson(data[0]);
              _isLoading = false;
            });

            // Save username to SharedPreferences
            SharedPreferences prefs = await SharedPreferences.getInstance();
            await prefs.setString('username', _userProfile!.name);
          }
        } else {
          throw Exception('Failed to load profile: ${response.statusCode}');
        }
      } catch (e) {
        debugPrint('Error: $e');
        setState(() {
          _isLoading = false;
        });
      }
    } else {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Widget buildInfoTile(String title, String value) {
    return ListTile(
      title: Text(title),
      subtitle: Text(value),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _userProfile == null
              ? const Center(child: Text('No profile data found'))
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [
                      // const CircleAvatar(
                      //   radius: 40,
                      //   backgroundImage: AssetImage('assets/images/user.png'),
                      // ),
                      const SizedBox(height: 20),
                      buildInfoTile('Username', _userProfile!.name.toString()),
                      buildInfoTile('User ID', _userProfile!.id.toString()),
                      buildInfoTile(
                          'Phone Number', _userProfile!.phoneNumber.toString()),
                      buildInfoTile('User Type', _userProfile!.userType),
                      buildInfoTile(
                          'Active', _userProfile!.isActive ? 'Yes' : 'No'),
                      buildInfoTile('Joined', _userProfile!.dateJoined),
                    ],
                  ),
                ),
    );
  }
}
