import 'package:quick_trip/features/reservation/screens/driver/profile_setting/profile_setting.dart';
import 'package:quick_trip/features/reservation/screens/driver/home/home.dart';
import 'package:quick_trip/features/reservation/screens/driver/my_ticket/ticket.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:iconsax/iconsax.dart';
import 'package:shared_preferences/shared_preferences.dart';

class NavigationMenuDriver extends StatefulWidget {
  const NavigationMenuDriver({super.key});

  @override
  State<NavigationMenuDriver> createState() => _NavigationMenuDriverState();
}

class _NavigationMenuDriverState extends State<NavigationMenuDriver> {
  final controller = Get.put(NavigationControllerDriver());
  String? _username;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadUsername();
  }

  Future<void> _loadUsername() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      _username = prefs.getString('username') ?? '';
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final darkmode = EHelperFunctions.isDarkMode(context);
    return Scaffold(
      bottomNavigationBar: Obx(
        () => NavigationBar(
            height: 80,
            elevation: 0,
            selectedIndex: controller.selectedIndex.value,
            onDestinationSelected: (index) =>
                controller.selectedIndex.value = index,
            backgroundColor: darkmode
                ? Ecolors.black
                : const Color.fromARGB(255, 243, 240, 240),
            indicatorColor: darkmode
                ? Ecolors.white.withOpacity(0.1)
                : Colors.black.withOpacity(0.1),
            destinations: const [
              NavigationDestination(icon: Icon(Iconsax.home), label: 'Home'),
              NavigationDestination(
                  icon: Icon(Iconsax.ticket), label: 'Exit Slips'),
              NavigationDestination(icon: Icon(Iconsax.user), label: 'Profile'),
            ]),
      ),
      body: Obx(() {
        final screens = [
          const HomeScreen(),
          const MyTicketScreen(),
          // Show a loading indicator until username is loaded
          _isLoading
              ? const Center(child: CircularProgressIndicator())
              : SettingScreen(),
        ];
        return screens[controller.selectedIndex.value];
      }),
    );
  }
}

class NavigationControllerDriver extends GetxController {
  final Rx<int> selectedIndex = 0.obs;
}
