import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';

class OnboardingPage extends StatelessWidget {
  const OnboardingPage({
    super.key,
    required this.image,
    required this.title,
    required this.subtitle,
  });

  final String image, title, subtitle;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(Esizes.defaultSpace),
      child: Column(
        children: [
          Image(
            width: EHelperFunctions.screenHeight() * 0.8,
            height: EHelperFunctions.screenHeight() * 0.6,
            image: AssetImage(image),
          ), // Image
          Text(
            title,
            style: Theme.of(context).textTheme.headlineMedium,
            textAlign: TextAlign.center,
          ), // Text
          const SizedBox(height: Esizes.spacebtwItems),
          Text(
            subtitle,
            style: Theme.of(context).textTheme.bodyMedium,
            textAlign: TextAlign.center,
          ), // Text
        ],
      ),
    );
  }
}

