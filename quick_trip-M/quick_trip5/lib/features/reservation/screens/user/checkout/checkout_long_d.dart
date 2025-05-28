import 'package:quick_trip/common/widgets/appbar/appbar.dart';
import 'package:quick_trip/common/widgets/custom_shapes/containers/rounded_container.dart';
import 'package:quick_trip/common/widgets/success_screen/success_screen.dart';
import 'package:quick_trip/common/widgets/text/seaction_heading.dart';
import 'package:quick_trip/navigation_menu_user.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:quick_trip/utils/constants/image_strings.dart';
import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:quick_trip/utils/helpers/helper_function.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class CheckOutLongDScreen extends StatelessWidget {

  final String from;
  final String to;
  final String selectedFor;
  final String? faydaNumber;
  final int passengerCount;

  const CheckOutLongDScreen({
    super.key,
    required this.from,
    required this.to,
    required this.selectedFor,
    this.faydaNumber,
    required this.passengerCount,
  });

  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);
    return Scaffold(
      appBar: EappBar(
        showBackArrow: true,
        title: Text('Payment Details', style: Theme.of(context).textTheme.headlineSmall),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(Esizes.defaultSpace),
          child: Column(
            children: [
              // Billing Container
              EroundedContainer(
                showBorder: true,
                padding: const EdgeInsets.all(Esizes.md),
                backgroundcolor: dark ? Ecolors.black : Ecolors.lightGrey,
                child: EBillingAmountSection(
                  from: from,
                  to: to,
                  selectedFor: selectedFor,
                  faydaNumber: faydaNumber,
                  passengerCount: passengerCount,
                ),
              ),
              const SizedBox(height: Esizes.spacebtwSections),

              // Payment Method
              EroundedContainer(
                showBorder: true,
                padding: const EdgeInsets.all(Esizes.md),
                backgroundcolor: dark ? Ecolors.black : Ecolors.lightGrey,
                child: const EBillingPaymentSection(),
              )
            ],
          ),
        ),
      ),

      // Checkout button
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(5),
        child: ElevatedButton(
          onPressed: () => Get.to(() => SuccessScreen(
            image: Eimages.successVerification,
            title: 'Payment Success!',
            subtitle: 'Have a good trip!',
            onPressed: () => Get.offAll(() => const NavigationMenu()),
          )),
          child: const Text('Pay'),
        ),
      ),
    );
  }
}

class EBillingAmountSection extends StatelessWidget {
  final String from;
  final String to;
  final String selectedFor;
  final String? faydaNumber;
  final int passengerCount;

  const EBillingAmountSection({
    super.key,
    required this.from,
    required this.to,
    required this.selectedFor,
    this.faydaNumber,
    required this.passengerCount,
  });

  @override
  Widget build(BuildContext context) {
    const seatPrice = 200;
    const serviceFee = 8;
    const taxFee = 12;
    final subtotal = seatPrice * passengerCount;
    final total = subtotal + serviceFee + taxFee;

    return Column(
      children: [
        _row('Route', '$from → $to'),
        _row('Passenger Type', selectedFor == 'self' ? 'For Self' : 'For Other'),
        if (selectedFor == 'other')
          _row('Fayda Number', faydaNumber ?? '-'),
        _row('Number of Passenger', '$passengerCount'),
        _row('Distance', '100 km'),
        _row('Level', '1'),
        _row('Subtotal', '$subtotal birr'),
        _row('Service Fee', '$serviceFee birr'),
        _row('Tax Fee', '$taxFee birr'),
        _row('Total', '$total birr', isBold: true),
      ],
    );
  }

 Widget _row(String label, String value, {bool isBold = false}) {
  return Padding(
    padding: const EdgeInsets.only(bottom: Esizes.spacebtwItems / 2),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start, // handles multi-line better
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          flex: 4,
          child: Text(label, style: Get.textTheme.bodyMedium),
        ),
        const SizedBox(width: 8),
        Expanded(
          flex: 6,
          child: Text(
            value,
            textAlign: TextAlign.right,
            overflow: TextOverflow.ellipsis,
            maxLines: 2, // allows small wrapping if needed
            style: isBold
                ? Get.textTheme.titleMedium
                : Get.textTheme.bodyMedium,
          ),
        ),
      ],
    ),
  );
}

}

class EBillingPaymentSection extends StatelessWidget {
  const EBillingPaymentSection({super.key});

  @override
  Widget build(BuildContext context) {
    final dark = EHelperFunctions.isDarkMode(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        EsectionHeading(
          title: 'Payment Method',
          buttonTitle: 'Change',
          onPressed: () {},
        ),
        const SizedBox(height: Esizes.spacebtwItems / 2),
        Row(
          children: [
            EroundedContainer(
              width: 70,
              height: 55,
              backgroundcolor: dark ? Ecolors.white : Ecolors.light,
              padding: const EdgeInsets.all(Esizes.sm),
              child: const Image(
                image: AssetImage(Eimages.chapa),
                fit: BoxFit.contain,
              ),
            ),
            const SizedBox(width: Esizes.spacebtwItems / 2),
            Text('Chapa', style: Theme.of(context).textTheme.bodyLarge),
          ],
        )
      ],
    );
  }
}





