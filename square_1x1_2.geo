// Gmsh project created on Thu Nov 14 20:17:48 2019
SetFactory("OpenCASCADE");
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {1, 0, 0, 1.0};
//+
Point(3) = {1, 1, 0, 1.0};
//+
Point(4) = {0, 1, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 1};
//+
Curve Loop(1) = {4, 1, 2, 3};
//+
Plane Surface(1) = {1};
//+
Physical Curve("0D") = {1};
//+
Physical Curve("1N") = {2};
//+
Physical Curve("2D") = {3};
//+
Physical Curve("3N") = {4};
//+
Show "*";
//+
Physical Surface("CC", 7) = {1};
