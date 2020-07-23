from classes import *
import buttons

def check_user(tg_id):
    response = session.query(User_role).filter_by(id=tg_id).all()
    if not response.__len__() < 1:
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


def get_client(tg_id):
    clients = session.query(Client).filter_by(user_id=tg_id)
    user_instance = []
    for row in clients:
        user_instance = row
    response = session.query(City).filter_by(id=user_instance.city_id)
    city = 'Н/Д'
    for row in response:
        city = row.name

    return [user_instance, city]


def get_master(tg_id):
    masters = session.query(Master).filter_by(user_id=tg_id)
    user_instance = []
    for row in masters:
        user_instance = row
    response = session.query(City).filter_by(id=user_instance.city_id)
    city = 'Н/Д'
    for row in response:
        city = row.name
    point = get_point(tg_id)
    response = session.query(Placement).filter_by(id=user_instance.placement_id)
    placement = 'Н/Д'
    for row in response:
        placement = row.name
    return [user_instance, point, placement, city]


def create_user(user_id, name, username, role):
    if role == 'client':
        instance = Client(name=name, user_id=user_id, username=username)
    elif role == 'master':
        instance = Master(name=name, user_id=user_id, username=username)
    else:
        return
    session.add(instance)
    session.commit()
    return


def update_name(tg_id, name, role):
    if role == 'client':
        session.query(Client).filter(Client.user_id == tg_id). \
            update({Client.name: name}, synchronize_session=False)
    elif role == 'master':
        session.query(Master).filter(Master.user_id == tg_id). \
            update({Master.name: name}, synchronize_session=False)
    session.commit()
    return


def update_user_name(tg_id, username, role):
    if role == 'client':
        session.query(Client).filter(Client.user_id == tg_id). \
            update({Client.username: username}, synchronize_session=False)
    elif role == 'master':
        session.query(Master).filter(Master.user_id == tg_id). \
            update({Master.username: username}, synchronize_session=False)
    session.commit()
    return


def update_telephone(tg_id, telephone, role):
    if role == 'client':
        session.query(Client).filter(Client.user_id == tg_id). \
            update({Client.telephone: telephone}, synchronize_session=False)
    elif role == 'master':
        session.query(Master).filter(Master.user_id == tg_id). \
            update({Master.telephone: telephone}, synchronize_session=False)
    session.commit()
    return


def update_email(tg_id, email, role):
    if role == 'client':
        session.query(Client).filter(Client.user_id == tg_id). \
            update({Client.email: email}, synchronize_session=False)
    elif role == 'master':
        session.query(Master).filter(Master.user_id == tg_id). \
            update({Master.email: email}, synchronize_session=False)
    session.commit()
    return


def update_city(tg_id, city_id, role):
    if role == 'client':
        session.query(Client).filter(Client.user_id == tg_id). \
            update({Client.city_id: city_id}, synchronize_session=False)
    elif role == 'master':
        session.query(Master).filter(Master.user_id == tg_id). \
            update({Master.city_id: city_id}, synchronize_session=False)
    session.commit()
    return


def update_acc_photo(tg_id):
    session.query(Master).filter(Master.user_id == tg_id). \
        update({Master.image: True}, synchronize_session=False)
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
    session.query(Master).filter(Master.user_id == tg_id). \
        update({Master.details: details}, synchronize_session=False)
    session.commit()


def update_placement(tg_id, placement_id):
    session.query(Master).filter(Master.user_id == tg_id). \
        update({Master.placement_id: placement_id}, synchronize_session=False)
    session.commit()


def update_master_flag(tg_id):
    session.query(User_role).filter(User_role.id == tg_id). \
        update({User_role.master: True}, synchronize_session=False)
    session.commit()


def update_card(tg_id, card):
    session.query(Master).filter(Master.user_id == tg_id). \
        update({Master.card: card}, synchronize_session=False)
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


def get_masters(placement_id):
    return session.query(Master).filter(Master.placement_id == placement_id).all()


def save_master(master_id, user_id):
    if get_user_role(user_id):
        instance = Saved_masters(master_id=master_id, client_id_master_acc=user_id)
    else:
        instance = Saved_masters(master_id=master_id, client_id=user_id)
    session.add(instance)
    session.commit()


def check_saved_masters(master_id, user_id):
    if get_user_role(user_id):
        masters = session.query(Saved_masters).filter(Saved_masters.master_id == master_id,
                                                      Saved_masters.client_id_master_acc == user_id).all()
    else:
        masters = session.query(Saved_masters).filter(Saved_masters.master_id == master_id,
                                                      Saved_masters.client_id == user_id).all()
    if masters.__len__() > 0:
        return False
    else:
        return True


def get_saved_masters(user_id):
    if get_user_role(user_id):
        return session.query(Saved_masters).filter(Saved_masters.client_id_master_acc == user_id).all()
    else:
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
    return session.query(Master).filter(Master.user_id == master_id).all()


def update_order_as_done(order_id):
    session.query(Order).filter(Order.id == order_id). \
        update({Order.done: True}, synchronize_session=False)
    session.commit()


def check_rating(user_id, master_id):
    if get_user_role(user_id):
        rating = session.query(Rating).filter(Rating.master_id == master_id,
                                              Rating.client_id_master_acc == user_id).all()
    else:
        rating = session.query(Rating).filter(Rating.master_id == master_id,
                                              Rating.client_id == user_id).all()
    if rating.__len__() > 0:
        return False
    else:
        return True


def check_feedback(user_id, master_id):
    if get_user_role(user_id):
        feedback = session.query(Feedback).filter(Feedback.master_id == master_id,
                                                  Feedback.client_id_master_acc == user_id).all()
    else:
        feedback = session.query(Feedback).filter(Feedback.master_id == master_id,
                                                  Feedback.client_id == user_id).all()
    if feedback.__len__() > 0:
        return False
    else:
        return True


def create_rating(master_id, client_id, point):
    if check_rating(master_id=master_id, user_id=client_id):
        if get_user_role(client_id):
            instance = Rating(master_id=master_id, client_id_master_acc=client_id, points=point)
        else:
            instance = Rating(master_id=master_id, client_id=client_id, points=point)
        session.add(instance)
        session.commit()
        return True
    else:
        return None


def create_feedback(master_id, client_id, feedback):
    if check_feedback(master_id=master_id, user_id=client_id):
        if get_user_role(client_id):
            instance = Feedback(master_id=master_id, client_id_master_acc=client_id, feedback=feedback)
        else:
            instance = Feedback(master_id=master_id, client_id=client_id, feedback=feedback)
        session.add(instance)
        session.commit()
        return True
    else:
        return None


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


def get_days(user_id):
    data = session.query(Working_days).filter(Working_days.master_id == user_id).all()
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


def set_current_role(user_id, role):
    session.query(Master).filter(Master.user_id == user_id). \
        update({Master.cur_role: role}, synchronize_session=False)
    session.commit()


def create_user_role(tg_id):
    instance = User_role(id=tg_id)
    session.add(instance)
    session.commit()


def update_to_master(tg_id):
    session.query(User_role).filter(User_role.id == tg_id). \
        update({User_role.master: True}, synchronize_session=False)
    session.commit()


def get_user_role(tg_id):
    response = session.query(User_role).filter_by(id=tg_id).all()
    return response[0].master


def get_city_by_id(city_id):
    city = session.query(City).filter_by(id=city_id).all()
    return city[0].name


def move_user(user_id):
    user_instance = get_client(user_id)
    instance = Master(name=user_instance[0].name, user_id=user_instance[0].user_id, username=user_instance[0].username,
                      telephone=user_instance[0].telephone, city_id=user_instance[0].city_id)
    session.add(instance)
    session.commit()
    update_to_master(user_id)


def create_working_day(user_id, day_name):
    instance = Working_days(master_id=user_id, day_name=day_name, day_num=buttons.days.index(day_name))
    session.add(instance)
    session.commit()


def update_working_time(user_id, time):
    session.query(Working_days).filter(Working_days.master_id == user_id). \
        update({Working_days.working_hours: time}, synchronize_session=False)
    session.commit()

def edit_day(day_id, non_active=False, set_time=False, time=None, active=False):
    if non_active:
        session.query(Working_days).filter(Working_days.id == day_id). \
            update({Working_days.non_active: True}, synchronize_session=False)
        session.commit()
        return True
    elif set_time:
        session.query(Working_days).filter(Working_days.id == day_id). \
            update({Working_days.working_hours: time}, synchronize_session=False)
        session.commit()
        return True
    elif active:
        session.query(Working_days).filter(Working_days.id == day_id). \
            update({Working_days.non_active: False}, synchronize_session=False)
        session.commit()
        return True
    else:
        return None

def get_available_days(master_id, current_day_num):
    data = session.query(Working_days).filter(Working_days.master_id == master_id,
                                              Working_days.day_num >= int(current_day_num),
                                              Working_days.non_active == 0).all()
    if data is None:
        return []
    else:
        return data

# if __name__ == '__main__':
#     data = session.query(Service_type.name).filter(Service_type.master_id == '405423146',
#                                             Service_type.segment_id == '1').all()
#     print(data)
