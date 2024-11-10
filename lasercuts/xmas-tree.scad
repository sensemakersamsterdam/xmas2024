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

