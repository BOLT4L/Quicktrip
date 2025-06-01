import 'dart:convert';
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/features/reservation/screens/driver/notification/notification_icon_driver.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:flutter/material.dart';
import 'package:iconsax/iconsax.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';

class MyTicketScreen extends StatefulWidget {
  const MyTicketScreen({super.key});

  @override
  State<MyTicketScreen> createState() => _MyTicketScreenState();
}

class _MyTicketScreenState extends State<MyTicketScreen> {
  late Future<List<ExitSlip>> _exitSlipsFuture;

  @override
  void initState() {
    super.initState();
    _exitSlipsFuture = _fetchExitSlips();
  }

  Future<List<ExitSlip>> _fetchExitSlips() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');

    final response = await http.get(
      Uri.parse('http://127.0.0.1:8000/api/exit-slips/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List data = json.decode(response.body);
      return data.map((e) => ExitSlip.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load exit slips');
    }
  }

  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);
    return Scaffold(
      appBar: EappBar(
        title: Text('My Exit Slips',
            style: Theme.of(context).textTheme.headlineMedium),
        actions: [
          NotificationIcon(
            onPressed: () {},
            iconColor: dark ? Ecolors.white : Ecolors.dark,
          )
        ],
      ),
      body: FutureBuilder<List<ExitSlip>>(
        future: _exitSlipsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Failed to load exit slips'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No exit slips found.'));
          }
          final slips = snapshot.data!;
          return RefreshIndicator(
            onRefresh: () async {
              setState(() {
                _exitSlipsFuture = _fetchExitSlips();
              });
            },
            child: ListView.builder(
              padding: const EdgeInsets.all(Esizes.defaultSpace),
              itemCount: slips.length,
              itemBuilder: (context, index) {
                final slip = slips[index];
                return Padding(
                  padding: const EdgeInsets.only(bottom: Esizes.lg),
                  child: TicketCard(
                    from: slip.from,
                    to: slip.to,
                    plateNumber: slip.plateNumber,
                    date: slip.date,
                    passengerCount: slip.passengerCount,
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

class ExitSlip {
  final String from;
  final String to;
  final String plateNumber;
  final String date;
  final int passengerCount;

  ExitSlip({
    required this.from,
    required this.to,
    required this.plateNumber,
    required this.date,
    required this.passengerCount,
  });

  factory ExitSlip.fromJson(Map<String, dynamic> json) {
    // Format date as needed
    String formattedDate = '';
    if (json['departure_time'] != null) {
      try {
        final dt = DateTime.parse(json['departure_time']);
        formattedDate = DateFormat('yyyy-MM-dd – kk:mm').format(dt);
      } catch (_) {
        formattedDate = json['departure_time'].toString();
      }
    }
    return ExitSlip(
      from: json['from_location'] ?? '',
      to: json['to_location'] ?? '',
      plateNumber: json['vehicle_plate'] ?? '',
      date: formattedDate,
      passengerCount: json['passenger_count'] ?? 0,
    );
  }
}

class TicketCard extends StatelessWidget {
  final String from;
  final String to;
  final String plateNumber;
  final String date;
  final int passengerCount;

  const TicketCard({
    super.key,
    required this.from,
    required this.to,
    required this.plateNumber,
    required this.date,
    required this.passengerCount,
  });

  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);
    final qrData = jsonEncode({
      'plate_number': plateNumber,
      'from': from,
      'to': to,
      'date': date,
      'passenger_count': passengerCount,
    });

    return Container(
      padding: const EdgeInsets.all(Esizes.md),
      decoration: BoxDecoration(
        color: dark ? Ecolors.darkGrey : Ecolors.lightContainer,
        borderRadius: BorderRadius.circular(16),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 6, spreadRadius: 2),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          /// Route Info
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _infoBlock(context, 'From', from),
              Icon(Iconsax.bus, size: 32, color: Ecolors.primary),
              _infoBlock(context, 'To', to, alignEnd: true),
            ],
          ),

          const SizedBox(height: Esizes.md),
          Divider(color: Ecolors.grey.withOpacity(0.4)),

          /// Details
          const SizedBox(height: Esizes.md),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _infoBlock(context, 'Plate No.', plateNumber),
              _infoBlock(context, 'Date', date, alignEnd: true),
            ],
          ),
          const SizedBox(height: Esizes.md),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _infoBlock(context, 'Passengers', '$passengerCount'),
              _infoBlock(context, 'Status', 'Authorized', alignEnd: true),
            ],
          ),

          const SizedBox(height: Esizes.lg),
          Center(
            child: QrImageView(
              data: qrData,
              size: 120,
              backgroundColor: Colors.white,
            ),
          ),
        ],
      ),
    );
  }

  Widget _infoBlock(BuildContext context, String label, String value,
      {bool alignEnd = false}) {
    return Column(
      crossAxisAlignment:
          alignEnd ? CrossAxisAlignment.end : CrossAxisAlignment.start,
      children: [
        Text(label, style: Theme.of(context).textTheme.labelLarge),
        Text(value,
            style: Theme.of(context)
                .textTheme
                .headlineSmall!
                .apply(fontWeightDelta: 2)),
      ],
    );
  }
}
