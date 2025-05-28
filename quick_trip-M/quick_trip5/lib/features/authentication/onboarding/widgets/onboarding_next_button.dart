import 'package:quick_trip/features/authentication/onboarding/onboarding_controller.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/device/device_utility.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';
import 'package:iconsax/iconsax.dart';
class OnboardingNextButton extends StatelessWidget {
  const OnboardingNextButton({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);
    return Positioned(
        right: Esizes.defaultSpace,
        bottom: EdeviceUtils.getBottomNavigationBarHeight(),
        child: ElevatedButton(
          onPressed: () => OnboardingController.instance.nextPage(),
          style: ElevatedButton.styleFrom(
              shape:  CircleBorder(),
              backgroundColor: dark ? Ecolors.primary : Colors.black),
              
          child: const Icon(Iconsax.arrow_right_3),
          
        ));
  }
}
