
import 'package:quick_trip/features/reservation/screens/driver/notification/notification.dart';
import 'package:quick_trip/features/reservation/screens/driver/notification/notification_controller.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:iconsax/iconsax.dart';

class NotificationIcon extends StatelessWidget {
  const NotificationIcon({
    super.key,
    this.iconColor,
    required this.onPressed,
    this.counterBgcolor,
    this.counterTextcolor,
  });

  final Color? iconColor, counterBgcolor, counterTextcolor;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);
    final controller = Get.put(NotificationController());

    return Obx(() => Stack(
          children: [
            IconButton(
              onPressed: () {
                controller.clearNotificationCount(); // reset counter
                Get.to(() => const NotificationScreen());
              },
              icon: Icon(Iconsax.notification_bing5, color: iconColor),
            ),
            if (controller.notificationCount.value > 0)
              Positioned(
                right: 0,
                child: Container(
                  width: 15,
                  height: 15,
                  decoration: BoxDecoration(
                    color: counterBgcolor ?? (dark ? Ecolors.red : Ecolors.redLight),
                    borderRadius: BorderRadius.circular(100),
                  ),
                  child: Center(
                    child: Text(
                      '${controller.notificationCount.value}',
                      style: Theme.of(context).textTheme.labelLarge!.apply(
                          color: dark ? Ecolors.dark : Ecolors.white,
                          fontSizeFactor: 0.8),
                    ),
                  ),
                ),
              )
          ],
        ));
  }
}