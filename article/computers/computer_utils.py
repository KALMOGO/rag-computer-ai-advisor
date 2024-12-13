def get_computer_dict(computer):
    """
    Convert a Computer instance to a dictionary representation.
    """
    return {
        "id": computer.id,
        "brand": computer.brand.name  if hasattr(computer, "brand") and computer.brand.name  is not None else "",
        "model": computer.model if hasattr(computer, "model") and computer.model is not None else "",
        "type": computer.type if hasattr(computer, "type") and computer.type is not None else "",
        "price": float(computer.price_amount) if hasattr(computer, "price_amount") and computer.price_amount is not None else "",
        "is_new": computer.is_new if hasattr(computer, "is_new") and computer.is_new is not None else "",
        "initial_price": float(computer.initial_price) if hasattr(computer, "initial_price") and computer.initial_price is not None else "",
        "is_screen_touch": computer.is_screen_touch if hasattr(computer, "is_screen_touch") and computer.is_screen_touch is not None else "",
        "processor": get_processor_dict(computer.processor),
        "memory": get_memory_dict(computer.memory),
        "storage": [get_storage_dict(storage) for storage in computer.storages.all()][0],
        "connectivity": get_connectivity_dict(computer),
        "ports": get_ports_dict(computer),
        "audio": get_audio_dict(computer),
        "cooling": get_cooling_dict(computer.cooling),
        "powerSupply": get_power_supply_dict(computer.power_supply),
        "graphics": get_graphics_dict(computer.graphics),
        "motherboard": get_motherboard_dict(computer.motherboard),
        "case": get_case_dict(computer.case),
        "extras": computer.extras.split(',') if computer.extras else [],
        "energy_rating": computer.energy_rating if hasattr(computer, "energy_rating") and computer.energy_rating is not None else "",
    }
def get_processor_dict(processor):
    if processor is None:
        return  {
        "brand":  '',
        "model":'',
        "cores": "",
        "threads": "",
        "baseClockSpeed": '',
        "turboClockSpeed":  '',
        "generation": ''
    }
    return {
        "brand": processor.brand.name if hasattr(processor, 'brand') and processor.brand.name is not None else '',
        "model": processor.model if hasattr(processor, 'model') and processor.model is not None else '',
        "cores": processor.cores if hasattr(processor, 'cores') and processor.cores  is not None else 0,
        "threads": processor.threads if hasattr(processor, 'threads') and processor.threads is not None else 0,
        "baseClockSpeed": processor.base_clock_speed if hasattr(processor, 'base_clock_speed') and processor.base_clock_speed is not None else '',
        "turboClockSpeed": processor.turbo_clock_speed if hasattr(processor, 'turbo_clock_speed') and processor.turbo_clock_speed is not None else '',
        "generation": processor.generation if hasattr(processor, 'generation') and processor.generation is not None else ''
    }
def get_memory_dict(memory):
    if memory is None : 
        return {
            "type":"","capacity":"","speed":""
        }
    return {
        "type": memory.type if hasattr(memory, "type") and memory.type  is not None else '',
        "capacity": memory.capacity if hasattr(memory, "capacity") and  memory.capacity is  not None else '',
        "speed": memory.speed if hasattr(memory, "speed") and memory.speed is not None else ''
    }
def get_storage_dict(storage):
    if storage is None:
        return  {
        "type":  '',
        "capacity": '',
        "interface": '',
        "rpm": ''
    }
    return {
        "type": storage.type if hasattr(storage, "type") and storage.type  is not None else '',
        "capacity": storage.capacity if hasattr(storage, "capacity") and storage.capacity is  not None else '',
        "interface": storage.interface if hasattr(storage, "interface") and storage.interface is not None else '',
        "rpm": storage.rpm if hasattr(storage, "rpm") and storage.rpm  is not None else ''
    }
def get_connectivity_dict(computer):
    if computer is None:
        return {
        "wifi":  '',
        "bluetooth":  '',
        "ethernet": ''
    }
    return {
        "wifi": computer.wifi if hasattr(computer, "wifi") and computer.wifi is not None else '',
        "bluetooth": computer.bluetooth if hasattr(computer, "bluetooth") and computer.ethernet is not None else '',
        "ethernet": computer.ethernet if hasattr(computer, "ethernet") and computer.ethernet is not None else ''
    }
def get_ports_dict(computer):
    if computer is None:
        return  {
        "usb3_2_gen2_typeC":  '',
        "usb3_2_gen2_typeA": '',
        "usb3_2_gen1_typeA": '',
        "usb2_0":  '',
        "hdmi_ports":  '',
        "display_ports": ''
    }
    return {
        "usb3_2_gen2_typeC": computer.usb3_2_gen2_typeC if hasattr(computer, "usb3_2_gen2_typeC") and computer.usb3_2_gen2_typeC  is  not None else '',
        "usb3_2_gen2_typeA": computer.usb3_2_gen2_typeA if hasattr(computer, "usb3_2_gen2_typeA") and computer.usb3_2_gen2_typeA is  not None else '',
        "usb3_2_gen1_typeA": computer.usb3_2_gen1_typeA if hasattr(computer, "usb3_2_gen1_typeA") and computer.usb3_2_gen1_typeA  is not None else '',
        "usb2_0": computer.usb2_0 if hasattr(computer, "usb2_0") and computer.usb2_0 is not None else '',
        "hdmi_ports": computer.hdmi_ports if hasattr(computer, "hdmi_ports") and computer.hdmi_ports   is not None else '',
        "display_ports": computer.display_ports if hasattr(computer, "display_ports") and computer.display_ports  is not None else ''
    }
def get_audio_dict(computer):
    if computer is None:
        return {
        "front_panel":  '',
        "rear_panel": ''
        }
    return {
        "front_panel": computer.audio_front_panel if hasattr(computer, "audio_front_panel") and computer.audio_front_panel is not None else '',
        "rear_panel": computer.audio_rear_panel if  hasattr(computer, "audio_rear_panel")  and computer.audio_rear_panel is not None else ''
    }
def get_cooling_dict(cooling):
    if cooling is None:
        return{
        "type": '',
        "radiator_size": ''
    }
    return {
        "type": cooling.type if hasattr(cooling, "type") and cooling.type is not None else '',
        "radiator_size": cooling.radiator_size if hasattr(cooling, "radiator_size") and cooling.radiator_size  is not None else ''
    }
def get_power_supply_dict(power_supply):
    if power_supply is None:
        return {
        "wattage":  '',
        "efficiency":  ''
    }
    return {
        "wattage": power_supply.wattage if hasattr(power_supply, "wattage") and power_supply.wattage  is not None else '',
        "efficiency": power_supply.efficiency if hasattr(power_supply, "efficiency") and power_supply.efficiency is not None else '',
    }
def get_graphics_dict(graphics):
    if graphics is None:
        return {
        "type":'',
        "brand": '',
        "model": '',
        "memory": '',
    }
    return {
        "type":graphics.type if hasattr(graphics, "type") and graphics.type is not None else '',
        "brand": graphics.brand.name if hasattr(graphics, "brand") and graphics.brand.name is not None else '',
        "model": graphics.model if hasattr(graphics, "model") and graphics.model is not None else '',
        "memory": graphics.memory if hasattr(graphics, "memory") and graphics.memory is not None else '',
    }
def get_motherboard_dict(motherboard):
    if motherboard is None:
        return {
        "brand":  '',
        "model":  '',
        "chipset":'',
    }
    return {
        "brand": motherboard.brand.name if hasattr(motherboard.brand, "name") and motherboard.brand.name is not None else '',
        "model": motherboard.model if hasattr(motherboard, "model") and motherboard.model is not None else '',
        "chipset": motherboard.chipset if hasattr(motherboard, "chipset") and motherboard.chipset is not None else '',
    }
def get_case_dict(case):
    if case is None:
        return  {
        "brand":  '',
        "model": '',
        "form_factor": '',
    }
    return {
        "brand": case.brand if hasattr(case, 'brand') and case.brand is not None else '',
        "model": case.model if hasattr(case, 'model') and case.model is not None else '',
        "form_factor": case.form_factor if hasattr(case, 'form_factor') and case.form_factor is not None else '',
    }
# Select the foreign and the manyTomany fields data
def get_optimized_computers_queryset(queryset):
    """
    Optimize the queryset with select_related and prefetch_related.
    """
    return queryset.select_related(
        'brand', 'processor', 'memory', 'graphics', 'motherboard', 'power_supply', 
        'cooling', 'case', 'operating_system'
    ).prefetch_related('storages')
# Used in the view
def get_computers_data(relevant_computers):
    """
    Convert a queryset of Computer objects to a list of dictionaries.
    """
    optimized_queryset = get_optimized_computers_queryset(relevant_computers)
    return [get_computer_dict(computer) for computer in optimized_queryset]


###########################################
import requests
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_location_by_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        location = {
            'ip': ip,
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country'),
            'location': data.get('loc'),  # lat, long
        }
        return location
    except Exception as e:
        return {"error": str(e)}


def delete_file(path):
    import os
    if os.path.exists(path):
        os.remove(path)
        return True
    return False