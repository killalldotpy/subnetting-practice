import random
import ipaddress
import os

# Funktion för att rensa konsolen
def rensa_skärm():
    os.system('cls' if os.name == 'nt' else 'clear')

# ASCII-bannern som visas konstant, med "by NRG" under
ascii_banner = """
   _____ __  ______  _   _________________________   ________
  / ___// / / / __ )/ | / / ____/_  __/_  __/  _/ | / / ____/
  \__ \/ / / / __  /  |/ / __/   / /   / /  / //  |/ / / __  
 ___/ / /_/ / /_/ / /|  / /___  / /   / / _/ // /|  / /_/ /  
/____/\____/_____/_/ |_/_____/ /_/   /_/ /___/_/ |_/\____/   
                                                            
                                                 by NRG                             
"""

# Funktion för att identifiera IP-klass
def identifiera_ip_klass(ip):
    första_oktetten = int(ip.split('.')[0])
    if 1 <= första_oktetten <= 126:
        return "A"
    elif 128 <= första_oktetten <= 191:
        return "B"
    elif 192 <= första_oktetten <= 223:
        return "C"
    else:
        return "Okänd"

# Skapar en klass för att hantera varje fråga
class SubnettingFråga:
    def __init__(self, ip, cidr):
        self.ip = ip
        self.cidr = cidr
        self.nätverk = ipaddress.IPv4Network(f'{self.ip}/{self.cidr}', strict=False)
        self.ip_klass = identifiera_ip_klass(self.ip)

    def ställ_fråga(self):
        print(f"\nIP-adress: {self.ip}/{self.cidr}\n")
        print("1. Vilken klass tillhör denna IP-adress? (A, B eller C)")
        print("2. Vad är subnätmasken?")
        print("3. Vad är nätverksadressen?")
        print("4. Vad är broadcastadressen?")
        print("5. Hur många värdar är tillgängliga i detta subnät?\n")

        subnet_mask = str(self.nätverk.netmask)
        nätverksadress = str(self.nätverk.network_address)
        broadcast_adress = str(self.nätverk.broadcast_address)
        antal_värdar = self.nätverk.num_addresses - 2  # Antal värdar (exkluderar nätverks- och broadcastadresser)

        # Hämta svar från användaren
        ip_klass_svar = input("Skriv in IP-klassen (A, B eller C): ")
        mask_svar = input("Skriv in subnätmasken: ")
        nätverk_svar = input("Skriv in nätverksadressen: ")
        broadcast_svar = input("Skriv in broadcastadressen: ")
        värdar_svar = input("Skriv in antalet tillgängliga värdar: ")

        # Kontrollera och visa feedback
        rätt = 0

        if ip_klass_svar.upper() == self.ip_klass:
            rätt += 1
        else:
            print(f"Fel! Korrekt IP-klass är: {self.ip_klass}")

        if mask_svar == subnet_mask:
            rätt += 1
        else:
            print(f"Fel! Korrekt subnätmask är: {subnet_mask}")

        if nätverk_svar == nätverksadress:
            rätt += 1
        else:
            print(f"Fel! Korrekt nätverksadress är: {nätverksadress}")

        if broadcast_svar == broadcast_adress:
            rätt += 1
        else:
            print(f"Fel! Korrekt broadcastadress är: {broadcast_adress}")

        if värdar_svar == str(antal_värdar):
            rätt += 1
        else:
            print(f"Fel! Korrekt antal tillgängliga värdar är: {antal_värdar}")

        return rätt

# Funktion för att generera slumpmässig IP från klass A, B eller C
def generera_slumpmässig_ip():
    ip_klass = random.choice(['A', 'B', 'C'])

    if ip_klass == 'A':
        första_oktetten = random.randint(1, 126)  # Klass A-adresser
        cidr = random.randint(8, 30)  # CIDR mellan /8 och /30
    elif ip_klass == 'B':
        första_oktetten = random.randint(128, 191)  # Klass B-adresser
        cidr = random.randint(16, 30)  # CIDR mellan /16 och /30
    else:  # Klass C
        första_oktetten = random.randint(192, 223)  # Klass C-adresser
        cidr = random.randint(24, 30)  # CIDR mellan /24 och /30

    andra_oktetten = random.randint(0, 255)
    tredje_oktetten = random.randint(0, 255)
    fjärde_oktetten = random.randint(0, 255)

    ip = f"{första_oktetten}.{andra_oktetten}.{tredje_oktetten}.{fjärde_oktetten}"
    return ip, cidr

# Funktion för att skapa en fråga med slumpmässig IP och CIDR
def generera_slumpmässig_fråga():
    ip, cidr = generera_slumpmässig_ip()
    return SubnettingFråga(ip, cidr)

# Huvudfunktion för att köra quizet
def kör_quiz():
    antal_frågor = 50  # Antal frågor
    rätt_svar = 0

    for i in range(antal_frågor):
        rensa_skärm()  # Rensar skärmen före varje fråga
        print(ascii_banner)  # Skriver ut ASCII-konsten varje gång
        print(f"\nFråga {i+1} av {antal_frågor}:")
        fråga = generera_slumpmässig_fråga()
        rätt = fråga.ställ_fråga()
        print(f"\nDu fick {rätt} av 5 rätt på denna fråga.")  # Uppdaterad för 5 frågor per fråga

        if rätt == 5:
            rätt_svar += 1

        input("\nTryck Enter för att gå vidare till nästa fråga...")  # Väntar på att användaren trycker Enter

    rensa_skärm()
    print(ascii_banner)  # Skriver ut ASCII-konsten en sista gång
    print(f"\nDu fick {rätt_svar} av {antal_frågor} frågor rätt!")

# Starta quizet
if __name__ == "__main__":
    rensa_skärm()
    print(ascii_banner)  # Visar bannern när quizet startar
    print("Välkommen till Subnetting-Quiz!")
    kör_quiz()