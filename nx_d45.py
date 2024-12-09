# Import the NXOpen module
import NXOpen

def main():
    # Initialize the NX session
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work

    # Create a list of coordinates for four points
    points_coordinates = [
        (0.0, 0.0, 0.0),  # Point 1
        (100.0, 0.0, 0.0),  # Point 2
        (100.0, 100.0, 0.0),  # Point 3
        (0.0, 100.0, 0.0)   # Point 4
    ]

    # Create points
    points = []
    for coord in points_coordinates:
        point = workPart.Points.CreatePoint(NXOpen.Point3d(coord[0], coord[1], coord[2]))
        points.append(point)
        point.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)

    # Create lines between the points
    lines = []
    for i in range(len(points)):
        start_point = points[i]
        end_point = points[(i + 1) % len(points)]  # Loop back to the first point
        line = workPart.Curves.CreateLine(start_point, end_point)
        line.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)
        lines.append(line)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
