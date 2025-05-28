
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:quick_trip/features/authentication/login/login.dart';

class OnboardingController extends GetxController {
  static OnboardingController get instance => Get.find();
  //variables
  final pageController = PageController();
  Rx<int> currentPageIndex = 0.obs;

  ///update current index when page scroll
  void updatePageIndicator(index) => currentPageIndex.value = index;

  ///jump to the specific dot selected page
  void dotNavigationClick(int index) {
    currentPageIndex.value = index;
    pageController.animateToPage(
      index,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  ///update current index and jump to next page
  void nextPage() {
  if (currentPageIndex.value == 2) {
    Get.off(()=> LoginScreen(), transition: Transition.noTransition);
  } else {
    int nextPage = currentPageIndex.value + 1;
    pageController.animateToPage(
      nextPage,
      duration: const Duration(milliseconds: 250), // Faster page animation
      curve: Curves.fastEaseInToSlowEaseOut,
    );
  }
}

  ///update current index and jump to the last page
  void skipPage() {
    currentPageIndex.value = 2;
    pageController.animateToPage(
      2,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

}














// import 'package:ecomerce/feuteres/authentication/login/login.dart';
// import 'package:flutter/material.dart';
// import 'package:get/get.dart';
// import 'package:shared_preferences/shared_preferences.dart';

// class OnboardingController extends GetxController {
//   static OnboardingController get instance => Get.find();

//   void completeOnboarding() async {
//     SharedPreferences prefs = await SharedPreferences.getInstance();
//     await prefs.setBool('onboardingCompleted', true); // Save status

//     Get.off(const LoginScreen(), transition: Transition.noTransition); // Go to login
//   }
//   // Variables
//   final PageController pageController = PageController();
//   Rx<int> currentPageIndex = 0.obs;

//   /// Update current index when page scrolls
//   void updatePageIndicator(int index) => currentPageIndex.value = index;

//   /// Jump to the specific dot-selected page
//   void dotNavigationClick(int index) {
//     currentPageIndex.value = index;
//     pageController.animateToPage(
//       index,
//       duration: const Duration(milliseconds: 300),
//       curve: Curves.easeInOut,
//     );
//   }

//   /// Update current index and jump to the next page
//   /// 
//   void nextPage() {
//   if (currentPageIndex.value == 2) {
//     Get.off(()=> LoginScreen(), transition: Transition.noTransition);
//   } else {
//     int nextPage = currentPageIndex.value + 1;
//     pageController.animateToPage(
//       nextPage,
//       duration: const Duration(milliseconds: 250), // Faster page animation
//       curve: Curves.fastEaseInToSlowEaseOut,
//     );
//   }
// }

//   /// 
//   /// 
//   /// 
//   // void nextPage() {
//   //   if (currentPageIndex.value == 2) {
//   //      Get.to(const LoginScreen());
//   //   } else {
//   //     int nextPage = currentPageIndex.value + 1;
//   //     pageController.animateToPage(
//   //       nextPage,
//   //       duration: const Duration(milliseconds: 300),
//   //       curve: Curves.easeInOut,
//   //     );
//   //   }
//   // }

//   /// Update current index and jump to the last page
//   void skipPage() {
//     currentPageIndex.value = 2;
//     pageController.animateToPage(
//       2,
//       duration: const Duration(milliseconds: 300),
//       curve: Curves.easeInOut,
//     );
//   }
// }