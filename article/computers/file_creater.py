import os 

# the file should be in the path with the model zoodoai
current_file_directory = os.path.dirname(os.path.realpath(__file__))
zoodoai_path = os.path.join(current_file_directory, '..', '..', 'zoodoAI')
zoodoai_path = os.path.abspath(zoodoai_path)

def convertComputerListTotxtFile(computers_data, file_name):  
    file_path = os.path.join(zoodoai_path, file_name)

    with open(file_path, 'w', encoding='utf-8') as file:
        for computer in computers_data:
            # Basic information
            file.write(f"Computer ID: {computer['id']}\n")
            file.write(f"-Brand: {computer['brand']}\n")
            if computer['model']:
                file.write(f"Model: {computer['model']}\n")
            file.write(f"Price: {computer['price']} CFA\n")

            # Processor details
            processor = computer['processor']
            file.write("-Processor:\n")
            file.write(f"  Brand: {processor['brand']}\n")
            file.write(f"  Model: {processor['model']}\n")
            file.write(f"  Cores: {processor['cores']}\n")
            file.write(f"  Threads: {processor['threads']}\n")
            file.write(f"  Base Clock Speed: {processor['baseClockSpeed']}\n")
            file.write(f"  Turbo Clock Speed: {processor['turboClockSpeed']}\n")
            
            # Memory details
            memory = computer['memory']
            file.write("-Memory:\n")
            file.write(f"  Type: {memory['type']}\n")
            file.write(f"  Capacity: {memory['capacity']}\n")
            file.write(f"  Speed: {memory['speed']}\n")
            
            # Storage details
            storage = computer['storage']
            file.write("-Storage:\n")
            file.write(f"  Type: {storage['type']}\n")
            file.write(f"  Capacity: {storage['capacity']}\n")
            
            # Graphics details
            graphics = computer['graphics']
            if graphics is not None:
                file.write("-Graphics:\n")
                file.write(f"  Type: {graphics['type']}\n")
                file.write(f"  Brand: {graphics['brand']}\n")
                file.write(f"  Model: {graphics['model']}\n")
                file.write(f"  Memory: {graphics['memory']}\n")
            
            # Power details
            power = computer['powerSupply']
            if power is not None:
                file.write("-Power supply:\n" if any(power.values()) else "")
                if power['wattage']:
                    file.write(f"  Wattage: {power['wattage']}\n")
            
            # Cooling details
            cooling = computer['cooling']
            if cooling is not None:
                file.write("-Cooling:\n" if any(cooling.values()) else "")
                if cooling['type']:
                    file.write(f"  Type: {cooling['type']}\n")
                if cooling['radiator_size']:
                    file.write(f"  Radiator size: {cooling['radiator_size']}\n")
            
            # Add a blank line between computers
            file.write("\n")

    # Check file created successfully
    if not os.path.exists(file_path):
        return False
    return True

