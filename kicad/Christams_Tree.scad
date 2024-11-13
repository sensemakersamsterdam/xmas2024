//Height Settings (for each color assign the extrusion height in mm, this is the height of the model that you will need to swap the plastic over)
print_thickness = 1.5;
plate_thickness = 3;
plate_width = 40;
plate_length = 60;
tree_dist = 7;
bold_dia=2.5;
led_dia=4;
$fn=32;

bold_dist = [27, 17];

//Tree Measurements  
//Tree Height (not the extruded height) 
    th1 = 50; 
    th2 = 40;
    th3 = 30;
    th4 = 20;
//Tree Width 
    tw1 = 50;
    tw2 = 35;
    tw3 = 20;
    tw4 = 5;
//Tree Points (not adjustable yet, so please leave it at 3, but in future plans)
    tp = 3;

translate([0, 0, -10])
    linear_extrude (height=plate_thickness)
        base_plate(true);

translate([0, 0, -30])
    linear_extrude (height=plate_thickness)
        base_plate(false);


translate([0, 0, -20])
    linear_extrude (height=print_thickness)
        print();

translate([0, tree_dist + plate_thickness/2, 0])
    rotate([90, 0, 0])
        linear_extrude (height=plate_thickness)
            tree1();

translate([0, plate_thickness/2, 0])
    rotate([90, 0, 0])
        linear_extrude (height=plate_thickness)
            tree2();

translate([0, -tree_dist + plate_thickness/2 , 0])
    rotate([90, 0, 0])
        linear_extrude (height=plate_thickness)
            tree3();

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
        mount_holes();
    }
}

module tree1()
{
    union()
    {
        difference()
        {
            tree(th1, tw1, tp);
            tree(th2, tw2, tp);
        }
        treemounts(tw1);
    }
}

module tree2()
{
    union()
    {
        difference()
        {
            tree(th2, tw2, tp);
            tree(th3, tw3, tp);
        }
        treemounts(tw2);
    }
}

module tree3()
{
    union()
    {
        difference()
        {
            tree(th3, tw3, tp);
            tree(th4, tw4, tp);
        }
        treemounts(tw3);
    }
}

module treemounts(tw)
{
    translate([((tw/2) - (plate_thickness*2)), -plate_thickness/2])
        square([plate_thickness, plate_thickness], center = true);
    translate([-((tw/2) - (plate_thickness*2)), -plate_thickness/2])
        square([plate_thickness, plate_thickness], center = true);
}
module tree(th, tw, tp)
{
    tw2 = tw/2;

        // Tree calculations
    pw = tw/(2*(tp+1));
    ph = th/(tp);
    ht = tw/2;
   
  // Draw Tree (height 1)
    polygon (points = 
        [[-tw2, 0], 
        [tw2, 0], 
        [tw2 - (2 * pw), ph], 
        [tw2 - pw, ph], 
        [tw2 - (3*pw), 2*ph], 
        [tw2 - (2*pw), 2*ph], 
        [tw2 - (4*pw), 3*ph], 
        [-tw2 + 2 * pw, 2*ph], 
        [-tw2 + 3 * pw, 2*ph], 
        [-tw2 + pw, ph], 
        [-tw2 + 2 * pw, ph]
        ]);
}

module print()
{
    difference()
    {
        union()
        {
            square([60 - 2 * 3.45, 40], center=true);
            hull()
            {
                translate([ -27, 17]) circle(d=6);
                translate([  27, 17]) circle(d=6);
            }
            hull()
            {
                translate([ -27, -17]) circle(d=6);
                translate([  27, -17]) circle(d=6);
            }
        }
        mount_holes();
    }
}

module mount_holes()
{
    // mount holes
    // [-9, -21.5] -> [9, 21.5]
    echo(bold_dist);
    for(x = [-bold_dist[0], bold_dist[0]])
        for(y = [-bold_dist[1], bold_dist[1]])
            translate([x, y])
                circle(d=bold_dia);
}
