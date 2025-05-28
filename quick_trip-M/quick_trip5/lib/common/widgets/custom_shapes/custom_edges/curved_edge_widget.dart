import 'package:quick_trip/common/widgets/custom_shapes/custom_edges/curved_edges.dart';
import 'package:flutter/material.dart';

class EcurvededgeWidget extends StatelessWidget {
  const EcurvededgeWidget({
    super.key,
    required this.child,
  });

  final Widget child;
  @override
  Widget build(BuildContext context) {
    return ClipPath(
      clipper: EcustomcurvedEdges(),
      child: child,
    );
  }
}
