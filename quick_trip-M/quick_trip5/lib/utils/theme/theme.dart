import 'package:quick_trip/utils/theme/custom_theme/app_bar_theme.dart';
import 'package:quick_trip/utils/theme/custom_theme/bottom_sheet_theme.dart';
import 'package:quick_trip/utils/theme/custom_theme/checkbox_theme.dart';
import 'package:quick_trip/utils/theme/custom_theme/chip_theme.dart';
import 'package:quick_trip/utils/theme/custom_theme/elevated_button_theme.dart';
import 'package:quick_trip/utils/theme/custom_theme/outlined_button_theme.dart';
import 'package:quick_trip/utils/theme/custom_theme/text_field_theme.dart';
import 'package:quick_trip/utils/theme/custom_theme/texttheme.dart';
import 'package:flutter/material.dart';

class EcoTheme {
  EcoTheme._();
  static ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    fontFamily: 'poppins',
    brightness: Brightness.light,
    primaryColor: Colors.blue,
    scaffoldBackgroundColor: Colors.black,
    textTheme: ETextTheme.lightTextTheme,
    elevatedButtonTheme: EEelevatedButtonTheme.lightEelevatedButtonTheme,
    appBarTheme: EAppBarrTheme.lightAppBarrTheme,
    bottomSheetTheme: EBottomshetTheme.lightBottomshetTheme,
    checkboxTheme: ECheckboxTheme.lightCheckboxTheme,
    chipTheme: EChipTheme.lightChipThemeData,
    outlinedButtonTheme: EOutlineButtonTheme.lightOutlinedButtonThemeData,
    inputDecorationTheme: ETextformfieldTheme.lightInputDecorationTheme,
    
  );
  static ThemeData darkTheme = ThemeData(
    useMaterial3: true,
    fontFamily: 'poppins',
    brightness: Brightness.dark,
    primaryColor: Colors.blue,
    scaffoldBackgroundColor: Colors.black,
    textTheme: ETextTheme.darkTextTheme,
    elevatedButtonTheme: EEelevatedButtonTheme.darkEelevatedButtonTheme,
    appBarTheme: EAppBarrTheme.darkAppBarrTheme,
    bottomSheetTheme: EBottomshetTheme.darkBottomshetTheme,
    checkboxTheme: ECheckboxTheme.darkCheckboxTheme,
    chipTheme: EChipTheme.darkChipThemeData,
    outlinedButtonTheme: EOutlineButtonTheme.darkOutlinedButtonThemeData,
    inputDecorationTheme: ETextformfieldTheme.darkInputDecorationTheme,
  );
}
