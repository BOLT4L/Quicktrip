import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:iconsax/iconsax.dart';
import 'package:quick_trip/common/widgets/custom_shapes/containers/primary_header_container_driver.dart';
import 'package:quick_trip/common/widgets/text/seaction_heading.dart';
import 'package:quick_trip/features/reservation/screens/driver/History/history_list_driver.dart';
import 'package:quick_trip/features/reservation/screens/driver/history/history.dart';
import 'package:quick_trip/features/reservation/screens/driver/home/widget/home_appbar.dart';
import 'package:quick_trip/utils/constants/sizes.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String? driverGreeting;
  bool isLoading = true;
  List<dynamic> recentTrips = [];
  bool isHistoryLoading = true;

  @override
  void initState() {
    super.initState();
    _loadDriverInfo();
    _loadHistory();
  }

  Future<void> _loadDriverInfo() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final phone = prefs.getString('loginIdentifier');
      final token = prefs.getString('accessToken');
       
      if (phone != null && token != null) {
        final response = await http.get(       
          Uri.parse('http://127.0.0.1:8000/api/getUser/$phone'),
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json',
          },               
        );

        if (response.statusCode == 200) {   
          final List data = jsonDecode(response.body);
          if (data.isNotEmpty) {
            final user = data[0];
            setState(() {
              driverGreeting = 'Hello, ${user['employee']['Fname']}';
              isLoading = false;
            });  
          }
        } else {
          debugPrint('Failed to fetch driver info: ${response.statusCode}');
          setState(() => isLoading = false);
        }
      }
    } catch (e) {
      debugPrint('Error: $e');
      setState(() => isLoading = false);
    }
  }

  Future<void> _loadHistory() async {
    try {
      setState(() => isHistoryLoading = true);
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('accessToken');

      if (token == null) {  
        debugPrint('No access token found');
        setState(() => isHistoryLoading = false);
        return;
      }
      debugPrint('Making request to history endpoint...');
      final response = await http.get(
        Uri.parse('http://127.0.0.1:8000/api/recent/'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      ).timeout(const Duration(seconds: 10));

      debugPrint('Response status: ${response.statusCode}');
      debugPrint('Response body: ${response.body}');

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        setState(() {
          recentTrips = data;
          isHistoryLoading = false;
        });
      } else {
        debugPrint('Failed to load history: ${response.statusCode}');
        setState(() => isHistoryLoading = false);
        throw Exception('Failed to load history: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('Error loading history: $e');
      setState(() => isHistoryLoading = false);
      // You might want to show an error message to the user here
      Get.snackbar(
        'Error',
        'Failed to load trip history: ${e.toString()}',
        snackPosition: SnackPosition.BOTTOM,
      );
    }
  }

  Future<void> _refreshDriverHome() async {
    setState(() {
      isHistoryLoading = true;
    });
    await Future.wait([
      _loadDriverInfo(),
      _loadHistory(),
    ]);
  }

  Widget buildTripCard(Map<String, dynamic> trip, BuildContext context) {
    final ticket = trip['ticket'] ?? {};
    final route = ticket['route'] ?? {};
    final vehicle = trip['vehicle'] ?? {};
    final vehicleUser = vehicle['user'] ?? {};
    final driver = vehicleUser['employee'] ?? {};
    final payment = trip['payment'] ?? {};
    final paymentUser = payment['user'] ?? {};
    final paymentEmployee = paymentUser['employee'] ?? {};

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  route['name'] ?? 'No route',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                Chip(
                  label: Text(
                    'ETB ${payment['amount'] ?? '-'}',
                    style: const TextStyle(color: Colors.white),
                  ),
                  backgroundColor: Colors.green,
                ),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                const Icon(Icons.person, size: 16),
                const SizedBox(width: 4),
                Text(
                  'Driver: ${driver['Fname'] ?? paymentEmployee['Fname'] ?? ''} ${driver['Lname'] ?? paymentEmployee['Lname'] ?? ''}',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ],
            ),
            const SizedBox(height: 4),
            Row(
              children: [
                const Icon(Icons.directions_bus, size: 16),
                const SizedBox(width: 4),
                Text(
                  'Plate: ${vehicle['plate_number'] ?? '-'}',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ],
            ),
            const SizedBox(height: 4),
            Row(
              children: [
                const Icon(Icons.calendar_today, size: 16),
                const SizedBox(width: 4),
                Text(
                  'Date: ${ticket['takeoff_date'] ?? '-'}',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ],
            ),
            const SizedBox(height: 4),
            Row(
              children: [
                const Icon(Icons.access_time, size: 16),
                const SizedBox(width: 4),
                Text(
                  'Time: ${ticket['takeoff_time'] ?? '-'}',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ],
            ),
            const SizedBox(height: 8),
            const Divider(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Status: ${payment['status'] == 'c' ? 'Completed' : 'Pending'}',
                  style: TextStyle(
                    color:
                        payment['status'] == 'c' ? Colors.green : Colors.orange,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  'Transaction: ${payment['transaction_id'] ?? '-'}',
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: RefreshIndicator(
        onRefresh: _refreshDriverHome,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            children: [
              // Header
              EprimaryHeaderContainer(
                height: 300,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const EHomeAppBar(),
                    const SizedBox(height: 5),

                    // Greeting Message
                    Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: Esizes.spacebtwItems),
                      child: Text(
                        isLoading
                            ? 'Loading...'
                            : (driverGreeting ?? 'Hello, Driver'),
                        style:
                            Theme.of(context).textTheme.headlineSmall?.copyWith(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.white,
                                ),
                      ),
                    ),

                    const SizedBox(height: 12),

                    // Assigned Trip Info
                    Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: Esizes.spacebtwItems),
                      child: SizedBox(
                        height: 160,
                        child: Card(
                          shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(16)),
                          elevation: 10,
                          color: const Color.fromARGB(255, 209, 160, 124)
                              .withOpacity(0.9),
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Row(
                              children: [
                                const Icon(Iconsax.bus,
                                    size: 40, color: Colors.blue),
                                const SizedBox(width: 16),
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    const SizedBox(height: 4),
                                    Text('Assigned Destination',
                                        style: Theme.of(context)
                                            .textTheme
                                            .titleMedium!
                                            .copyWith(
                                                fontWeight: FontWeight.bold)),
                                    const SizedBox(height: 4),
                                    Text.rich(
                                      TextSpan(
                                        children: [
                                          const TextSpan(text: 'Adama '),
                                          WidgetSpan(
                                            alignment:
                                                PlaceholderAlignment.middle,
                                            child: Icon(Icons.swap_horiz,
                                                size: 20,
                                                color: Colors.black54),
                                          ),
                                          const TextSpan(text: ' Addis Ababa'),
                                        ],
                                      ),
                                      style: Theme.of(context)
                                          .textTheme
                                          .bodyMedium,
                                    ),
                                    const SizedBox(height: 12),
                                    Text('Queue Number: ',
                                        style: Theme.of(context)
                                            .textTheme
                                            .titleSmall!
                                            .copyWith(
                                                fontWeight: FontWeight.w600)),
                                    Text('9',
                                        style: Theme.of(context)
                                            .textTheme
                                            .titleLarge!
                                            .copyWith(color: Colors.redAccent)),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              // Body
              // In the body section of your HomeScreen, replace the history list part with:
              Padding(
                padding: const EdgeInsets.all(Esizes.defaultSpace),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    EsectionHeading(
                      title: 'Recent Trip',
                      onPressed: () => Get.to(() => const HistoryScreen()),
                    ),
                    const SizedBox(height: Esizes.spacebtwItems),
                    isHistoryLoading
                        ? const Center(child: CircularProgressIndicator())
                        : recentTrips.isEmpty
                            ? const Text('No recent trips available.')
                            : Column(
                                children: recentTrips
                                    .map((trip) => buildTripCard(trip, context))
                                    .toList(),
                              ),
                  ],
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
