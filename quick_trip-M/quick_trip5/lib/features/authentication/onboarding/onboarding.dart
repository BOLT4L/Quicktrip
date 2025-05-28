import 'package:quick_trip/features/authentication/onboarding/onboarding_controller.dart';
import 'package:quick_trip/features/authentication/onboarding/widgets/onboarding_dot_navigation.dart';
import 'package:quick_trip/features/authentication/onboarding/widgets/onboarding_next_button.dart';
import 'package:quick_trip/features/authentication/onboarding/widgets/onboarding_page.dart';
import 'package:quick_trip/features/authentication/onboarding/widgets/onboarding_skip.dart';
import 'package:flutter/material.dart';
import 'package:quick_trip/utils/constants/image_strings.dart';
import 'package:quick_trip/utils/constants/text_strings.dart';
import 'package:get/get.dart';


class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context) {

    final controller = Get.put(OnboardingController());
    return Scaffold(
      body: Stack(
        children: [
          //horizontal scrollable pages
          PageView(
            controller: controller.pageController,
            onPageChanged: controller.updatePageIndicator,
            children: const [
              OnboardingPage(
                image: Eimages.onboardingImage1,
                title: Etext.onboardingTitle1,
                subtitle: Etext.onboardingsubTitle1,
              ), // Column
              OnboardingPage(
                image: Eimages.onboardingImage2,
                title: Etext.onboardingTitle2,
                subtitle: Etext.onboardingsubTitle2,
              ),
              OnboardingPage(
                image: Eimages.onboardingImage3, 
                title: Etext.onboardingTitle3,
                subtitle: Etext.onboardingsubTitle3,
              )
            ],
          ), // PageView

          //skip button
          const OnboardingSkip(),

          //dot navigation smoothpageindicator
          const OnboardingdotNavigation(), // Positioned

          //circullar button
          const OnboardingNextButton()

        ],
      ),
    );
  }
}
