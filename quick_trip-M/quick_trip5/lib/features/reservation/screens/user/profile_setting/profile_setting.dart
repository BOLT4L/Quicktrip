import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/common/widgets/custom_shapes/containers/primary_header_container.dart';
import 'package:quick_trip/common/widgets/images/E_circular_image.dart';
import 'package:quick_trip/common/widgets/list_tiles/setting_menu_tile.dart';
import 'package:quick_trip/features/authentication/login/login.dart';
import 'package:quick_trip/features/reservation/screens/user/change_password/change_pass.dart';
import 'package:quick_trip/features/reservation/screens/user/profile/profile.dart';
import 'package:quick_trip/features/reservation/screens/user/notification/notification.dart';
import 'package:quick_trip/features/reservation/screens/user/alert/alert.dart';
import 'package:quick_trip/features/reservation/screens/user/history/history.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/constants/image_strings.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:iconsax/iconsax.dart';

class SettingScreen extends StatelessWidget {
  const SettingScreen({super.key});

  void _showLogoutDialog(BuildContext context) {
  showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: const Text('Logout'),
      content: const Text('Are you sure you want to log out?'),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: () {
            // TODO: Clear session/token here

            Get.offAll(() => const LoginScreen());
          },
          style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
          child: const Text('Logout'),
        ),
      ],
    ),
  );
}


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            EprimaryHeaderContainer(
                height: 200,
                child: Column(
                  children: [
                    //appbar
                    EappBar(
                      title: Text(
                        'Account',
                        style: Theme.of(context)
                            .textTheme
                            .headlineMedium!
                            .apply(color: Ecolors.white),
                      ),
                    ),
                    //user profile
                    EUserProfileTile(
                      onPressed: () => Get.to(() => const ProfileScreen()),
                    ),
                    const SizedBox(height: Esizes.spacebtwSections),
                  ],
                )),
            //body
            Padding(
              padding: const EdgeInsets.all(Esizes.defaultSpace),
              child: Column(
                children: [
                  //account setting
                  SizedBox(
                    child: Container(
                      alignment: Alignment.centerLeft,
                      child: Text('Other Options',
                                style: Theme.of(context).textTheme.headlineSmall),
                    ),
                  ),
                        
                  const SizedBox(height: Esizes.spacebtwItems),
                  ESettingMenuTile(
                    icon: Iconsax.clock,
                    title: ' History',
                    subtitle: 'view your over all purchased tickets',
                    onTap: () => Get.to(() => const HistoryScreen()),
                  ),
                  ESettingMenuTile(
                    icon: Iconsax.notification,
                    title: ' Notification',
                    subtitle: 'see your notification',
                    onTap: () => Get.to(() => const NotificationScreen()),
                  ),
                 
                  ESettingMenuTile(
                    icon: Iconsax.alarm,
                    title: ' Alerts',
                    subtitle: 'see your alerts',
                    onTap: ()=> Get.to(()=> const AlertScreen()),
                  ),

                  ESettingMenuTile(
                    icon: Iconsax.lock,
                    title: 'Change Password',
                    subtitle: 'Update your login password',
                    onTap: () => Get.to(() => const ChangePasswordScreen()),
                  ),


                  //logout button
                  const SizedBox(height: Esizes.spacebtwItems),
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton(
                        onPressed: () {
                            _showLogoutDialog(context);
                          },
                          child: const Text('Logout')),
                  ),
                  const SizedBox(height: Esizes.spacebtwSections * 2.5),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}









class EUserProfileTile extends StatelessWidget {
  const EUserProfileTile({
    super.key,
    this.onPressed,
  });
  final VoidCallback? onPressed;
  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: const EcircularImage(
          image: Eimages.user, width: 50, height: 50, padding: 0),
      title: Text('',
          style: Theme.of(context)
              .textTheme          
              .headlineSmall!
              .apply(color: Ecolors.white)),
      subtitle: Text('view your profile',
          style: Theme.of(context)
              .textTheme
              .bodyMedium!
              .apply(color: Ecolors.white)),
      trailing: IconButton(
          onPressed: onPressed,
          icon: const Icon(Iconsax.edit, color: Ecolors.white)),
    );
  }
}