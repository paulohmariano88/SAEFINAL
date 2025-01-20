# import RPi.GPIO as GPIO

# class Signal:
#     def __init__(self, relay_pin=17):
#         """
#         Configura o GPIO para o relé.
        
#         Args:
#             relay_pin (int): Número do pino GPIO usado para o relé.
#         """
#         self.RELAY_PIN = relay_pin
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.RELAY_PIN, GPIO.OUT)
#         GPIO.output(self.RELAY_PIN, GPIO.LOW)  # Começa com o relé desligado

#     def activate_relay(self):
#         """Ativa o relé."""
#         GPIO.output(self.RELAY_PIN, GPIO.HIGH)
#         print("Relé ativado.")

#     def deactivate_relay(self):
#         """Desativa o relé."""
#         GPIO.output(self.RELAY_PIN, GPIO.LOW)
#         print("Relé desativado.")

#     def cleanup_gpio(self):
#         """Limpa as configurações GPIO."""
#         GPIO.cleanup()
#         print("GPIO limpo e liberado.")
