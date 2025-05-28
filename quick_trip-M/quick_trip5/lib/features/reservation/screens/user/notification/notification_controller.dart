import 'package:get/get.dart';

class NotificationController extends GetxController {
  var notificationCount = 2.obs; // Initial count (you can load from DB/API later)

  void clearNotificationCount() {
    notificationCount.value = 0;
  }

  void increaseCount() {
    notificationCount.value++;
  }
}