import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/features/reservation/screens/user/checkout/checkout_short_d.dart';
import 'package:quick_trip/utils/constants/sizes.dart';

class ShortDistanceScreen extends StatefulWidget {
  final String from;
  final String to;

  const ShortDistanceScreen({
    super.key,
    required this.from,
    required this.to,
  });

  @override
  State<ShortDistanceScreen> createState() => _ShortDistanceScreenState();
}

class _ShortDistanceScreenState extends State<ShortDistanceScreen> {
  int passengerCount = 1;
  String selectedOption = 'self';
  final TextEditingController _faydaController = TextEditingController();
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  // ✅ Persist card selection
  int selectedCardIndex = -1;
  String? selectedLevel;

  void _onPay() {
    if (_formKey.currentState!.validate()) {
      if (selectedCardIndex == -1) {
        Get.snackbar("Route not selected", "Please select a route level before proceeding.",
            snackPosition: SnackPosition.BOTTOM,
            backgroundColor: Colors.red.shade100,
            colorText: Colors.black);
        return;
      }

      Get.to(() => CheckOutScreen(
            from: widget.from,
            to: widget.to,
            selectedFor: selectedOption,
            faydaNumber: selectedOption == 'other' ? _faydaController.text : null,
            passengerCount: passengerCount,
            level: selectedLevel ?? '',
          ));
    }
  }

  @override
  Widget build(BuildContext context) {
    final routes = [
      {
        'route': '${widget.from} → ${widget.to}',
        'distance': '100 km',
        'number of seat': '15',
        'level': 'Level 1',
      },
      {
        'route': '${widget.from} → ${widget.to}',
        'distance': '100 km',
        'number of seat': '20',
        'level': 'Level 2',
      },
      {
        'route': '${widget.from} → ${widget.to}',
        'distance': '100 km',
        'number of seat': '25',
        'level': 'Level 3',
      },
    ];

    return Scaffold(
      appBar: EappBar(
        showBackArrow: true,
        title: Text('Short Distance',
            style: Theme.of(context).textTheme.headlineMedium),
      ),
      body: Padding(
        padding: const EdgeInsets.all(Esizes.defaultSpace),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Selected Route:',
                  style: Theme.of(context).textTheme.headlineSmall),
              Text('${widget.from} → ${widget.to}',
                  style: Theme.of(context).textTheme.bodyLarge),
              const SizedBox(height: 20),

              /// Toggle Buttons
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

              /// Fayda number
              if (selectedOption == 'other') ...[
                const SizedBox(height: 16),
                TextFormField(
                  controller: _faydaController,
                  validator: (value) {
                    if (selectedOption == 'other' &&
                        (value == null || value.isEmpty)) {
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

              Text('Available Routes:',
                  style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 10),

              /// Route Cards
              Expanded(
                child: ListView.builder(
                  itemCount: routes.length,
                  itemBuilder: (context, index) {
                    final route = routes[index];
                    final isSelected = selectedCardIndex == index;

                    return GestureDetector(
                      onTap: () {
                        setState(() {
                          selectedCardIndex = index;
                          selectedLevel = route['level'];
                        });
                      },
                      child: Card(
                        color:
                            isSelected ? const Color.fromARGB(255, 113, 185, 244) : const Color.fromARGB(255, 122, 122, 122),
                        shape: RoundedRectangleBorder(
                          side: BorderSide(
                            color: isSelected
                                ? Colors.blue
                                : Colors.grey.shade300,
                            width: 2,
                          ),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        margin: const EdgeInsets.symmetric(vertical: 8),
                        child: ListTile(
                          title: Text(
                            route['route']!,
                            style: const TextStyle(
                                fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const SizedBox(height: 8),
                              Text('Distance: ${route['distance']}',
                                  style: const TextStyle(fontSize: 14)),
                              const SizedBox(height: 6),
                              Text('Number of seat: ${route['number of seat']}',
                                  style: const TextStyle(fontSize: 14)),
                              const SizedBox(height: 6),
                              Text('Level: ${route['level']}',
                                  style: const TextStyle(
                                      fontSize: 14,
                                      fontWeight: FontWeight.w500)),
                            ],
                          ),
                          leading: const Icon(Icons.directions_bus,
                              color: Colors.blue, size: 32),
                        ),
                      ),
                    );
                  },
                ),
              ),

              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _onPay,
                  child:
                      const Text('Pay', style: TextStyle(fontSize: 18)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}








