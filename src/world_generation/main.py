from .file_gen import generate_world

def main():
    generate_world(
        main_file="gazebo_templates/main.sdf",
        output_path="gazebo_generated/gen.sdf",
        include_map={
            "{objects}": "gazebo_templates/object.sdf",
            "{robot}": "gazebo_templates/robot.sdf",
        },
        replace_map={
            "{x}": str(10),
            "{y}": str(20),
        },
    )

if __name__ == "__main__":
    main()
