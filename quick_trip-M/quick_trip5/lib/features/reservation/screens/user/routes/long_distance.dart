
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/features/reservation/screens/user/checkout/checkout_long_d.dart';
import 'package:quick_trip/utils/constants/sizes.dart';

class LongDistanceScreen extends StatefulWidget {
  final String from;
  final String to;

  const LongDistanceScreen({super.key, required this.from, required this.to});

  @override
  State<LongDistanceScreen> createState() => _LongDistanceScreenState();
}

class _LongDistanceScreenState extends State<LongDistanceScreen> {
  int? selectedIndex;
  int passengerCount = 1;
  String selectedOption = 'self';
  final TextEditingController _faydaController = TextEditingController();
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  // Dummy bus list
  final List<Map<String, String>> buses = [
    {'level': 'Level 1', 'distance': '245 km', 'seats': '30'},
    {'level': 'Level 1', 'distance': '245 km', 'seats': '40'},
    {'level': 'Level 1', 'distance': '245 km', 'seats': '20'},
    {'level': 'Level 1', 'distance': '245 km', 'seats': '20'},
    {'level': 'Level 1', 'distance': '245 km', 'seats': '20'},
  ];

   void _onPay() {
    if (_formKey.currentState!.validate()) {
      Get.to(() => CheckOutLongDScreen(
        from: widget.from,
        to: widget.to,
        selectedFor: selectedOption,
        faydaNumber: selectedOption == 'other' ? _faydaController.text : null,
        passengerCount: passengerCount,
      ));
    }
  }
  @override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: EappBar(
      showBackArrow: true,
      title: Text('Long Distance', style: Theme.of(context).textTheme.headlineMedium),
    ),
    body: Form(
      key: _formKey,
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(Esizes.defaultSpace),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Selected Route:', style: Theme.of(context).textTheme.headlineSmall),
            Text('${widget.from} → ${widget.to}', style: Theme.of(context).textTheme.bodyLarge),
            const SizedBox(height: 20),

            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ChoiceChip(
                  label: const Text('For Self'),
                  selected: selectedOption == 'self',
                  onSelected: (selected) {
                    setState(() => selectedOption = 'self');
                  },
                ),
                const SizedBox(width: 10),
                ChoiceChip(
                  label: const Text('For Other'),
                  selected: selectedOption == 'other',
                  onSelected: (selected) {
                    setState(() => selectedOption = 'other');
                  },
                ),
              ],
            ),

            if (selectedOption == 'other') ...[
              const SizedBox(height: 16),
              TextFormField(
                controller: _faydaController,
                validator: (value) {
                  if (selectedOption == 'other' && (value == null || value.isEmpty)) {
                    return 'Please enter Fayda number';
                  }
                  return null;
                },
                decoration: const InputDecoration(
                  labelText: 'Enter Fayda Number',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 20),
            ],

            Text('Available Buses:', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 10),

            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: buses.length,
              itemBuilder: (context, index) {
                final bus = buses[index];
                final isSelected = selectedIndex == index;

                return GestureDetector(
                  onTap: () {
                    setState(() {
                      selectedIndex = index;
                    });
                  },
                  child: Card(
                    color: isSelected ? const Color.fromARGB(255, 114, 190, 245) : null,
                    shape: RoundedRectangleBorder(
                      side: BorderSide(color: isSelected ? Colors.blue : Colors.grey.shade300, width: 2),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      title: Text('${widget.from} → ${widget.to}'),
                      subtitle: Padding(
                        padding: const EdgeInsets.only(top: 8.0),
                        child: Text(
                          'Level: ${bus['level']}\nDistance: ${bus['distance']}   Number of Seats: ${bus['seats']}',
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                      ),
                      leading: const Icon(Icons.directions_bus, color: Colors.blue),
                    ),
                  ),
                );
              },
            ),

            const SizedBox(height: 100), // Padding to avoid overlap by button
          ],
        ),
      ),
    ),

    bottomNavigationBar: Padding(
      padding: const EdgeInsets.all(Esizes.defaultSpace),
      child: ElevatedButton(
        onPressed: selectedIndex != null ? _onPay : null,
        child: const Text('Pay'),
      ),
    ),
  );
}

}
