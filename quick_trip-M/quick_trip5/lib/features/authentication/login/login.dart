import 'package:quick_trip/features/authentication/login/widgets/login_form.dart';
import 'package:quick_trip/features/authentication/login/widgets/login_header.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';


class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final PageController _pageController = PageController();
  int _selectedIndex = 0; // 0 for User, 1 for Driver

  void _switchLogin(int index) {
    setState(() {
      _selectedIndex = index;
      _pageController.animateToPage(index,
          duration: const Duration(milliseconds: 300), curve: Curves.easeInOut);
    });
  }

  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);
    
    return Scaffold(
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.all(Esizes.spacebtwItems),
          child: Column(
            children: [
              // Logo, Title, Subtitle
              EloginHeader(dark: dark),
              const SizedBox(height: Esizes.spacebtwSections),

              // Toggle Buttons for User & Driver Login
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _buildToggleButton("User", 0),
                  _buildToggleButton("Driver", 1),
                ],
              ),
              const SizedBox(height: Esizes.spacebtwItems),

              // PageView for Switching Between User & Driver Login
              SizedBox(
                height: 500, 
                child: PageView(
                  controller: _pageController,
                  onPageChanged: (index) => setState(() => _selectedIndex = index),
                  children: const [
                    ELoginForm(userType: "User"), // User Login Form
                    ELoginForm(userType: "Driver"), // Driver Login Form
                  ],
                ),
              ),

            ],
          ),
        ),
      ),
    );
  }

  Widget _buildToggleButton(String text, int index) {
    return GestureDetector(
      onTap: () => _switchLogin(index),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 20),
        margin: const EdgeInsets.symmetric(horizontal: 10),
        decoration: BoxDecoration(
          color: _selectedIndex == index ? Colors.blue : Colors.grey[300],
          borderRadius: BorderRadius.circular(10),
        ),
        child: Text(
          text,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: _selectedIndex == index ? Colors.white : Colors.black,
          ),
        ),
      ),
    );
  }
}


















// class Loginscreen extends StatelessWidget {
//   const Loginscreen({super.key});

//   @override
//   Widget build(BuildContext context) {
//     final dark = EHelperFunctions.isDarkMode(context);
//     return Scaffold(
//       body: SingleChildScrollView(
//         child: Padding(
//           padding: EspacingStyles.paddingwithAppbarHeight,
//           child: Column(
//             children: [
//               //logo, title,subtitle
//               EloginHeader(dark: dark),
//               //form
//               const EloginForm(),
//               //divider
//               EformDivider(),
//               const SizedBox(height: Esizes.spacebtwSections),
//               //footer
//               const EsocialButton()
//             ],
//           ),
//         ),
//       ),
//     );
//   }
// }



