import random
from typing import Dict 

def read_file(path: str) -> str:
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

def write_file(path: str, content: str) -> None:
    file = open(path, "w")
    file.write(content)
    file.close()

def generate_world(main_file: str, output_path: str, replace_map: Dict[str, str]) -> None:
    main_content = read_file(main_file)

    for old_str, new_str in replace_map.items():
        main_content = main_content.replace(old_str, new_str)

    write_file(output_path, main_content)

def generate_tiles(template_path: str) -> str:
    full_string = ""
    template_string = read_file(template_path)

    to_replace =["XXXX", "YYYYYY", "MM1", "MM2", "FFF"]   
         
    for i in range(10):
        #range 4 to 6 updates only the middle tiles, which are used in carworld5
        for j in range(4,6):
            mname = "tile_"+str(i-5)+"_"+str(j-5)
            pos = str(-9+2*i)+" "+str(-9+2*j)+" 0 0 0 0"           
            m1=str(1)
            #m1= str(round(random.random(),2)*100)
            m2=str(1)
            #m2 = str(round(random.random(),2)*100)

            if(float(m1)<50):
                color ="0.9 0.1 0"
            else:
                color ="0.1 0.9 0"
            
            replacement = [mname, pos, m1, m2, color]

            current_template = template_string
            for to_repl, repl in zip(to_replace, replacement):
                current_template = current_template.replace(to_repl, repl)

            full_string += current_template
    
    return full_string


def generate_planks(template_path: str) -> str:
    pass

def generate_objects(template_path: str) -> str:
    full_string = ""
    template_string = read_file(template_path)
    
    to_replace =['[[OBJECT]]','[[POSITION]]','[[RADIUS]]','[[LENGTH]]','[[COLOR]]']   
      
    color1='1 0 0 1'
    color2 ='0 1 0 1'
    color3 ='0 0 1 1'
    
    # generate 16 objects
    for i in range(16):
        # replacement for [[OBJECT]]
        obj_name = "cyl_"+str(i)
     
        # replacement for [[POSITION]]
        # first objects set in X direction starting from -3 as robot has 
        # limited side vision
        posx= str(round(random.uniform(-3,10),2))
        posy= (round(random.uniform(-7,7),2))
        while (posy >-2 and posy <2):
            posy= (round(random.uniform(-7,7),2))

        posy = str(posy)
        position = posx+" "+posy+" 0.5 0 -0 0"
        
        # replacement for [[RADIUS]]
        radius = str(round(random.uniform(0.2,1),2))

        # replacement for [[LENGTH]]
        length = str(round(random.uniform(0.2,3),2))

        # replacement for [[COLOR]]
        selector = random.randint(1,3)

        color = color1
        match (selector) :
            case 2:
                color = color2
            case 3:
                color = color3

        replacement =[obj_name,position,radius, length, color]

        current_template = template_string
        for to_repl, repl in zip(to_replace, replacement):
            current_template = current_template.replace(to_repl, repl)
            
        full_string += current_template
       
    return full_string
      

def main():
    generate_world(
        main_file="gazebo_templates/main_base1.sdf",
        output_path="gazebo_generated/generated_world.sdf",
        replace_map={
            "[[TILES]]": generate_tiles("gazebo_templates/tile_base.sdf"),
            "[[CYLINDERS]]": generate_objects("gazebo_templates/cylinder_base.sdf"),
            "[[ROBOT]]": read_file("gazebo_templates/robot_stacked_drive.sdf")
            
        },
    )

if __name__ == "__main__":
    main()
