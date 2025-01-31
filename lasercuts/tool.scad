

difference()
{
    union()
    {
        circle(d=13);
        hull()
        {
        translate([0, -6]) circle(d=7);
        translate([0, -25]) circle(d=5.5);
        }
    }
translate([0, 5]) square([5.5, 10], center=true);
intersection()
{
square([5.5, 10], center=true);
rotate(120) square([5.5, 10], center=true);
rotate(240) square([5.5, 10], center=true);
}
}