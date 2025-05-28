import 'package:quick_trip/utils/constants/sizes.dart';
import 'package:flutter/material.dart';

class EProfileMenu extends StatelessWidget {
  const EProfileMenu({
    super.key,
    required this.title,
    required this.value,
  });
  
  final String title, value;
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      child: Padding(
        padding: const EdgeInsets.all(Esizes.spacebtwItems/1.5),
        child: Row(
          children: [
            Expanded(
                flex: 3,
                child: Text(title,
                    style: Theme.of(context).textTheme.bodySmall,
                    overflow: TextOverflow.ellipsis)),
            Expanded(
                flex: 5,
                child: Text(value,
                    style: Theme.of(context).textTheme.bodyMedium,
                    overflow: TextOverflow.ellipsis)),
            
          ],
        ),
      ),
    );
  }
}
