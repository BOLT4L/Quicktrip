import 'package:quick_trip/common/widgets/custom_shapes/containers/circular_container.dart';
import 'package:quick_trip/common/widgets/custom_shapes/custom_edges/curved_edge_widget.dart';
import 'package:quick_trip/utils/constants/colors.dart';
import 'package:flutter/material.dart';

class EprimaryHeaderContainer extends StatelessWidget {
  const EprimaryHeaderContainer({
    super.key,
    required this.child,
    required this.height,
  });

  final Widget child;
  final double? height;
  @override
  Widget build(BuildContext context) {
    return EcurvededgeWidget(
      child: Container(
        color: Ecolors.primary,
        padding: const EdgeInsets.all(0),
        child: SizedBox(
          height: height,
          child: Stack(
            children: [
              Positioned(
                  top: 0,
                  right: 0,
                  child: EcircularContainer(
                      backgroundcolor: Ecolors.textWhite.withOpacity(0.1))),
              Positioned(
                  top: 100,
                  right: -300,
                  child: EcircularContainer(
                      backgroundcolor: Ecolors.textWhite.withOpacity(0.1))),
              child,
            ],
          ),
        ),
      ),
    );
  }
}
