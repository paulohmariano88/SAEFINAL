import serial


class SignalAnalogical:

    def __init__(self):
        self.SERIAL_PORT_CRITICAL = "COM3"  # Porta Crítica
        self.SERIAL_PORT_DANGER = "COM5"  # Porta Perigosa
        self.BAUD_RATE = 9600
        self.serial_danger  = None
        self.serial_critical = None

        try:
            self.serial_danger = serial.Serial(self.SERIAL_PORT_DANGER, self.BAUD_RATE, timeout=1)
            self.serial_critical = serial.Serial(self.SERIAL_PORT_CRITICAL, self.BAUD_RATE, timeout=1)
        except Exception as e:
            print("Error port {e}")

    def send_signal_critical(self):
        try:
            self.serial_critical.write(b"DANGER\n")
            print("Sinal DANGER Enviado")
        except Exception as e:
            print(f"Erro ao enviar o sinal {e}")
    
    def  send_signal_danger(self):
        try:
            self.serial_danger.write(b"CRITICAL\n")
            print("SINAL CRITICAL Enviado")
        except Exception as e:
            print(f"Erro a {e}")

    def close_communication(self):
        """
        Fecha as portas seriais.
        """
        if self.serial_danger is not None:
            self.serial_danger.close()
            print("Porta DANGER fechada.")
        if self.serial_critical is not None:
            self.serial_critical.close()
            print("Porta CRITICAL fechada.")
