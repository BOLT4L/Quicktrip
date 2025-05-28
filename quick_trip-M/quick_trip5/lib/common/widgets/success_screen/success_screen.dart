import 'package:quick_trip/common/styles/spacing_styles.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/constants/text_strings.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';

class SuccessScreen extends StatelessWidget {
  const SuccessScreen(
      {super.key,
      this.image,
      this.title,
      this.subtitle,
      required this.onPressed});
  // ignore: prefer_typing_uninitialized_variables
  final image, title, subtitle;
  final VoidCallback onPressed;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Padding(
          padding: EspacingStyles.paddingwithAppbarHeight * 2,
          child: Column(
            children: [
              //image
              Image(
                image: AssetImage(image),
                width: EHelperFunctions.screenWidth() * 0.6,
              ),
              const SizedBox(height: Esizes.spacebtwSections),
              //title and subtitle
              Text(title,
                  style: Theme.of(context).textTheme.headlineMedium,
                  textAlign: TextAlign.center),

              const SizedBox(height: Esizes.spacebtwSections),
              Text(subtitle,
                  style: Theme.of(context).textTheme.labelMedium,
                  textAlign: TextAlign.center),
              const SizedBox(height: Esizes.spacebtwItems),
              //buttons
              SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                      onPressed: onPressed,
                      child: const Text(Etext.eContinue))),
              const SizedBox(height: Esizes.spacebtwItems),
            ],
          ),
        ),
      ),
    );
  }
}
