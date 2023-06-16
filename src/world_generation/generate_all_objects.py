#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 11:26:32 2023

@author: heiko
"""
import random
import os
from pathlib import Path

def read_file(path: str) -> str:
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

def write_file(path: str, content: str) -> None:
    file = open(path, "w")
    file.write(content)
    file.close()


def generate_sfd(main_file: str, output_file: str, to_replace, replacement) -> None:
    main_content = read_file(main_file)
    for i in range(len(to_replace)):
        main_content = main_content.replace(to_replace[i], replacement[i])
    write_file(output_file, main_content)
  
    

    
    
def create_objects():
    
    to_replace =['[[OBJECT]]','[[POSITION]]','[[RADIUS]]','[[LENGTH]]','[[COLOR]]']   
      
    color1='1 0 0 1'
    color2 ='0 1 0 1'
    color3 ='0 0 1 1'
    
    # generate 16 obejects
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


        #print(posx,"  ",posy)
        position = posx+" "+posy+" 0.5 0 -0 0"
        print(position)
        
        # replacement for [[RADIUS]]
        
        radius = str(round(random.uniform(0.2,1),2))
        # replacement for [[LENGTH]]
        length = str(round(random.uniform(0.2,3),2))
        # replacement for [[COLOR]]

        selector = random.randint(1,3)
        match (selector) :
            case 1:
                color = color1
            case 2:
                color = color2
            case 3:
                color = color3

        replacement =[obj_name,position,radius, length, color]
       
        path1 = Path(__file__).parents[2]
      
        main_file = os.path.join(path1, 'generated_world/gazebo_templates/cylinder_base.sdf')
        #print(main_file)
        output_file = os.path.join(path1,"generated_world/gazebo_generated/objects/cylinder_"+str(i)+".sdf")
        #print(output_file)
        generate_sfd(main_file,output_file,to_replace,replacement)

def create_tiles():
    
#   <model name="XXXX"    eg. tiles
#   <pose>YYYYYY</pose>   0 -9.5 0 0 0 0
#   <mu>MM1</mu>          100
#   <mu2>MM2</mu2>        100
#   <ambient>FFF</ambient>   1 0 0
    to_replace =["XXXX","YYYYYY", "MM1", "MM2", "FFF"]   
      
    for i in range(10):
        
        
        #range 4 to 6 updates only the middle tiles, which are used in carworld5
        for j in range(4,6):
            
            mname = "tile_"+str(i-5)+"_"+str(j-5)
            pos = str(-9+2*i)+" "+str(-9+2*j)+" 0 0 0 0"           
            m1= str(round(random.random(),2)*100)
            m2 = str(round(random.random(),2)*100)
            if(float(m1)<50):
                color ="0.9 0.1 0"
            else:
                color ="0.1 0.9 0"
            
            replacement =[mname,pos, m1, m2, color]
       
            path1 = Path(__file__).parents[2]
          
            main_file = os.path.join(path1, 'generated_world/gazebo_templates/tile_base.sdf')
            output_file = os.path.join(path1,"generated_world/gazebo_generated/tiles/tile_"+str(i)+str(j)+".sdf")
            
            generate_sfd(main_file,output_file,to_replace,replacement)
                


def main():
    
    create_objects()
    create_tiles()
    
if __name__ =="__main__" :
    main()
    
        
        
        
        
        