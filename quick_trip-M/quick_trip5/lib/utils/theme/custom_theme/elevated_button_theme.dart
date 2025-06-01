import 'package:flutter/material.dart';
class EEelevatedButtonTheme {
  EEelevatedButtonTheme._();
  static final lightEelevatedButtonTheme =ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      elevation: 0.0,
      foregroundColor: Colors.white,
      backgroundColor: Colors.blue,
      disabledForegroundColor: Colors.grey,
      disabledBackgroundColor: Colors.grey,
      side: const BorderSide(color: Colors.blue),
      padding:const EdgeInsets.symmetric(vertical: 18),
      textStyle:const TextStyle(fontSize: 16, color: Colors.white, fontWeight: FontWeight.w600),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),


    ),
  );
  static final darkEelevatedButtonTheme =ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
      elevation: 0.0,
      foregroundColor: Colors.white,
      backgroundColor: Colors.blue,
      disabledForegroundColor: Colors.grey,
      disabledBackgroundColor: Colors.grey,
      side: const BorderSide(color: Colors.blue),
      padding:const EdgeInsets.symmetric(vertical: 18),
      textStyle:const TextStyle(fontSize: 16, color: Colors.white, fontWeight: FontWeight.w600),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      
      ),
  );
}