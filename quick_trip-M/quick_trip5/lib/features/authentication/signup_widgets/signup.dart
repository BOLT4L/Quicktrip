import 'package:quick_trip/features/authentication/signup_widgets/widgets/signup_form.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/constants/text_strings.dart';
import 'package:flutter/material.dart';

class SignupScreen extends StatelessWidget {
  const SignupScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(Esizes.defaultSpace),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              //title
              Text(Etext.signupTitle,
                  style: Theme.of(context).textTheme.headlineMedium),
              const SizedBox(height: Esizes.spacebtwSections),

              //form
              EsignupForm(),
              const SizedBox(height: Esizes.spacebtwSections),

            ],
          ),
        ),
      ),
    );
  }
}
