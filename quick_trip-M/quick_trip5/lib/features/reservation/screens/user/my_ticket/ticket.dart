
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/features/reservation/screens/user/notification/notification_icon_user.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:flutter/material.dart';
import 'package:iconsax/iconsax.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:qr_flutter/qr_flutter.dart';

class MyTicketScreen extends StatelessWidget {
  const MyTicketScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);
    return Scaffold(
      appBar: EappBar(
        title:
            Text('My Ticket', style: Theme.of(context).textTheme.headlineMedium),
        actions: [
          NotificationIcon(
            onPressed: () {},
            iconColor: dark ? Ecolors.white : Ecolors.dark,
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(Esizes.defaultSpace),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TicketCard(),
          ],
        ),
      ),
    );
  }
}

class TicketCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);
    return Container(
      padding: const EdgeInsets.all(Esizes.md),
      decoration: BoxDecoration(
        color: dark ? Ecolors.darkGrey : Ecolors.lightContainer,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black12,
            blurRadius: 6,
            spreadRadius: 2,
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('From', style: Theme.of(context).textTheme.labelLarge),
                  Text('Addis Ababa',
                      style: Theme.of(context)
                          .textTheme
                          .headlineSmall!
                          .apply(fontWeightDelta: 2)),
                ],
              ),
              Icon(Iconsax.bus, size: 32, color: Ecolors.primary),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text('To', style: Theme.of(context).textTheme.labelLarge),
                  Text('Dire Dawa',
                      style: Theme.of(context)
                          .textTheme
                          .headlineSmall!
                          .apply(fontWeightDelta: 2)),
                ],
              ),
            ],
          ),
          const SizedBox(height: Esizes.md),
          Divider(color: Ecolors.grey.withOpacity(0.4)),
          const SizedBox(height: Esizes.md),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Date', style: Theme.of(context).textTheme.labelLarge),
                  Text('March 30, 2025',
                      style: Theme.of(context)
                          .textTheme
                          .headlineSmall!
                          .apply(fontWeightDelta: 2)),
                ],
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text('Status', style: Theme.of(context).textTheme.labelLarge),
                  Text('Pending...',
                      style: Theme.of(context)
                          .textTheme
                          .headlineSmall!
                          .apply(fontWeightDelta: 2, color: Ecolors.primary)),
                ],
              ),
            ],
          ),
          const SizedBox(height: Esizes.md),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Level :', style: Theme.of(context).textTheme.titleMedium),
                  Text('Subtotal :', style: Theme.of(context).textTheme.titleMedium),
                  Text('Service Fee :', style: Theme.of(context).textTheme.titleMedium),
                  Text('Tax Fee :', style: Theme.of(context).textTheme.titleMedium),
                  Text('Total:', style: Theme.of(context).textTheme.titleMedium),
                ],
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text('Level 2', style: Theme.of(context).textTheme.titleMedium),
                  Text('200', style: Theme.of(context).textTheme.titleMedium),
                  Text('5', style: Theme.of(context).textTheme.titleMedium),
                  Text('5', style: Theme.of(context).textTheme.titleMedium),
                  Text('210', style: Theme.of(context).textTheme.titleMedium),

                ],
              ),
            ],
          ),
          const SizedBox(height: Esizes.lg),
          Center(
            child: QrImageView(
              data: '1234567890',
              size: 100,
              backgroundColor: Colors.white,
            ),
          ),
        ],
      ),
    );
  }
}
