import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:flutter/material.dart';

class NotificationScreen extends StatelessWidget {
  const NotificationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final notifications = [
      {
        'title': 'Trip Confirmed',
        'message': 'Your ticket for Addis Ababa → Hawassa is confirmed.',
        'date': 'April 14, 2025'
      },
      {
        'title': 'System Notice',
        'message': 'Our service will be down for maintenance at 10 PM.',
        'date': 'April 12, 2025'
      },
      
    ];

    return Scaffold(
      appBar: EappBar(
        showBackArrow: true,
        title: Text(
          'Notification',
          style: Theme.of(context).textTheme.headlineMedium,
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(Esizes.defaultSpace),
        child: ListView.separated(
          itemCount: notifications.length,
          separatorBuilder: (_, __) => const SizedBox(height: Esizes.spacebtwItems),
          itemBuilder: (context, index) {
            final notif = notifications[index];
            return Card(
              elevation: 3,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12)),
              child: ListTile(
                contentPadding: const EdgeInsets.all(16),
                title: Text(notif['title']!,
                    style: Theme.of(context).textTheme.titleMedium),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: 4),
                    Text(notif['message']!),
                    const SizedBox(height: 8),
                    Text(notif['date']!,
                        style: Theme.of(context)
                            .textTheme
                            .labelSmall!
                            .copyWith(color: Colors.grey)),
                  ],
                ),
                leading: const Icon(Icons.notifications_active, color: Colors.blue),
              ),
            );
          },
        ),
      ),
    );
  }
}
