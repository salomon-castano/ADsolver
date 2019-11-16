//+
SetFactory("OpenCASCADE");
Circle(1) = {0, 0, 0, 1, 0, 2*Pi};
//+
Circle(2) = {0, 0, 0, 2, 0, 2*Pi};
//+
Physical Curve("external_radius", 1) = {2};
//+
Physical Curve("internal_radius", 2) = {1};
//+
Curve Loop(1) = {2};
//+
Curve Loop(2) = {1};
//+
Plane Surface(1) = {1, 2};
//+
Physical Surface("area", 3) = {1};
