import 'package:flutter/material.dart';
import 'package:quick_trip/features/reservation/screens/driver/history/history_detail.dart';
import 'package:quick_trip/utils/constants/sizes.dart';

class HistoryList extends StatelessWidget {
  const HistoryList({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, String>> historyData = [
      {"date": "March 30, 2025", "route": "Addis Ababa → Adama", "status": "Completed"},
      {"date": "March 28, 2025", "route": "Bishoftu → Adama", "status": "Completed"},
    ];

    return historyData.isEmpty
        ? Center(
            child: Text(
              "No History Found",
              style: Theme.of(context).textTheme.bodyLarge,
            ),
          )
        : ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            padding: const EdgeInsets.all(Esizes.spacebtwItems),
            itemCount: historyData.length,
            separatorBuilder: (_, __) => const SizedBox(height: Esizes.spacebtwItems),
            itemBuilder: (context, index) {
              final trip = historyData[index];
              return Card(
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                elevation: 3,
                child: ListTile(
                  contentPadding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                  leading: const Icon(Icons.directions_bus, color: Colors.blue),
                  title: Text(trip["route"]!, style: const TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: Text(trip["date"]!),
                  trailing: Text(
                    trip["status"]!,
                    style: TextStyle(
                      color: trip["status"] == "Completed" ? Colors.green : Colors.red,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => HistoryDetailScreen(trip: trip),
                      ),
                    );
                  },
                ),
              );

            },
          );
  }
}
