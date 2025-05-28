
import 'package:get/get.dart'; 
import 'package:quick_trip/common/widgets/custom_shapes/containers/primary_header_container.dart';
import 'package:quick_trip/features/reservation/screens/user/history/history_list.dart';
import 'package:quick_trip/common/widgets/text/seaction_heading.dart';
import 'package:quick_trip/features/reservation/screens/user/history/history.dart';
import 'package:quick_trip/features/reservation/screens/user/home/widget/home_appbar.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:flutter/material.dart';
import 'package:quick_trip/features/reservation/screens/user/routes/short_distance.dart';
import 'package:quick_trip/features/reservation/screens/user/routes/long_distance.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final PageController _pageController = PageController();
  int _selectedIndex = 0;
  String? _shortFrom, _shortTo, _longFrom, _longTo;
  final List<String> _shortLocations = ['Adama', 'Addis Ababa(Merkato)', 'Mojo', 'Bishoftu'];
  final List<String> _longLocations = ['Addis Ababa(Merkato)', 'Hawasa', 'Dire Dawa','Dambi Dolo', 'Gondar', 'Bahir Dar', 'Mekele'];
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  void _switchTab(int index) {
    setState(() {
      _selectedIndex = index;
    });
    _pageController.animateToPage(index,
        duration: const Duration(milliseconds: 300), curve: Curves.easeInOut);
  }

  void _onSearch() {
  if (_formKey.currentState!.validate()) {
    if (_selectedIndex == 0) {
      Get.to(() => ShortDistanceScreen(
            from: _shortFrom!,
            to: _shortTo!,
          ));
    } else {
      Get.to(() => LongDistanceScreen(
            from: _longFrom!,
            to: _longTo!,
          ));
    }
  }
}

  DateTime? _selectedDate;

Future<void> _pickDate(BuildContext context) async {
  final DateTime? picked = await showDatePicker(
    context: context,
    initialDate: _selectedDate ?? DateTime.now(),
    firstDate: DateTime.now(),
    lastDate: DateTime.now().add(const Duration(days: 365)),
  );
  if (picked != null && picked != _selectedDate) {
    setState(() {
      _selectedDate = picked;
    });
  }
}


@override
Widget build(BuildContext context) {
  return Scaffold(
    body: RefreshIndicator(
      onRefresh: _refreshHome,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: Stack(
          children: [
            Column(
              children: [
                const EprimaryHeaderContainer(
                  height: 300,
                  child: Column(
                    children: [
                      EHomeAppBar(),
                    ],
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(Esizes.spacebtwItems),
                  child: Column(
                    children: [
                      const SizedBox(height: 110),
                      EsectionHeading(
                          title: 'Recent Trip',
                          onPressed: () => Get.to(() => const HistoryScreen())),
                      const HistoryList(),
                    ],
                  ),
                )
              ],
            ),
            Positioned(
              top: 100,
              left: 20,
              right: 20,
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [const Color.fromARGB(255, 83, 117, 151), const Color.fromARGB(255, 121, 156, 185)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.2),
                      blurRadius: 8,
                      spreadRadius: 2,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Form(
                  key: _formKey,
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          _buildToggleButton('Short Distance', 0),
                          const SizedBox(width: 10),
                          _buildToggleButton('Long Distance', 1),
                        ],
                      ),
                      const SizedBox(height: 16),
                      SizedBox(
                        height: 232,
                        child: PageView(
                          controller: _pageController,
                          onPageChanged: (index) {
                            setState(() {
                              _selectedIndex = index;
                            });
                          },
                          children: [
                            _buildSearchCard('Short Distance', _shortFrom, _shortTo, (val) => setState(() => _shortFrom = val), (val) => setState(() => _shortTo = val), _shortLocations),
                            _buildSearchCard('Long Distance', _longFrom, _longTo, (val) => setState(() => _longFrom = val), (val) => setState(() => _longTo = val), _longLocations),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    ),
  );
}

// Function to reload the page
Future<void> _refreshHome() async {
  setState(() {});
}

  Widget _buildToggleButton(String label, int index) {
    return GestureDetector(
      onTap: () => _switchTab(index),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: _selectedIndex == index ? Colors.white : Colors.blue.shade300,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          label,
          style: TextStyle(
            color: _selectedIndex == index ? Colors.blue : Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }




  Widget _buildSearchCard(String label, String? from, String? to, Function(String?) onFromChanged, Function(String?) onToChanged, List<String> locations) {
    return Column(
      children: [
        Row(
          children: [
            Expanded(
            child: DropdownButtonFormField<String>(
              isExpanded: true, // 💥 prevents horizontal overflow
              value: from,
              items: locations.map((loc) {
                return DropdownMenuItem<String>(
                  value: loc,
                  child: Text(
                    loc,
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                );
              }).toList(),
              onChanged: onFromChanged,
              validator: (value) => value == null ? 'Please select a location' : null,
              decoration: InputDecoration(
                labelText: 'From',
                filled: true,
                fillColor: const Color.fromARGB(255, 83, 117, 151),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                contentPadding: const EdgeInsets.symmetric(horizontal: 12), // optional
              ),
            ),
          ),


            const SizedBox(width: 10),
            Expanded(
                child: DropdownButtonFormField<String>(
                  isExpanded: true, // 💥 prevents horizontal overflow
                  value: to,
                  items: locations.map((loc) {
                    return DropdownMenuItem<String>(
                      value: loc,
                      child: Text(
                        loc,
                        overflow: TextOverflow.ellipsis,
                        maxLines: 1,
                      ),
                    );
                  }).toList(),
                  onChanged: onToChanged,
                  validator: (value) => value == null ? 'Please select a location' : null,
                  decoration: InputDecoration(
                    labelText: 'To',
                    filled: true,
                    fillColor: const Color.fromARGB(255, 83, 117, 151),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 12), // optional
                  ),
                ),
              ),


          ],
        ),
    if (label == 'Long Distance') ...[
        const SizedBox(height: 12),
        TextFormField(
          readOnly: true,
          onTap: () => _pickDate(context),
          decoration: InputDecoration(
            labelText: 'Select Date',
            prefixIcon: const Icon(Icons.calendar_today),
            filled: true,
            fillColor: const Color.fromARGB(255, 83, 117, 151),
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
          ),
          controller: TextEditingController(
            text: _selectedDate == null
                ? ''
                : '${_selectedDate!.year}-${_selectedDate!.month.toString().padLeft(2, '0')}-${_selectedDate!.day.toString().padLeft(2, '0')}',
          ),
          validator: (value) {
            if (label == 'Long Distance' && (_selectedDate == null || value!.isEmpty)) {
              return 'Please select a date';
            }
            return null;
          },
        ),
      ],



        const SizedBox(height: 16),
        ElevatedButton(
          onPressed: _onSearch,
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 12),
            backgroundColor: Colors.blue,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          ),
          child: const Center(
            child: Text('Search Routes', style: TextStyle(fontSize: 16, color: Colors.white)),
          ),
        ),


        if (label == 'Short Distance') ...[
      const SizedBox(height: 8),
      const Text(
        '-Short distance trips are within nearby cities or zones.\n-Choose your departure and destination.',
        style: TextStyle(color: Colors.white, fontSize: 14),
        textAlign: TextAlign.start,
      ),
    ],
      ],
    );
  }
}

