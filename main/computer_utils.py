def recommended_object_builder(relevant_computer, computer_images,recommendation_info):
    """Build the recommended object"""
    return {
        "id": relevant_computer.id,
        "name": relevant_computer.model,
        "brand": relevant_computer.brand.name,
        "price": float(relevant_computer.price_amount),
        "ram_capacity": relevant_computer.memory.capacity, 
        "ram_speed": relevant_computer.memory.speed,  
        "ram_type": relevant_computer.memory.type,  
        "storage": [
            {
                "type": storage.type,
                "capacity": storage.capacity,
                "rpm": storage.rpm,
            } for storage in relevant_computer.storages.all()
        ],
        "processor": {
            "brand":relevant_computer.processor.brand.name,
            "model":relevant_computer.processor.model,
            "cores":relevant_computer.processor.cores,
            "threads":relevant_computer.processor.threads,
            "base_clock_speed":relevant_computer.processor.base_clock_speed,
            "turbo_clock_speed":relevant_computer.processor.turbo_clock_speed
        },
        "graphic": {
           "type": relevant_computer.graphics.type,
           "memory": relevant_computer.graphics.memory,
           "model": relevant_computer.graphics.model,
           "brand": relevant_computer.graphics.brand.name
        },   
        "images": [
            {
                "src": photo.image.url,
                "alt": f"{relevant_computer.model} - Image {index + 1}"
            } for index, photo in enumerate(computer_images)
        ],
        "image": computer_images.filter(is_cover=True).first().image.url if computer_images.filter(is_cover=True).exists() else '',  # Cover image or first image
        "description": relevant_computer.description,
        "bluetooth": relevant_computer.bluetooth,
        "ethernet": relevant_computer.ethernet,
        "usb3_2_gen2_typeC": relevant_computer.usb3_2_gen2_typeC,
        "usb3_2_gen2_typeA": relevant_computer.usb3_2_gen2_typeA,
        "usb3_2_gen1_typeA": relevant_computer.usb3_2_gen1_typeA,
        "usb2_0": relevant_computer.usb2_0,
        "hdmi_ports": relevant_computer.hdmi_ports,
        "display_ports": relevant_computer.display_ports,
        "audio_front_panel": relevant_computer.audio_front_panel,
        "audio_rear_panel": relevant_computer.audio_rear_panel,
        "height": relevant_computer.height,
        "width": relevant_computer.width,
        "depth": relevant_computer.depth,
        "weight": relevant_computer.weight,
        "warranty_duration": relevant_computer.warranty_duration,
        "warranty_type": relevant_computer.warranty_type,
        "warranty_support": relevant_computer.warranty_support,
        "energy_rating": relevant_computer.energy_rating,
        "extras": relevant_computer.extras,
        "recommendation_reason": recommendation_info.choose_reason if  hasattr(recommendation_info, "choose_reason") else None,
    }
    