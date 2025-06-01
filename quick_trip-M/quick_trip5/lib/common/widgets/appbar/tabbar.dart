import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/device/device_utility.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';

class ETabBar extends StatelessWidget implements PreferredSizeWidget {
  const ETabBar({
    super.key,
    required this.tabs,
  });
  final List<Widget> tabs;
  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);
    return Material(
      color: dark ? Ecolors.black : Ecolors.white,
      child: TabBar(
        tabs: tabs,
        isScrollable: true,
        indicatorColor: Ecolors.primary,
        labelColor:
            EHelperFunctions.isDarkMode(context) ? Ecolors.white : Ecolors.dark,
        unselectedLabelColor: Ecolors.darkGrey,
      ),
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(EdeviceUtils.getAppBarHeight());
}

