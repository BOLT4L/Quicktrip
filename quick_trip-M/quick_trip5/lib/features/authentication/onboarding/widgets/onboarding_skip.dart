import 'package:quick_trip/features/authentication/onboarding/onboarding_controller.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/device/device_utility.dart';
import 'package:flutter/material.dart';

class OnboardingSkip extends StatelessWidget {
  const OnboardingSkip({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Positioned(
        top: EdeviceUtils.getAppBarHeight(),
        right: Esizes.defaultSpace,
        child: TextButton(
            onPressed: () => OnboardingController.instance.skipPage(),
            child: const Text('skip')));
  }
}
