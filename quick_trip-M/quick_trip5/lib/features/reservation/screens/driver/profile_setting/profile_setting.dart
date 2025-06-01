import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/common/widgets/custom_shapes/containers/primary_header_container_driver.dart';
import 'package:quick_trip/common/widgets/images/E_circular_image.dart';
import 'package:quick_trip/common/widgets/list_tiles/setting_menu_tile.dart';
import 'package:quick_trip/common/widgets/text/seaction_heading.dart';
import 'package:quick_trip/features/authentication/login/login.dart';
import 'package:quick_trip/features/reservation/screens/driver/profile/profile.dart';
import 'package:quick_trip/features/reservation/screens/driver/notification/notification.dart';
import 'package:quick_trip/features/reservation/screens/driver/queue/queue.dart';
import 'package:quick_trip/features/reservation/screens/driver/alert/alert.dart';
import 'package:quick_trip/features/reservation/screens/driver/history/history.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/constants/image_strings.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:iconsax/iconsax.dart';

class SettingScreen extends StatefulWidget {
  const SettingScreen({super.key});

  @override
  State<SettingScreen> createState() => _SettingScreenState();
}

class _SettingScreenState extends State<SettingScreen> {
  String username = '';
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
        final response = await http.get(
          Uri.parse('http://127.0.0.1:8000/api/getUser/$phone'),
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json',
          },
        );

        if (response.statusCode == 200) {
          final List data = jsonDecode(response.body);
          if (data.isNotEmpty) {
            final user = data[0];
            setState(() {
              username = user['employee']['Fname'] ?? '';
              isLoading = false;
            });
          }
        } else {
          debugPrint('Failed to fetch profile: ${response.statusCode}');
          setState(() => isLoading = false);
        }
      }
    } catch (e) {
      debugPrint('Error fetching profile: $e');
      setState(() => isLoading = false);
    }
  }

  void _showLogoutDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Logout'),
        content: const Text('Are you sure you want to log out?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              // TODO: Clear session/token here
              Get.offAll(() => const LoginScreen());
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Logout'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              child: Column(
                children: [
                  EprimaryHeaderContainer(
                    height: 200,
                    child: Column(
                      children: [
                        EappBar(
                          title: Text(
                            'Account',
                            style: Theme.of(context)
                                .textTheme
                                .headlineMedium!
                                .apply(color: Ecolors.white),
                          ),
                        ),
                        EUserProfileTile(
                          onPressed: () => Get.to(() => const ProfileScreen()),
                          username: username,
                        ),
                        const SizedBox(height: Esizes.spacebtwSections),
                      ],
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(Esizes.defaultSpace),
                    child: Column(
                      children: [
                        const EsectionHeading(
                          title: 'Other Options',
                          showActionbutton: false,
                        ),
                        const SizedBox(height: Esizes.spacebtwItems),
                        ESettingMenuTile(
                          icon: Iconsax.clock,
                          title: ' History',
                          subtitle: 'view your all tickets',
                          onTap: () => Get.to(() => const HistoryScreen()),
                        ),
                        // ESettingMenuTile(
                        //   icon: Iconsax.notification,
                        //   title: ' Notification',
                        //   subtitle: 'see your notification',
                        //   onTap: () => Get.to(() => const NotificationScreen()),
                        // ),
                        ESettingMenuTile(
                          icon: Iconsax.car,
                          title: ' Take Queue',
                          subtitle: 'take your queue number',
                          onTap: () => Get.to(() => const QueueScreen()),
                        ),
                        ESettingMenuTile(
                          icon: Iconsax.alarm,
                          title: ' Alerts',
                          subtitle: 'see your alerts',
                          onTap: () => Get.to(() => const AlertScreen()),
                        ),
                        const SizedBox(height: Esizes.spacebtwItems),
                        SizedBox(
                          width: double.infinity,
                          child: OutlinedButton(
                              onPressed: () {
                                _showLogoutDialog(context);
                              },
                              child: const Text('Logout')),
                        ),
                        const SizedBox(height: Esizes.spacebtwSections * 2.5),
                      ],
                    ),
                  )
                ],
              ),
            ),
    );
  }
}

class EUserProfileTile extends StatelessWidget {
  const EUserProfileTile({
    super.key,
    required this.username,
    this.onPressed,
  });

  final String username;
  final VoidCallback? onPressed;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: const EcircularImage(
          image: Eimages.user, width: 50, height: 50, padding: 0),
      title: Text(
        username,
        style: Theme.of(context)
            .textTheme
            .headlineSmall!
            .apply(color: Ecolors.white),
      ),
      trailing: IconButton(
          onPressed: onPressed,
          icon: const Icon(Iconsax.edit, color: Ecolors.white)),
    );
  }
}
