# MeetingPro - Réservation de Salles

## Contributeurs
- Dorian Bismuth
- Ahmad Hassan

---

## Description

**MeetingPro** est une application Python permettant de gérer les réservations de salles au sein d'une organisation.  
Elle permet aux utilisateurs d’ajouter des clients et des salles, de réserver des salles pour des créneaux horaires spécifiques, et de visualiser toutes les réservations et disponibilités via une interface graphique.

---

## Structure du projet

Afin de réaliser ce projet qu'est **MeetingPro**, on a due dans un premier temps découper les taches afin de pouvoir réaliser d'un côté la partie data du programme, et d'un autre côté la partie interface. Toutes ces fonctions et classes ont été faite dans un repertoire nommé src (source) et l'appelle des classe et des fonctions s'est fait sur le fichier main.py hors du src.

Afin de structurer au mieux possible les appels entre les fonctions et les classes, nous nous sommes inspirés d'un diagramme de classes nous permettant ainsi d'avoir un visuel sur les différentes relations d'appel de fonctions/classes que pourraient avoir chaque partie de notre code. Et finalement, on retrouvait un schéma comme celui-ci :

---

**Diagramme de Classes**

```plaintext
+-------------------+           +-------------------+           +-----------------------+
|   New_Customer    |           |    New_Room       |<>-------->|    type_of_room       |
+-------------------+           +-------------------+           +-----------------------+
| - id_customer     |           | - id              |           | - Standard            |
| - name            |           | - capacity        |           | - Conference          |
| - surname         |           | - room:           |           | - Informatics         |
| - email           |           |   type_of_room    |           +-----------------------+
+-------------------+           +-------------------+
                                | +room_infos()     |
                                +-------------------+

+-----------------------+
|   Reserve_a_room      |
+-----------------------+
| - room_id             |
| - id_customer         |
| - date                |
| - debut               |
| - fin                 |
| - id_reservation      |
+-----------------------+
| +reservation_infos()  |
+-----------------------+

+-------------------------------------------------------------+
|                        Database                             |
+-------------------------------------------------------------+
| - filepath: str                                             |
| - data: dict                                                |
+-------------------------------------------------------------+
| +add_customer(customer: New_Customer)                       |
| +add_room(room: New_Room)                                   |
| +add_reservation(reservation: Reserve_a_room)               |
| +get_customers() -> list[New_Customer]                      |
| +get_rooms() -> list[New_Room]                              |
| +get_reservations() -> list[Reserve_a_room]                 |
+-------------------------------------------------------------+
         ^             ^             ^
         |             |             |
         |             |             |
         |             |             |
         +-------------+-------------+
           Utilise/instancie ces classes
```

---
Le code contient aussi un autre répertoire nommé **tests**, dans lequel ce trouve les tests de toutes les classes ou les fonctions des fichiers du répertoire **src** jugés utile à être testés à l'exception de ceux provenant du fichier python gérant l'interface de MeetingPro nommé **GUI.py** (Graphical User Interface), car il est inutile de tester si une interface est bien créée ou si elle a bien fait appelle à d'autres fonctions ou classes des autres fichiers.

Afin de tester chacunes des fonctions ou des classes nécessaires, il suffira de se placer dans le fichier python du repertoire **tests** que l'on veut tester, puis d'utiliser la commande **pytest** dans le terminal afin de tester les fonctions/classes du fichier.

Le fichier **pyproject.toml** renseigne sur certaines infos du code et de leurs créateurs (nous). Et le fichier **.gitignore** renseigne sur certaine infos de la versions de Python ainsi que sur certains packages utilisables (ou utilisés).

---

## Utilisation et exécution de l'application MeetingPro

- La toute première étape à l'utilisation de MeetingPro App est de cloner le lien du repository sur lequel se trouve le projet afin de le pull en local (sur son ordinateur).
Une fois cela fait, l'utilisateur doit ouvrir le dossier du projet sur un logiciel de code (ex: VS Code). Une fois le dossier ouvert, l'utilisateur doit ouvrir le repertoire **MeetingPro-Room-Booking**, puis le répertoire **src**, et enfin le fichier python **GUI.py**.
A l'issue duquel, il devra simplement compiler le code et l'interface graphique s'ouvrira.
Pour une interface optimale, il est conseillé d'agrandir l'interface en pleine écran (ou au moins de l'agrandir de 1.5 fois sa taille de base).

- Maintenant que l'interface est ouvert, il suffit de suivre ce qu'indique les boutons. Toutes données ajoutées à la base de données peut se retrouver sous formes de tableau dans l'affichage. Il suffit alors d'appuyer sur **Display**, et on retrouve en bas de la fenêtre 4 booutons afin d'afficher les clients enregistrés **Show Customers**, les pièces enregistrer **Show Rooms**, les réservations de pièces qui ont été faites **Show Reservations**, ainsi que les horaires de chaques salles encore réservable **Show Availability** sachant qu'une salle peut être réservé au minimum 30min à partir de 08:00 du matin jusqu'à 20:00 du soir.

- Si certaines de ces caractéristiques sont manquantes, il suffit juste d'aggrandir la page un petit peu plus afin de les voir apparaitre.
Lors d'ajout d'une de ces caractéristiques, si vous voulez la voir apparaitre sur le tableau correspondant, vous devez raffraichir la page, et pour cela il suffit juste de cliquer à nouveau sur le bouton menant à l'affichage que vous souhaitez voir être mis à jour.

- Afin d'ajouter un client ou bien une nouvelle salle, soit vous partez de la page **home** indiqué en haut à gauche de l'écran (avec laquel vous pouvez aussi intéragir) puis vous cliquez sur **Add**, soit vous vous rendez directement sur la page **Add** indiquez en haut à gauche. Suite à quoi, en fonction de ce que vous voulez ajouter, vous n'avez qu'à appuyer sur le bouton qui vous est utile et rentrer les informations du nouveau client ou de la nouvelle pièce que vous ajoutez. Lorsque vous créeez une nouvelle pièce, vous devez choisir un ID, celui peut contenir n'importe quel suite de caractères ou de chiffres ainsi que les caractères spéciaux "**.**" ou "**_**". Si une pièce ou un nouveau client ajouté à l'appli possède des informations identiques comme le même id pour plusieurs salles, ou la même adresse mail pour plusieurs clients, un message d'erreur sera alors renvoyé indiquant la cause de l'erreur.

- Enfin la dernière étape qui est la réservation, de la même manière que précedemment, il suffit d'appuyer sur le bouton **Book** qui est soit sur l'écran d'acceuil (**Home**), soit directement appuyer sur **Book** en haut à gauche. Suite à quoi, la reservation se fait de telle sorte que vous devez d'abord choisir le client qui reserve une salle, puis entrer les informations concernant la réservation de la salle comme la date, la durée,le type de pièce dont le client a besoin ainsi que le nombre de personnes qu'il y aura. Les élements à remplir manuellement devront être rempli de la même manière que ce qui est indiquée dans les informations entre parenthèses. Enfin il suffira d'appuyer sur **Search available rooms** afin d'aficher un dernier menu déroulant indiquant les salles disponibles en fonctions des différents critères choisit par le client, et cocher une salle correspondant aux critères recherchés avant de valider. 
Evidemment, en cas d'erreur ou d'informations manquantes, un message d'erreur apparaitra avec d'ecrit la raison de l'erreur.

- Maintenant, si vous voulez supprimer un client, une salle, ou une reservation, il vous suffit de revenir sur le logiciel de programmation que vous avez utilisez afin d'ouvrir l'interface, de trouver dans le repertoire **MeetingPro-Room-Booking** deux fichier en **.json** nommés **data.json** ainsi que **utilisateur.json**, de les ouvrir et de retirer les blocs comprenant les informations à retirer en N'OUBLIANT PAS LES CARACTERES SUIVANT "{" et "}"
AVANT ET APRES LES BLOCS. ET SI LE BLOC EST A LA FIN D'UNE DES CLASSES **CLIENT**, **SALLE**, OU **RESERVATION**, IL FAUT AUSSI ENLEVER LA VIRGULE PRECEDANT LE BLOC.

---
## Info utile :

En cas de compilation du code GUI.py plusieurs fois, l'interface s'ouvrira autant de fois que vous aurez compilez le code, il est alors déconseillé de compiler le code plusieurs fois.

---

