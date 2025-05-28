import 'package:quick_trip/utils/constants/colors.dart';
import 'package:flutter/material.dart';

class EChipTheme {
  EChipTheme._();

  static ChipThemeData lightChipThemeData =ChipThemeData(
    disabledColor: Ecolors.grey.withOpacity(0.4),
    labelStyle: const TextStyle(color: Ecolors.black),
    selectedColor:Ecolors.primary,
    padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 12), 
    checkmarkColor: Ecolors.white, 
  );

  static ChipThemeData darkChipThemeData =ChipThemeData(
    disabledColor: Ecolors.darkGrey.withOpacity(0.4),
    labelStyle: const TextStyle(color: Ecolors.white),
    selectedColor:Ecolors.primary,
    padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 12), 
    checkmarkColor: Ecolors.white, 
  );
}