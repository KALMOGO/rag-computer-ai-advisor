def recommended_object_builder(relevant_computer, computer_images,recommendation_info):
    """Build the recommended object"""
    return {
        "id": relevant_computer.id,
        "name": relevant_computer.model,
        "brand": relevant_computer.brand.name if hasattr(relevant_computer, 'brand') else '',
        "price": float(relevant_computer.price_amount),
        "ram_capacity": relevant_computer.memory.capacity if hasattr(relevant_computer.memory, 'capacity') else '',
        "ram_speed": relevant_computer.memory.speed if hasattr(relevant_computer.memory, 'speed') else '',
        "ram_type": relevant_computer.memory.type if hasattr(relevant_computer.memory, 'type') else '',
        "is_new": relevant_computer.is_new,
        "initial_price": float(relevant_computer.initial_price),
        "is_screen_touch": relevant_computer.is_screen_touch if hasattr(relevant_computer, "is_screen_touch") and relevant_computer.is_screen_touch is not None else "",
        "storage": [
            {
                "type": storage.type if hasattr(storage, 'type') else '',
                "capacity": storage.capacity if hasattr(storage, 'capacity') else '',
                "rpm": storage.rpm if hasattr(storage, 'rpm') else '',
            } for storage in relevant_computer.storages.all()
        ],
        "processor": {
            "brand":relevant_computer.processor.brand.name if hasattr(relevant_computer.processor, 'brand') else '',
            "model":relevant_computer.processor.model if hasattr(relevant_computer.processor, 'model') else '',
            "cores":relevant_computer.processor.cores if hasattr(relevant_computer.processor, 'cores') else '',
            "threads":relevant_computer.processor.threads if hasattr(relevant_computer.processor, 'threads') else '',
            "base_clock_speed":relevant_computer.processor.base_clock_speed if hasattr(relevant_computer.processor, 'base_clock_speed') else '',
            "turbo_clock_speed":relevant_computer.processor.turbo_clock_speed if hasattr(relevant_computer.processor, 'turbo_clock_speed') else '',
            "generation":relevant_computer.processor.generation if hasattr(relevant_computer.processor, 'generation') else '',
        },
        "graphic": {
           "type": relevant_computer.graphics.type if hasattr(relevant_computer.graphics, 'type') else '',
           "memory": relevant_computer.graphics.memory if hasattr(relevant_computer.graphics, 'memory') else '',
           "model": relevant_computer.graphics.model    if hasattr(relevant_computer.graphics, 'model') else '',
           "brand": relevant_computer.graphics.brand.name if hasattr(relevant_computer.graphics, 'brand') else '',
        },   
        "images": [
            {
                "src": photo.image.url if photo.image else '',
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
        "os_name": relevant_computer.operating_system.name if hasattr(relevant_computer.operating_system, "name") else None,
        "os_version": relevant_computer.operating_system.version if hasattr(relevant_computer.operating_system, "version") else None,
        "os_bitness": relevant_computer.operating_system.bitness if hasattr(relevant_computer.operating_system, "bitness") else None,
        "screen_size": relevant_computer.screen_size,
        "color": relevant_computer.color,
        "cooling_type": relevant_computer.cooling.type if hasattr(relevant_computer.cooling, "type") else None,
        "cooling_radiatorSize": relevant_computer.cooling.radiatorSize if hasattr(relevant_computer.cooling, "radiatorSize") else None,
        "power_supply_wattage": relevant_computer.power_supply.wattage if hasattr(relevant_computer.power_supply, "wattage") else None,
        "power_supply_efficiency": relevant_computer.power_supply.efficiency if hasattr(relevant_computer.power_supply, "efficiency") else None,
        "case": relevant_computer.case.form_factor if hasattr(relevant_computer.case, "form_factor") else None,
        "keyboard_is_backlit": relevant_computer.keyboard.is_backlit if hasattr(relevant_computer.keyboard, "is_backlit") else None,
        "keyboard_as_numeric_panel": relevant_computer.keyboard.as_numeric_panel if hasattr(relevant_computer.keyboard, "as_numeric_panel") else None,
        "keyboard_as_finger_print": relevant_computer.keyboard.as_finger_print if hasattr(relevant_computer.keyboard, "as_finger_print") else None,
        "keyboard_type": relevant_computer.keyboard.type if hasattr(relevant_computer.keyboard, "type") else None,
        "recommendation_reason": recommendation_info.choose_reason if  hasattr(recommendation_info, "choose_reason") else None,
        }
    