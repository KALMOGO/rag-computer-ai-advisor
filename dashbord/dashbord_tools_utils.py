from datetime import datetime, timedelta

def get_orders_data(order):
    return {
            "client_name": f'{order.last_name} {order.first_name}',
            "creation_date": order.creation_date.strftime("%Y-%m-%d"),
            "phone": order.phone,
            "location": order.location,
            "number": order.number,
            "computer": order.computer.pk +"/" + order.computer.brand.name,  #+"/" + order.computer.model  ,
            "computer_info": order.computer.pk +"/" + order.computer.brand.name +"/" + 
              order.computer.model + "/" + "core i "+ f"{order.computer.processor.cores-1}" + "/" + 
                "RAM:" +order.computer.memory.capacity + "GB /" + "disque: " + order.computer.storages.first().capacity +
                 "/" + "prix: " + str(order.computer.price_amount) + " fcfa" + "/" + "Couleur :" + order.computer.color.color,
            "delivery_date": order.delivery_date.strftime("%Y-%m-%d"),
            "id": order.pk,
            "is_traited": order.is_traited,
            # priority compare the order delivery date with the current date and return the priority high, medium or low
            # the delivery should be done in 3 days, it high if it remind one day, medium if it remind 1 day and some minutes nd low if it remind 2 days
            "priority":"High" if datetime.combine(order.delivery_date, datetime.min.time()) - datetime.now() <= timedelta(days=1) else \
                        "Medium" if datetime.combine(order.delivery_date, datetime.min.time()) - datetime.now() <= timedelta(days=2) else \
                        "Low",
            "supplier": order.computer.supplier.first_name + " " + order.computer.supplier.last_name,
            "supplier_id": order.computer.supplier.pk,
            "supplier_phone": order.computer.supplier.phone1 + "/" + order.computer.supplier.phone2,
            "supplier_company": order.computer.supplier.company,
            "percentage": order.computer.percentage
    }