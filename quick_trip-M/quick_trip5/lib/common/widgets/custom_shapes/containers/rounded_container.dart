import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:flutter/material.dart';

import 'package:quick_trip/utils/constants/colors.dart';

class EroundedContainer extends StatelessWidget {
  const EroundedContainer({
    super.key,
    this.width,
    this.height,
    this.radius = Esizes.cardradiusLg,
    this.padding,
    this.margin,
    this.child,
    this.showBorder = false,
    this.borderColor = Ecolors.borderPrimary,
    this.backgroundcolor = Ecolors.white,
  });

  final double? width;
  final double? height;
  final double radius;
  final EdgeInsetsGeometry? padding;
  final EdgeInsetsGeometry? margin;
  final Widget? child;
  final Color backgroundcolor;
  final bool showBorder;
  final Color borderColor;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      margin: margin,
      padding: padding,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(radius),
        color: backgroundcolor,
        border: showBorder
            ? Border.all(
                color: borderColor) // Apply border only if showBorder is true
            : null,
      ),
      child: child,
    );
  }
}
