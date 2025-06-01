import 'package:quick_trip/utils/constants/image_strings.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/constants/text_strings.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';

class EloginHeader extends StatelessWidget {
  const EloginHeader({
    super.key,
    required this.dark,
  });

  final bool dark;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(
          height: Esizes.spacebtwItems,
        ),
        Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image(
                image:
                    AssetImage(dark ? Eimages.lightappLogo : Eimages.darkappLogo),
                width: EHelperFunctions.screenWidth() * 0.6),
          ],
        ),
   
        Row(
          children: [
            Center(
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(
                  Etext.loginsubTitle,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }
}
