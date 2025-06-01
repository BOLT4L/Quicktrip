import 'package:quick_trip/features/authentication/onboarding/onboarding.dart';
import 'package:quick_trip/utils/theme/theme.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class App extends StatelessWidget {
  const App({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      debugShowCheckedModeBanner: false,
      themeMode: ThemeMode.system,
      theme: EcoTheme.lightTheme,
      darkTheme: EcoTheme.darkTheme,
      home: const OnboardingScreen(),
    );
  }
}















// class App extends StatelessWidget {
//   const App({super.key});

//   // This widget is the root of your application.
//   @override
//   Widget build(BuildContext context) {
//     return GetMaterialApp(
//       debugShowCheckedModeBanner: false,
//       themeMode: ThemeMode.system,
//       theme: EcoTheme.lightTheme,
//       darkTheme: EcoTheme.darkTheme,
//       home: const OnboardingScreen(),
//     );
//   }
// }
