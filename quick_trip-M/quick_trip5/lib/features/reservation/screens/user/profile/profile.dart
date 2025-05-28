
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/common/widgets/images/E_circular_image.dart';
import 'package:quick_trip/common/widgets/text/seaction_heading.dart';
import 'package:quick_trip/features/reservation/screens/user/profile/widget/profile_menu.dart';
import 'package:quick_trip/utils/constants/image_strings.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const EappBar(showBackArrow: true, title: Text('Profile')),
      //body
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(Esizes.defaultSpace),
          child: Column(
            children: [
              SizedBox(
                width: double.infinity,
                child: Column(
                  children: [
                    const EcircularImage(
                      image: Eimages.user,
                      width: 80,
                      height: 80,
                    ),
                    
                  ],
                ),
              ),
              const SizedBox(height: Esizes.spacebtwItems / 2),
              const Divider(),
              const SizedBox(height: Esizes.spacebtwItems),
              const EsectionHeading(
                title: 'Profile Information',
                showActionbutton: false,
              ),
              const SizedBox(height: Esizes.spacebtwItems),
              // EProfileMenu(
              //     title: 'Name', value: 'xyz'),
              EProfileMenu(
                  title: 'User ID',
                  value: '43323',
                  ),
              EProfileMenu(
                  title: 'Phone Number', value: '0921053296'),
              EProfileMenu(title: 'Gender', value: 'Male'),
              EProfileMenu(
                  title: 'Date of Birth',
                  value: '1 Jan, 2010',
                  ),
              const Divider(),
              
            ],
          ),
        ),
      ),
    );
  }
}
