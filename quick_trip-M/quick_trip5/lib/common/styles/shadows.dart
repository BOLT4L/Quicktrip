import 'package:quick_trip/utils/constants/colors.dart';
import 'package:flutter/material.dart';

class EshadowsStyle {
  static final verticalProductShadow = BoxShadow(
    color: Ecolors.darkGrey.withOpacity(0.1),
    blurRadius: 50,
    spreadRadius: 7,
    offset: const Offset(0, 2)

  );
   static final horizontalProductShadow = BoxShadow(
    color: Ecolors.darkGrey.withOpacity(0.1),
    blurRadius: 50,
    spreadRadius: 7,
    offset: const Offset(0, 2)

  );

}