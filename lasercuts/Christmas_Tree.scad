//Height Settings (for each color assign the extrusion height in mm, this is the height of the model that you will need to swap the plastic over)
print_thickness = 1.5;
plate_thickness = 3;
plate_width = 40;
plate_length = 60;
tree_dist = 7;
bold_dia=2.8;
bold_dia_2 = 2.2;
blind_klink_dia = 4.8;
led_dia=4;
led_size = [5, 5, 2];
$fn=32;

bold_dist = [37, 19.5];
print_size = [2*bold_dist[0] + 6, 2 * bold_dist[1] + 6];

tree_size = [print_size[0], 100];
led_center_x = [-30, -10, 10, 30];
led_center_y = [-2.25, 5.175, 12.675];

mount_center_x = [-37, 37];
mount_center_y = [22.5 - 3, -22.5 + 3];

tb_size = [110, 60];
rb_dia = 5;

// choose one of the following
//mode = "3D";
mode = "2D";
// mode = "plate";


if (mode == "3D")
{
    color("white") 
    for(y = led_center_y)
    { 
        translate([0, y, -20])
        translate([0, 1.5, 0])
            rotate([90, 0, 0])
                linear_extrude(3)
                    plate();    
    }

    color("green")
    print();

    color("aqua", .5)
    translate([0, 0, -21.5])
    linear_extrude(3)
    bottom();

    color("lightblue")
    translate([0, 0, 4.5])
    linear_extrude(3)
    top();

    color("lightgreen")
    translate([0, 0, 1.5])
    linear_extrude(3)
    top1();

    color("lightgray")
    translate([0, 0, 1.5])
        linear_extrude (height=led_size[2])
            leds();

    color("lightgray")
    translate([0, 20, 2.5])
        cube([8, 4, 4], center=true);

    color("pink")
    translate([(8.5 - (tb_size[0]/2)), 0, -8.5])
    rotate([90, 0, 90])
    linear_extrude(3, center=true) side();

    color("pink")
    translate([-(8.5 - (tb_size[0]/2)), 0, -8.5])
    rotate([90, 0, 90])
    linear_extrude(3, center=true) side();

    color("orange")
    translate([0, 26, -8.5])
    rotate([90, 0, 0])
    linear_extrude(3, center=true) front();

    color("orange")
    translate([0, -26, -8.5])
    rotate([90, 0, 0])
    linear_extrude(3, center=true) back();
}
else if (mode == "2D")
{
    color("aqua", .5)
    translate([0, 50])
    bottom();

    color("lightblue")
    translate([0, 112])
    top();

    color("lightgreen")
    translate([0, 174])
    top1();

    color("pink")
    translate([0, 265])
    side();

    color("pink")
    translate([0, 175])
    side();

    color("orange")
    translate([0, 220])
    front();

    color("orange")
    translate([0, 250])
    back();
}
else if (mode == "plate")
{
    color("white") 
        translate([0, -120])
            plate();    
    color("white") 
        translate([101, -120])
            plate();    
    color("white") 
        translate([202, -120])
            plate();    
}


module bottom()
{
    difference()
    {
        top_bottom(blind_klink_dia);
        
        translate([-(tb_size[0]-17)/2, 0])
        square([3.1, 36.1], center=true);

        translate([(tb_size[0]-17)/2, 0])
        square([3.1, 36.1], center=true);
        
        
        translate([30, 26])
            square([20.1, 3.1], center=true);

        translate([-30, 26])
            square([20.1, 3.1], center=true);
        
        
        translate([30, -26])
            square([20.1, 3.1], center=true);

        translate([-30, -26])
            square([20.1, 3.1], center=true);
    }
}

module top()
{
    difference()
    {
        top_bottom(bold_dia);

        for(y = led_center_y)
            translate([0, y])
                square([100.1, 3.1], center=true);

        mount_holes();
        
*        translate([0, 25])
            square([8, 12], center=true);
    }
}



module top1()
{
    difference()
    {
        top_bottom(bold_dia);

        for(y = led_center_y)
            translate([0, y])
                square([100.1, 3.1], center=true);

        difference()
        {
            hull()
            {
                for(x = [-bold_dist[0], bold_dist[0]])
                    for(y = [-bold_dist[1], bold_dist[1]])
                        translate([x, y])
                            circle(d=6);
            }
            for(x = [-bold_dist[0], bold_dist[0]])
                for(y = [-bold_dist[1], bold_dist[1]])
                    translate([x, y])
                        circle(d=7);
        }
    
        translate([-(tb_size[0]-17)/2, 0])
        square([3.1, 36.1], center=true);

        translate([(tb_size[0]-17)/2, 0])
        square([3.1, 36.1], center=true);
        
        translate([30, 26])
            square([20.1, 3.1], center=true);

        translate([-30, 26])
            square([20.1, 3.1], center=true);
                        
        translate([0, 25])
            square([8, 10], center=true);
        
    }
}


module top_bottom(mount_dia)
{
    difference()
    {
        hull()
        {
            translate([ (tb_size[0] - rb_dia) / 2,  (tb_size[1] - rb_dia)/2]) circle(d=rb_dia);
            translate([ (tb_size[0] - rb_dia) / 2, -(tb_size[1] - rb_dia)/2]) circle(d=rb_dia);
            translate([-(tb_size[0] - rb_dia) / 2,  (tb_size[1] - rb_dia)/2]) circle(d=rb_dia);
            translate([-(tb_size[0] - rb_dia) / 2, -(tb_size[1] - rb_dia)/2]) circle(d=rb_dia);
        }
        mount_holes(mount_dia);
    }
}


module front()
{
    difference()
    {
        front_back();
    }
}

module back()
{
    difference()
    {
        front_back();

        translate([0, 10])
        square([90, 20], center=true);
        
        translate([7, 0])
        square([15, 12], center=true); 
    }
}

module front_back()
{
    difference()
    {
        union()
        {
            square([tb_size[0], 20], center=true);

            translate([30, 0])
            square([20, 26], center=true);

            translate([-30, 0])
            square([20, 26], center=true);
        }
        translate([-(tb_size[0]-17)/2, 5])
        square([3.1, 10.1], center=true);
        
        translate([(tb_size[0]-17)/2, 5])
        square([3.1, 10.1], center=true);
    }
}

module side()
{
    difference()
    {
        union()
        {
            square([tb_size[1], 20], center=true);
            square([36, 26], center=true);
        }
        for(y = led_center_y)
        {
            translate([y, 3.5])
                square([3.4, 20], center=true);
        }
        
        translate([(tb_size[1]-8)/2, -5])
        square([3.1, 10.1], center=true);
        
        translate([-(tb_size[1]-8)/2, -5])
        square([3.1, 10.1], center=true);
    }
}

module plate()
{
    difference()
    {
        translate([0, 60])
        square([100, 110], center=true);
        
        translate([0, 13.65])
        square([print_size[0] + 1, 20], center=true);
    }
}


module print()
{
    linear_extrude (height=print_thickness)
        printplate();
}

module printplate()
{
    difference()
    {
        hull()
        {
            for(x = [-bold_dist[0], bold_dist[0]])
                for(y = [-bold_dist[1], bold_dist[1]])
                    translate([x, y])
                        circle(d=6);
        }
        mount_holes(bold_dia);
        for(x = mount_center_x)
        for(y = led_center_y)
        {
            translate([x, y]) circle(d=bold_dia_2);
        }
    }
}

module leds()
{
    for(x = led_center_x)
    for(y = led_center_y)
    {
        translate([x, y]) 
            square([led_size[0], led_size[1]], center=true);
    }
}

module base_plate(is_mountplate=false)
{
    difference()
    {
        square([plate_length, plate_width], center = true);
        
        if(is_mountplate)
        {
            translate([0, tree_dist + plate_thickness/2, 0])
                treemounts(tw1);
            translate([0,  plate_thickness/2, 0])
                treemounts(tw2);
            translate([0, -tree_dist + plate_thickness/2, 0])
                treemounts(tw3);
            
            // leds
            for(x = [-22.5, -7.5, 7.5, 22.5])
                for(y = [-7.5, 0, 7.5])
                    translate([x, y])
                        circle(d=led_dia);
        }
        mount_holes(bold_dia);
    }
}


module mount_holes(mount_dia)
{
    // mount holes
    echo(bold_dist);
    for(x = mount_center_x)
        for(y = mount_center_y)
            translate([x, y])
                circle(d=mount_dia);
}