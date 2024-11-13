import svgwrite

# Create a new SVG drawing
dwg = svgwrite.Drawing('plate.svg', profile='tiny', size=("12cm", "4cm"), viewBox="0 0 1200 400")

# Show outline of viewport using 'rect' element
dwg.add(dwg.rect(insert=(1, 1), size=("410mm", "210mm"), fill="none", stroke="blue", stroke_width=2))

# Create a group of lines with green stroke
g = dwg.g(stroke="orange")

# Add lines to the group
g.add(dwg.line(start=("5mm", "5mm"), end=("405mm", "5mm"), stroke_width="1px"))
g.add(dwg.line(start=(300, 300), end=(500, 100), stroke_width="1px"))
g.add(dwg.line(start=(500, 300), end=(700, 100), stroke_width="1px"))
g.add(dwg.line(start=(700, 300), end=(900, 100), stroke_width="1px"))
g.add(dwg.line(start=(900, 300), end=(1100, 100), stroke_width="1px"))

# Add the group to the SVG
dwg.add(g)

# Save the SVG to a file
dwg.save()