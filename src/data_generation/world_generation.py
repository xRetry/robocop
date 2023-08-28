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
        for j in range(2):
            mname = "tile_"+str(i)+"_"+str(j)
            pos = str(-9+2*i)+" "+str(j-0.5)+" 0 0 0 0"           
            m1=str(1)
            #m1= str(round(random.random(),2)*50+50)
            m2=str(1)
            if (j==1):
                m2=str(1)
            
            #m2 = str(round(random.random(),2)*0.5)

            if(float(m2)<1):
                color ="0.9 0.1 0"
            else:
                color ="0.1 0.9 0"
            
            replacement = [mname, pos, m1, m2, color]

            current_template = template_string
            for to_repl, repl in zip(to_replace, replacement):
                current_template = current_template.replace(to_repl, repl)

            full_string += current_template
    
    return full_string


def generate_smoke(template_path: str) -> str:
    full_string = ""
    template_string = read_file(template_path)
    
    to_replace =['[[OBJECT]]','[[POSITION]]']   
    
    for i in range (1,3):
        obj_name = "smoker_"+str(i)
    
        if i%2 ==0:
            y = random.uniform(-4,-2.5)
        else:
            y=random.uniform(2.5,4)
        
        x = random.uniform(-8,6)
        
        posx = str(round(x,2))
        posy = str(round(y,2))
        
        position = posx+" "+posy+" 0 0 -0 0"
        replacement =[obj_name,position]

        current_template = template_string
        for to_repl, repl in zip(to_replace, replacement):
            current_template = current_template.replace(to_repl, repl)
            
        full_string += current_template
        
    return full_string
    
def generate_objects(template_path: str) -> str:
    full_string = ""
    template_string = read_file(template_path)
    
    to_replace =['[[OBJECT]]','[[POSITION]]','[[RADIUS]]','[[LENGTH]]','[[COLOR]]']   
      
    color1='1 0 0 1'
    color2 ='0 1 0 1'
    color3 ='0 0 1 1'
    
    # generate 16 objects
    no_obj = 25
    posx = -10
    increment = 20 /no_obj
    for i in range(no_obj):
   
        # replacement for [[OBJECT]]
        obj_name = "cyl_"+str(i)
     
        # replacement for [[POSITION]]
        # first objects set in X direction starting from -3 as robot has 
        # limited side vision
        #posx= str(round(random.uniform(-3,10),2))
        
        posx = posx + increment + random.uniform(-1,1)
        posxx = str(round(posx,2))
   
        if i%2 ==0:
            y = round(random.uniform(-4,-1.5),2)
            posy = str(y)
        else:
            y = round(random.uniform(1.5,4),2)
            posy = str(y)

        # replacement for [[RADIUS]]
        radius = str(round(random.uniform(0.2,0.8),2))

        # replacement for [[LENGTH]]
        length = round(random.uniform(0.2,1.5),2)
        posz = str(round(length/2,2))
        length = str(length)
        
        position = posxx+" "+posy+" "+posz+" 0 -0 0"
        
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
        main_file="gazebo_templates/main_base.sdf",
        output_path="gazebo_generated/generated_world.sdf",
        replace_map={
            "[[STEP_SIZE]]": str(0.1),
            "[[TILES]]": "",
            "[[CYLINDERS]]": generate_objects("gazebo_templates/cylinder_base.sdf"),
            "[[ROBOT]]": read_file("gazebo_templates/robot_stacked_drive.sdf"),
            "[[SMOKE]]": generate_smoke("gazebo_templates/fogemitter.sdf")
        },
# =============================================================================
#         replace_map={
#             "[[STEP_SIZE]]": str(0.1),
#             "[[TILES]]": generate_tiles("gazebo_templates/tile_base_ori.sdf"),
#             "[[CYLINDERS]]": generate_objects("gazebo_templates/cylinder_base.sdf"),
#             "[[ROBOT]]": read_file("gazebo_templates/robot_stacked_drive.sdf")
#         },
# =============================================================================
    )

if __name__ == "__main__":
    main()
