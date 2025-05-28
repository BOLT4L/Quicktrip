import 'package:quick_trip/features/reservation/screens/user/profile_setting/profile_setting.dart';
import 'package:quick_trip/features/reservation/screens/user/home/home.dart';
import 'package:quick_trip/features/reservation/screens/user/my_ticket/ticket.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:iconsax/iconsax.dart';

class NavigationMenu extends StatelessWidget {
  const NavigationMenu({super.key});
  @override
  Widget build(BuildContext context) {
    final controller = Get.put(NavigationController());
    final darkmode = EHelperFunctions.isDarkMode(context);
    return Scaffold(
      bottomNavigationBar: Obx(
        () => NavigationBar(
            height: 80,
            elevation: 0,
            selectedIndex: controller.selectedIndex.value,
            onDestinationSelected: (index) =>
                controller.selectedIndex.value = index,
            backgroundColor: darkmode ? Ecolors.black : const Color.fromARGB(255, 243, 240, 240),
            indicatorColor: darkmode
                ? Ecolors.white.withOpacity(0.1)
                : Colors.black.withOpacity(0.1),
            destinations: const [
              NavigationDestination(icon: Icon(Iconsax.home), label: 'Home'),
              NavigationDestination(
                  icon: Icon(Iconsax.ticket), label: 'Tickets'),
              NavigationDestination(icon: Icon(Iconsax.user), label: 'Profile'),
            ]),
      ),
      body: Obx(() => controller.screens[controller.selectedIndex.value]),
    );
  }
}

class NavigationController extends GetxController {
  final Rx<int> selectedIndex = 0.obs;
  final screens = [
    const HomeScreen(),
    const MyTicketScreen(),
    const SettingScreen(),
  ];
}
