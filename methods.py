from classes import *


def check_user(tg_id):
    response = session.query(User).filter_by(user_id=tg_id)
    for row in response:
        if row:
            return True
        else:
            return False


def get_point(user_id):
    response = session.query(Rating).filter(Rating.master_id == user_id)
    counter = 0
    point = 0
    for row in response:
        point += row.points
        counter += 1
    if counter == 0:
        return 0
    return round(point / counter, 0)


def get_user(tg_id):
    response = session.query(User).filter_by(user_id=tg_id)
    user_instance = []
    for row in response:
        user_instance = row
    point = get_point(tg_id)
    response = session.query(Placement).filter_by(id=user_instance.placement_id)
    placement = 'Н/Д'
    for row in response:
        placement = row.name
    response = session.query(City).filter_by(id=user_instance.city_id)
    city = 'Н/Д'
    for row in response:
        city = row.name
    return [user_instance, point, placement, city]


def create_user(user_id, name, username):
    instance = User(name=name, user_id=user_id, username=username)
    session.add(instance)
    session.commit()


def update_name(tg_id, name):
    session.query(User).filter(User.user_id == tg_id). \
        update({User.name: name}, synchronize_session=False)
    session.commit()


def update_user_name(tg_id, username):
    session.query(User).filter(User.user_id == tg_id). \
        update({User.username: username}, synchronize_session=False)
    session.commit()


def update_telephone(tg_id, telephone):
    session.query(User).filter(User.user_id == tg_id). \
        update({User.telephone: telephone}, synchronize_session=False)
    session.commit()


def update_email(tg_id, email):
    session.query(User).filter(User.user_id == tg_id). \
        update({User.email: email}, synchronize_session=False)
    session.commit()


def update_city(tg_id, city_id):
    session.query(User).filter(User.user_id == tg_id). \
        update({User.city_id: city_id}, synchronize_session=False)
    session.commit()


def update_acc_photo(tg_id):
    session.query(User).filter(User.user_id == tg_id). \
        update({User.image: True}, synchronize_session=False)
    session.commit()


def create_certificate(tg_id, photo_path):
    instance = Media(user_id=tg_id, image=photo_path)
    session.add(instance)
    session.commit()


def update_certificate_details(tg_id, image, description):
    session.query(Media).filter(Media.image == image, Media.user_id == tg_id). \
        update({Media.description: description}, synchronize_session=False)
    session.commit()


def update_acc_details(tg_id, details):
    session.query(User).filter(User.user_id == tg_id). \
        update({User.details: details}, synchronize_session=False)
    session.commit()


def update_placement(tg_id, placement_id):
    session.query(User).filter(User.user_id == tg_id). \
        update({User.placement_id: placement_id}, synchronize_session=False)
    session.commit()


def update_master_flag(tg_id):
    session.query(User).filter(User.user_id == tg_id). \
        update({User.master: True}, synchronize_session=False)
    session.commit()


def update_card(tg_id, card):
    session.query(User).filter(User.user_id == tg_id). \
        update({User.card: card}, synchronize_session=False)
    session.commit()


def get_cities():
    return session.query(City).all()


def get_placements(city_id):
    return session.query(Placement).filter(Placement.city_id == city_id).all()


def create_sample_service(tg_id, service_name):
    instance = Services(master_id=tg_id, name=service_name)
    session.add(instance)
    session.commit()
    services = session.query(Services).filter(Services.master_id == tg_id, Services.name == service_name)
    for instance in services:
        return instance.id


def update_service_photo(tg_id, service_id, image):
    session.query(Services).filter(Services.master_id == tg_id, Services.id == service_id). \
        update({Services.image: image}, synchronize_session=False)
    session.commit()


def get_certificates(tg_id):
    return session.query(Media).filter(Media.user_id == tg_id).all()


def get_sample_services(tg_id):
    return session.query(Services).filter(Services.master_id == tg_id).all()


def create_time_slot(user_id, start_time, end_time, date):
    instance = Time_slot(master_id=user_id, start_time=start_time, end_time=end_time, date=date)
    session.add(instance)
    session.commit()


def get_masters(placement_id):
    return session.query(User).filter(User.placement_id == placement_id, User.master).all()


def get_time_slots(user_id):
    return session.query(Time_slot).filter(Time_slot.master_id == user_id, Time_slot.ordered == '0').all()


def save_master(master_id, user_id):
    instance = Saved_masters(master_id=master_id, client_id=user_id)
    session.add(instance)
    session.commit()


def check_saved_masters(master_id, user_id):
    masters = session.query(Saved_masters).filter(Saved_masters.master_id == master_id,
                                                  Saved_masters.client_id == user_id).all()
    if masters.__len__() > 0:
        return False
    else:
        return True


def get_saved_masters(user_id):
    return session.query(Saved_masters).filter(Saved_masters.client_id == user_id).all()


def create_service(tg_id, service_name, segment):
    instance = Service_type(master_id=tg_id, name=service_name, segment_id=segment)
    session.add(instance)
    session.commit()
    return session.query(Service_type).filter(Service_type.master_id == tg_id, Service_type.name == service_name,
                                              Service_type.segment_id == segment).value(Service_type.id)


def get_services(tg_id, segment):
    return session.query(Service_type).filter(Service_type.master_id == tg_id, Service_type.segment_id == segment).all()


def get_master_by_id(master_id):
    return session.query(User).filter(User.user_id == master_id).all()


def create_order(time_slot_id, client_id, master_id, service_id):
    instance = Order(time_slot_id=time_slot_id, client_id=client_id,
                     master_id=master_id, service_id=service_id)
    session.add(instance)
    session.commit()


def set_busy_time_slot(time_slot_id):
    session.query(Time_slot).filter(Time_slot.id == time_slot_id). \
        update({Time_slot.ordered: True}, synchronize_session=False)
    session.commit()


def get_orders_for_master(master_id, done):
    return session.query(Order).filter(Order.master_id == master_id, Order.done == done, Order.canceled == '0').all()


def update_order_as_done(order_id):
    session.query(Order).filter(Order.id == order_id). \
        update({Order.done: True}, synchronize_session=False)
    session.commit()


def get_orders_for_client(client_id, done):
    return session.query(Order).filter(Order.client_id == client_id, Order.done == done, Order.canceled == '0').all()


def get_time_slot_by_id(time_slot_id):
    return session.query(Time_slot).filter(Time_slot.id == time_slot_id).all()


def check_rating(user_id, master_id):
    rating = session.query(Rating).filter(Rating.master_id == master_id,
                                          Rating.client_id == user_id).all()
    if rating.__len__() > 0:
        return False
    else:
        return True


def check_feedback(user_id, master_id):
    feedback = session.query(Feedback).filter(Feedback.master_id == master_id,
                                              Feedback.client_id == user_id).all()
    if feedback.__len__() > 0:
        return False
    else:
        return True


def create_rating(master_id, client_id, point):
    instance = Rating(master_id=master_id, client_id=client_id, points=point)
    session.add(instance)
    session.commit()


def create_feedback(master_id, client_id, feedback):
    instance = Feedback(master_id=master_id, client_id=client_id, feedback=feedback)
    session.add(instance)
    session.commit()


def get_service_by_id(service_id):
    return session.query(Service_type).filter(Service_type.id == service_id).all()


def get_service_segments():
    return session.query(Service_segment).all()


def get_service_names(user_id, segment):
    data = session.query(Service_type.name).filter(Service_type.master_id == user_id,
                                                   Service_type.segment_id == segment).all()
    if data is None:
        return []
    else:
        return data


def update_service_cost(service_id, money_cost):
    session.query(Service_type).filter(Service_type.id == service_id). \
        update({Service_type.money_cost: money_cost}, synchronize_session=False)
    session.commit()


def update_service_time_cost(service_id, time_cost):
    session.query(Service_type).filter(Service_type.id == service_id). \
        update({Service_type.time_cost: time_cost}, synchronize_session=False)
    session.commit()


def delete_service(service_id):
    print(service_id)
    session.query(Service_type).filter(Service_type.id == service_id). \
        delete()
    session.commit()


def check_service(name, user_id):
    services = session.query(Services).filter(Services.name == name, Services.master_id == user_id).all()
    if services.__len__() > 0:
        return False
    else:
        return True


def update_sample_service_name(service_id, name):
    session.query(Services).filter(Services.id == service_id). \
        update({Services.name: name}, synchronize_session=False)
    session.commit()


def delete_sample_service(service_id):
    session.query(Services).filter(Services.id == service_id). \
        delete()
    session.commit()


def update_certificate_description(certificate_id, description):
    session.query(Media).filter(Media.id == certificate_id). \
        update({Media.description: description}, synchronize_session=False)
    session.commit()


def delete_certificate(certificate_id):
    session.query(Media).filter(Media.id == certificate_id). \
        delete()
    session.commit()


def get_sample_service_by_id(service_id):
    return session.query(Services).filter(Services.id == service_id).all()


def get_certificate_by_id(certificate_id):
    return session.query(Media).filter(Media.id == certificate_id).all()


# if __name__ == '__main__':
#     data = session.query(Service_type.name).filter(Service_type.master_id == '405423146',
#                                             Service_type.segment_id == '1').all()
#     print(data)
