# waterstandtwitter
Versturen waterstand naar Twitter

## Aanleiding
Voor het maken van wandeling langs de IJssel bij Hattem vond ik het handig om te weten of ik geen natte
voeten zou krijgen. De waterstand die Rijkswaterstaat meet bij Zwolle geeft een goede indicatie van de
mogelijkheden om met droge voeten de wandeling te kunnen voltooien.  
Aangezien ik werk in de automatisering en ik het leuk vind om dit als hobby-project te doen heb ik een
Twitter-account voor de waterstand bij het [Katerveer in Zwolle](https://twitter.com/waterstandkatv)
gemaakt.  
Opmerking: ik gebruik de naam Twitter omdat ik nog niet kan wennen aan X.

## Uitvoering
De gegevens komen van Rijkswaterstaat. Deze data is vrij beschikbaar zonder autorisatie. De API is niet
beschreven, maar door het klikken op de kaart in de browser en het bekijken van het request is goed te
achterhalen hoe de data er uit ziet.  
Aangezien het generiek is heb ik niet alleen de waterstand bij Zwolle, maar ook de voorliggende bij Wijhe
en nog een eerder bij Zutphen toegevoegd. Hieronder staan de stappen voor het configureren.  

* De locatie en afkorting van de naam op [waterinfo](https://waterinfo.rws.nl/#/expert/Waterhoogten?parameters=Waterhoogte___20Oppervlaktewater___20t.o.v.___20Normaal___20Amsterdams___20Peil___20in___20cm)
* Gebruik een e-mailadres wat uniek is, dat vindt Twitter beter.
* Maak een Twitter-account en koppel deze aan de e-mail. Hierbij heb ik gekozen voor `waterstand<LOC_ID>`
* Genereer api keys op https://apps.twitter.com/
* Plaats de keys in een script setenvvars.sh die een directory hoger staat dan de repository.
* Voeg een regel toe aan `waterstandtwitter.py`

De sourcecode spreekt hopelijk voor zich. Met het build-script kan er een docker image gemaakt worden.  
Via de cron-job wordt deze elke 8 uur uitgevoerd.