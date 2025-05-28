import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  Future<List<dynamic>> _fetchHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');

    final response = await http.get(
      Uri.parse('http://127.0.0.1:8000/api/recent/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load history');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: EappBar(
        showBackArrow: true,
        title:
            Text('History', style: Theme.of(context).textTheme.headlineMedium),
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _fetchHistory(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No trip history found.'));
          }

          final trips = snapshot.data!;
          return ListView.builder(
            itemCount: trips.length,
            itemBuilder: (context, index) {
              final trip = trips[index];
              final ticket = trip['ticket'];
              final vehicle = trip['vehicle'];
              final route = ticket['route'];
              final driver = vehicle['user']['employee'];

              return ListTile(
                leading: const Icon(Icons.directions_bus),
                title: Text(route['name']),
                subtitle: Text(
                    'Driver: ${driver['Fname']} ${driver['Lname']}\nPlate: ${vehicle['plate_number']}'),
                trailing: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(ticket['takeoff_date']),
                    Text(ticket['takeoff_time']),
                  ],
                ),
              );
            },
          );
        },
      ),
    );
  }
}
