import 'package:flutter/material.dart';

class HistoryDetailScreen extends StatelessWidget {
  final Map<String, String> trip;

  const HistoryDetailScreen({super.key, required this.trip});

  Widget buildRow(String label, String value, BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: Theme.of(context).textTheme.bodyMedium),
          Text(
            value,
            style: Theme.of(context).textTheme.bodyLarge!.copyWith(
              fontWeight: FontWeight.w500,
              color: label == 'Status' && value == 'Completed'
                  ? Colors.green
                  : (label == 'Status' ? Colors.red : null),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Trip Details'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Card(
          elevation: 3,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                buildRow('Route', trip['route'] ?? '-', context),
                const Divider(),
                buildRow('Date', trip['date'] ?? '-', context),
                const Divider(),
                buildRow('Status', trip['status'] ?? '-', context),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
