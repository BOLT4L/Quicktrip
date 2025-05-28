import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';

class EcircularImage extends StatelessWidget {
  const EcircularImage({
    super.key,
    this.width = 56,
    this.height = 56,
    this.padding = Esizes.sm,
    required this.image,
    this.overlayColor,
    this.backgroundColor,
    this.fit = BoxFit.cover,
    this.isNetworkImage = false,
  });

  final double width, height, padding;
  final String image;
  final Color? overlayColor;
  final Color? backgroundColor;
  final BoxFit? fit;
  final bool isNetworkImage;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      padding: EdgeInsets.all(padding),
      decoration: BoxDecoration(
        color: backgroundColor ??
            (EHelperFunctions.isDarkMode(context)
                ? Ecolors.black
                : Ecolors.white),
        borderRadius: BorderRadius.circular(100),
      ),
      child: Image(
          fit: fit,
          image: isNetworkImage
              ? NetworkImage(image)
              : AssetImage(image) as ImageProvider,
          color: overlayColor),
    );
  }
}
