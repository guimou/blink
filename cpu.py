#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import des bibliothèques
from blinkstick import blinkstick
import psutil

# Classe principale
class Main(blinkstick.BlinkStickPro):
    # Fonction principale
    def run(self):
        # Extinction des LEDs
        self.off()
    
        try:
            # Boucle infinie, pour que le programme tourne sans arrêt
            while (True):
                # Vidage de la programmation des LEDs
                self.clear()
                # On va chercher le pourcentage d'utilisatio du CPU, toutes les 0.5 secondes
                cpu = psutil.cpu_percent(interval=0.5)
                # Calcul de l'intensité d'utilisation (pour la couleur à afficher)
                intensity = int(255 * cpu / 100)
                # Calcul du nombre de LEDs à allumer
                level = int(self.r_led_count * cpu / 100)
                # On part de la LED 0
                led = 0
                # On passe sur chacune des LEDs
                while led <= self.r_led_count-1:
                    # Si c'est une LED qui doit être allumée, on lui met la bonne couleur, de vert à rouge
                    if led <= level:
                        self.set_color(channel=0, index=led, r=intensity, g=255-intensity, b=0)
                    # Sinon on l'éteint
                    else:
                        self.set_color(0, led, 0, 0, 0)
                    led += 1
                # Et finalement on envoit les données au Blinkstick
                self.send_data_all()
        # En cas d'interruption au clavier, on arrête
        except KeyboardInterrupt:
            self.off()
            return

# Lancement du programme, avec le nombre de LEDs en paramètre
main = Main(r_led_count=32)

# Si on a bien trouvé le Blinkstick on lance la fonction principale
if main.connect():
    main.run()
# Sinon on arrête
else:
    print u"Le Blinkstick n'a pas été trouvé..."
# Fin du programme
print u"Fin"
