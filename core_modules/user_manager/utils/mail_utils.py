from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives, get_connection


class utils:
    @staticmethod
    def get_connection_for_mail():
        try:
            EMAIL_HOST = settings.EMAIL_HOST
            EMAIL_PORT = settings.EMAIL_PORT
            EMAIL_HOST_USER = settings.EMAIL_HOST_USER
            EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
            EMAIL_USE_TLS = settings.EMAIL_USE_TLS
        except ImportError:
            EMAIL_HOST = None
            EMAIL_PORT = None
            EMAIL_HOST_USER = None
            EMAIL_HOST_PASSWORD = None
            EMAIL_USE_TLS = True
        if EMAIL_HOST and EMAIL_PORT and EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
            try:
                connection = get_connection(
                    host=EMAIL_HOST,
                    port=EMAIL_PORT,
                    username=EMAIL_HOST_USER,
                    password=EMAIL_HOST_PASSWORD,
                    use_tls=EMAIL_USE_TLS,
                )
            except Exception as E:
                connection = None
                print("Che dio ti fulmini sei tu il bastardo che va in errore:", E)
            return connection
        else:
            raise ValidationError("Dio bono non funge la mail, ma te la sei settata sul remote/settings?")

    @staticmethod
    def send_mail(destinatario, oggetto, corpo, mittente=None):
        if mittente is None:
            mittente = "efestodev@info.it"
        email = EmailMultiAlternatives(oggetto, corpo, mittente, [destinatario], connection=get_connection())
        try:
            print("EMAIL INVIATA A:", destinatario)
            email.send()
        except Exception as E:
            print(
                "Errore invio mail <<Dest:{}; Oggetto:{}; Mittente:{}; Corpo:{};\n Errore:{}".format(
                    destinatario, oggetto, mittente, corpo, E
                )
            )
