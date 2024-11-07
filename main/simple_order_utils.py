"""
    -  Un bon ordinateur doit avoir une carte graphique et un stockage de RAM suffisant
    -  On complete les request de l'utilisateur avec des ordinateurs qui respectent ces bonnes conditions
"""
def graphicForGoodComputer( Computer ,price_min, price_max):
    """
        Check if there is a computer with graphical cards with a
         price between min and max
         :param request:
          price_min: min price
          price_max: max price
          :return: list of computer with graphical  price between min and max if exist else empty list
    """
    cpter = Computer.objects.filter(
        price_amount__range=(price_min, price_max),
        graphics__isnull=False
    )
    if cpter.exists():
        return cpter
    else:
        return []

def ramForGoodComputer(Computer,price_min, price_max, ram = 8):
    """
        Check if there is a computer with ram greate or egal to "ram" and price between min and max
         :param request:
          price_min: min price
          price_max: max price
          ram: ram capacity for good computer
          :return: list of computer with ram price between min and max if exist else empty list
    """
    cpter = Computer.objects.filter(
        price_amount__range=(price_min, price_max),
        memory__capacity__gte=ram)

    if cpter.exists():
        return cpter
    else:
        return []

def storageForGoodComputer(Computer ,price_min, price_max, storage = 512, storage_unit = 'SSD'):
    """
        Check if there is a computer with storage greate or egal to "storage" and price between min and max
         :param request:
          price_min: min price
          price_max: max price
          storage: storage capacity for good computer
          :return: list of computer with storage price between min and max if exist else empty list
    """
    cpter = Computer.objects.filter(
        price_amount__range=(price_min, price_max),
        storages__capacity__gte=storage,
        storages__type=storage_unit
    )
    # print(cpter)
    if cpter.exists():
        return cpter
    else:
        return []

def processorForGoodComputer(Computer,price_min, price_max, processor_core = 4):
    """
        Check if there is a computer with processor greater than "processor_core" and price between min and max
         :param request:
          price_min: min price
          price_max: max price
          processor_core: processor core for good computer
          processor_speed: processor speed for good computer
          :return: list of computer with processor price between min and max if exist else empty list
    """
    cpter = Computer.objects.filter(
        price_amount__range=(price_min, price_max),
        processor__cores__gte=processor_core
    )
    # print(cpter) 
    if cpter.exists():
        return cpter
    else:
        return []


def charateristiqueRelevantComputer(relevant_computers, characteristics):
    """
        Filter the relevant computers with the given characteristics
        :param relevant_computers: list of relevant computers
        :param characteristics: a dictionary with the characteristics of the computer
        :return: the filtered list of computers
    """

    color = characteristics.get('couleur', '')
    os    = characteristics.get('Systeme_exploitation', '')
    processor_speed = characteristics.get('Vitesse_processeur', '')
    # print(processor_speed)
    if len(color)!=0 and len(os)!=0 and len(processor_speed)!=0:
        return relevant_computers.filter(
                color__color = color, 
                operating_system__name = os,
                processor__base_clock_speed = processor_speed
            )
    elif len(color)!=0 and len(os)!=0:
        return relevant_computers.filter(
                color__color = color, 
                operating_system__name = os
            )
    elif len(color)!=0 and len(processor_speed)!=0:
        return relevant_computers.filter(
                color__color = color, 
                processor__base_clock_speed = processor_speed
            )
    elif len(os)!=0 and len(processor_speed)!=0:
        return relevant_computers.filter(
                operating_system__name = os, 
                processor__base_clock_speed = processor_speed
            )
    elif len(color)!=0:
        return relevant_computers.filter(
                color__color = color
            )
    elif len(os)!=0:
        return relevant_computers.filter(
                operating_system__name = os
            )
    elif len(processor_speed)!=0:
        return relevant_computers.filter(
                processor__base_clock_speed = processor_speed
            )
    else:
        return []
    

def mergeSimpleOrderComputer(result_relevant_computers, result_graphical_computers,
                            result_ram_computers, result_storage_computers,
                            result_processor_computers):
    """
        Check there no duplicated computer, then merge the results
        :param result_relevant_computers: list of relevant computers
        :param result_graphical_computers: list of graphical computers
        :param result_ram_computers: list of ram computers
        :param result_storage_computers: list of storage computers
        :param result_processor_computers: list of processor computers
        :return: the merged list of computers
    """
    result = list(result_relevant_computers
                  )+list(result_graphical_computers
                )+ list(result_ram_computers
                ) + list(result_storage_computers
                ) + list(result_processor_computers)
    return list(set(result))

def recommendationPersistance(SimpleOrderRecommendation,result_computers,
                             user_id, user_location, price_min, price_max,graphic,
                             brand, ram, storage, processor_core, processor_speed,
                             os, color):
    """
        Save the recommendation in the database
        :param result_computers: list of computers
        :param SimpleOrderRecommendation: model of recommendation
        :return: None
    """
    import time
    start_time = time.time()
    try:
        for computer in result_computers:
            recommendation = SimpleOrderRecommendation.objects.create(
                computer_id=computer.id,
                user_id=user_id,
                user_location=user_location,
                min_budget=price_min,
                max_budget=price_max,
                graphic=graphic,
                brand=brand,
                ram=ram,
                storage=storage,
                processor_core=processor_core,
                processor_speed=processor_speed,
                os=os,
                color=color,
                recommendation_id=start_time
            )
            recommendation.save()
    except Exception as e:
        print(e)
        return None
    return start_time