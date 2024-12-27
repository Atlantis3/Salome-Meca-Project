import math

def rotate_point(x, y, angle, center_x, center_y):
    """
    Rotate a point (x, y) around a center (center_x, center_y) by a given angle in degrees.
    
    Args:
    - x, y: Coordinates of the point to rotate
    - angle: The angle in degrees
    - center_x, center_y: Coordinates of the center of rotation
    
    Returns:
    - (new_x, new_y): The rotated coordinates
    """
    angle_rad = math.radians(angle)
    
    # Translate point back to origin
    translated_x = x - center_x
    translated_y = y - center_y
    
    # Rotate point
    rotated_x = translated_x * math.cos(angle_rad) - translated_y * math.sin(angle_rad)
    rotated_y = translated_x * math.sin(angle_rad) + translated_y * math.cos(angle_rad)
    
    # Translate point back
    new_x = rotated_x + center_x
    new_y = rotated_y + center_y
    
    return new_x, new_y

def rotate_dataframe(df, angle, center_x, center_y):
    """
    Rotate all points in a DataFrame around a fixed center by a given angle.
    
    Args:
    - df: A pandas DataFrame with columns 'x_coordinates' and 'y_coordinates'
    - angle: The angle in degrees
    - center_x, center_y: Coordinates of the center of rotation
    
    Returns:
    - A new DataFrame with rotated coordinates
    """
    rotated_data = df.apply(
        lambda row: rotate_point(row['x_cordinates'], row['y_cordinates'], angle, center_x, center_y), 
        axis=1
    )
    
    # Unpack the rotated data into new columns
    df['x_rotated'], df['y_rotated'] = zip(*rotated_data)
    return df

    
