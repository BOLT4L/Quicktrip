import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/features/reservation/screens/user/notification/notification_icon_user.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/constants/text_strings.dart';
import 'package:flutter/material.dart';

class EHomeAppBar extends StatelessWidget {
  const EHomeAppBar({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return EappBar(
      title: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(Etext.homeappbarTitle,
              style: Theme.of(context)
                  .textTheme
                  .labelMedium!
                  .apply(color: Ecolors.grey)),
          Text(Etext.homeappbarsubTitle,
              style: Theme.of(context)
                  .textTheme
                  .headlineSmall!
                  .apply(color: Ecolors.white))
        ],
      ),
      actions: [
        NotificationIcon(onPressed: (){}, iconColor:Ecolors.white,)
      ],
    );
  }
}
