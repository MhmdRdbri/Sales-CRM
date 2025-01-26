from ippanel import Client, Error, HTTPError,ResponseCode

def prepare_sms_message(opportunity):
    priority_translations = {
        "low_priority": "اولویت پایین",
        "mid_priority": "اولویت متوسط",
        "high_priority": "اولویت بالا",
    }

    buyer_type_translations = {
        "OM": "عمده",
        "KH": "خرده",
    }

    message = f"یادآوری فرصت فروش: پیگیری با مشتری {opportunity.profile.full_name} در تاریخ {opportunity.follow_up_date} (امروز).\n" \
              f"اولویت: {priority_translations.get(opportunity.opportunity_priority, 'نامشخص')}.\n" \
              f"نوع خریدار: {buyer_type_translations.get(opportunity.buyer_type, 'نامشخص')}.\n" \
              f"توضیحات: {opportunity.description or 'بدون توضیحات'}."

    return message

def send_sms_to_users(to, message):
    client = Client("AMGn2I3D2nVl3RiQ2pvOIwztpE1EopPX3LHwmDlfSaA=")
    try:
        message_id = client.send("+983000505", to, message, "summary")
        print(message_id)
        
    except Error as e:
        print("Error handled => code: %s, message: %s" % (e.code, e.message))

        if e.code == ResponseCode.ErrUnprocessableEntity.value:
            for field in e.message:
                print("Field: %s , Errors: %s" % (field, e.message[field]))
    except HTTPError as e:
        print("Error handled => code: %s" % (e))
