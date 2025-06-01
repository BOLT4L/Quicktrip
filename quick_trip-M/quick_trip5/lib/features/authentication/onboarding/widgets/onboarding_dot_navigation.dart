import 'package:quick_trip/features/authentication/onboarding/onboarding_controller.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/device/device_utility.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';

class OnboardingdotNavigation extends StatelessWidget {
  const OnboardingdotNavigation({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final controller = OnboardingController.instance;
    final dark = EHelperFunctions.isDarkMode(context);
    return Positioned(
      bottom: EdeviceUtils.getBottomNavigationBarHeight() + 25,
      left: Esizes.defaultSpace,
      child: SmoothPageIndicator(
        count: 3,
        controller: controller.pageController,
        onDotClicked: controller.dotNavigationClick,
        effect: ExpandingDotsEffect(
            activeDotColor: dark ? Ecolors.light : Ecolors.dark, dotHeight: 6),
      ), // SmoothPageIndicator
    );
  }
}
