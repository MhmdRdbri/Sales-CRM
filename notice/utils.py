from ippanel import Client, Error, HTTPError, ResponseCode

def send_sms(to, message):
    

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