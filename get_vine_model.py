def get_vine_model(name, vine_type, x, y, z, theta):
    '''
    Get the two string sections needed to create an object in a world file

    Parameters:
        name (str): the name of this vine
        vine_type (int): which model to use [1, 2, 3]
        x (float): x coordinate of the vine
        y (float): y coordinate of the vine
        z (float): z coordinate of the vine

    Returns:
        first_part (str): the first string section
        second_part (str): the second string section
    '''
    if vine_type not in [1, 2, 3]:
        raise ValueError('vine_type must be in [1, 2, 3]')

    # 'cloud' is the number in the title of the stl file for each vine
    if vine_type == 1:
        cloud = 3
    elif vine_type == 2:
        cloud = 16
    elif vine_type == 3:
        cloud = 7

    first_part = '''
    <model name='{}'>
        <pose frame=''>{:.5f} {:.5f} {:.5f} 0 0 {:.5f}</pose>
        <scale>1 1 1</scale>
        <link name='link'>
          <pose frame=''>{:.5f} {:.5f} {:.5f} 0 0 {:.5f}</pose>
          <velocity>0 0 0 0 -0 0</velocity>
          <acceleration>0 0 0 0 -0 0</acceleration>
          <wrench>0 0 0 0 -0 0</wrench>
        </link>
    </model>'''.format(name, x, y, z, theta, x, y, z, theta)

    second_part = '''
    <model name='{}'>
      <static>1</static>
      <link name='link'>
        <collision name='collision'>
          <geometry>
            <mesh>
              <uri>model://Vine{}/meshes/mega_cloud{}_processed.stl</uri>
              <scale>1 1 1</scale>
            </mesh>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>100</mu>
                <mu2>50</mu2>
              </ode>
              <torsional>
                <ode/>
              </torsional>
            </friction>
            <contact>
              <ode/>
            </contact>
            <bounce/>
          </surface>
          <max_contacts>10</max_contacts>
        </collision>
        <visual name='visual'>
          <geometry>
            <mesh>
              <uri>model://Vine{}/meshes/mega_cloud{}_processed.stl</uri>
              <scale>1 1 1</scale>
            </mesh>
          </geometry>
          <material>
            <script>
              <uri>file://media/materials/scripts/gazebo.material</uri>
              <name>Gazebo/Wood</name>
            </script>
          </material>
        </visual>
        <self_collide>0</self_collide>
        <enable_wind>0</enable_wind>
        <kinematic>0</kinematic>
      </link>
      <pose frame=''>{:.5f} {:.5f} {:.5f} 0 0 {:.5f}</pose>
    </model>'''.format(name, vine_type, cloud, vine_type, cloud,
                       x, y, z, theta)

    return first_part, second_part
