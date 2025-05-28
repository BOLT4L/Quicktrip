import 'package:flutter/material.dart';
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/features/reservation/screens/user/history/history_list.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: EappBar(
        showBackArrow: true,
        title: Text('History', style: Theme.of(context).textTheme.headlineMedium),
      ),
      body: const HistoryList(),
    );
  }
}
