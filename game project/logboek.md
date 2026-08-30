## 5 Augustus 2026

Vandaag begin ik aan het introductieproject.  
Ik heb alles geïnitialiseerd en de repository in orde gemaakt, dus het werk kan beginnen.

## 6 Augustus 2026

Tutorial volledig gevolgd en de basiscode van Blackjack nagemaakt in Pygame.

Tijdens het volgen van de tutorial merkte ik dat sommige stukken code vrij snel voorbij gingen. Vooral het tekenen van onderdelen op het scherm en het werken met `pygame.Rect` en `blit()` waren nog niet meteen duidelijk. Na het programma een paar keer te runnen begon de structuur van de game-loop wel duidelijker te worden.

## 7 Augustus 2026

Game een paar keer gespeeld om inspiratie op te doen voor een uitbreiding.

Ik wil iets doen in het thema Fantasy, aangezien ik zelf een fantasy liefhebber ben.

Ik ga een uitbreiding maken waarbij zowel de speler als de tegenstander HP hebben en de verliezer na elke verloren hand HP verliest. Degene die als eerste 0 HP heeft, verliest het gevecht.

Eerst wil ik dit simpel houden met één tegenstander: een Goblin.

## 9 Augustus 2026

Begonnen met de eerste versie van de fantasy-uitbreiding.

Ik heb `player_hp` en `goblin_hp` toegevoegd en beide op 100 gezet. Daarna een eenvoudige functie gemaakt om de HP van de speler en de Goblin op het scherm te tonen.

Hier heb ik even mee moeten zoeken omdat de tekst op sommige plaatsen over de kaarten en scores heen kwam. Uiteindelijk de coördinaten wat aangepast zodat alles leesbaar bleef.

Ook de kleuren van de kaarten iets aangepast om het spel iets meer een fantasy-uitstraling te geven.

## 10 Augustus 2026

Vandaag geprobeerd om de HP daadwerkelijk te laten veranderen wanneer een hand afgelopen is.

Eerst werd er meerdere keren HP afgetrokken omdat de `check_endgame()`-functie in de game-loop voortdurend opnieuw wordt uitgevoerd. Daardoor kon één verloren hand ineens veel meer dan 20 HP kosten.

Na wat zoeken bleek dat de bestaande variabele `add_score` hiervoor al bruikbaar was. Ik heb het verlagen van de HP daarom binnen dezelfde controle gezet, zodat er per hand maar één keer schade wordt gedaan.

Bij winst verliest de Goblin 20 HP en bij verlies verliest de speler 20 HP.

## 13 Augustus 2026

Versie 1.0 verder getest.

Er zat nog een probleem in wanneer iemand 0 HP had en ik op `NEW HAND` klikte. De nieuwe ronde begon wel, maar de HP bleef op 0 staan.

Daarom bij het starten van een nieuw gevecht toegevoegd dat zowel `player_hp` als `goblin_hp` terug naar 100 worden gezet.

De eerste fantasy-versie werkt nu zoals bedoeld: meerdere handen Blackjack spelen totdat de Hero of Goblin geen HP meer heeft.

## 15 Augustus 2026

Nagedacht over hoe ik de uitbreiding iets interessanter kon maken zonder de originele Blackjack-code volledig te veranderen.

Besloten om meerdere vijanden toe te voegen. De speler moet nu eerst een Goblin, daarna een Orc en uiteindelijk een Dragon verslaan.

Hiervoor heb ik twee lijsten gemaakt:

`enemies = ['Goblin', 'Orc', 'Dragon']`

en een lijst met hun HP.

Dit vond ik eerst wat verwarrend omdat ik moest zorgen dat de juiste naam en HP steeds dezelfde index gebruikten.

## 16 Augustus 2026

Verder gewerkt aan versie 2.0.

De Goblin heeft 100 HP, de Orc 120 HP en de Dragon 150 HP.

Ik heb eerst geprobeerd om dezelfde `goblin_hp`-variabele te blijven gebruiken voor alle vijanden, maar dat werd snel onduidelijk. Daarom heb ik deze veranderd naar `enemy_hp` en gebruik ik `enemy_number` om bij te houden tegen welke vijand de speler momenteel vecht.

Bij het verslaan van een vijand wordt `enemy_number` met één verhoogd en worden de naam en HP van de volgende vijand geladen.

## 18 Augustus 2026

Vandaag de damage aangepast.

In versie 1.0 verloor de tegenstander altijd 20 HP wanneer de speler won. Dat werkte, maar voelde niet echt alsof Blackjack zelf invloed had op het gevecht.

Daarom doet de speler nu damage gelijk aan zijn score. Als ik bijvoorbeeld met 19 win, verliest de tegenstander 19 HP. Hierdoor heeft de kaartscore ook betekenis voor het fantasy-gedeelte.

De speler verliest bij een verloren hand nog steeds standaard 20 HP om het systeem eenvoudig te houden.

## 19 Augustus 2026

Tijdens het testen merkte ik dat de speler vaak al weinig HP over had na de Goblin en daardoor bijna geen kans meer had tegen de Orc of Dragon.

Om dit eerlijker te maken heb ik toegevoegd dat de Hero na het verslaan van een vijand weer volledig naar 100 HP gaat.

De vijanden worden wel steeds sterker:

- Goblin: 100 HP
- Orc: 120 HP
- Dragon: 150 HP

Dit voelt tijdens het spelen een stuk beter.

## 20 Augustus 2026

De bestaande Wins, Losses en Draws onderaan het scherm vond ik niet meer goed passen bij het nieuwe concept.

Daarom vervangen door een lijst met de drie vijanden:

`Goblin: UNDEFEATED`  
`Orc: UNDEFEATED`  
`Dragon: UNDEFEATED`

Wanneer een vijand verslagen wordt verandert zijn status naar `DEFEATED`.

Daarvoor drie eenvoudige boolean-variabelen gebruikt. Ik heb bewust geen ingewikkelder systeem gemaakt omdat deze oplossing duidelijk is en voor drie vijanden prima werkt.

## 21 Augustus 2026

Vooral getest en kleine fouten opgelost.

Een probleem was dat na het resetten van het volledige spel sommige fantasy-variabelen nog hun oude waarde hadden. Bijvoorbeeld dat de Goblin opnieuw verscheen terwijl zijn status nog op `DEFEATED` stond.

Daarom bij een volledige restart nu ook `enemy_number`, `enemy_name`, `enemy_hp` en de drie defeated-variabelen terug naar hun beginwaarde gezet.

Ook gecontroleerd of de normale Blackjack-regels nog steeds werken na alle uitbreidingen.

## 22 Augustus 2026

Laatste versie van Fantasy Blackjack getest.

De basis van de tutorial is nog steeds duidelijk herkenbaar, maar het spel heeft nu een kleine campaign gekregen waarin de Hero achtereenvolgens de Goblin, Orc en Dragon moet verslaan.

Na het verslaan van de Dragon verschijnt `KINGDOM SAVED!`.

Ik ben tevreden met de uitbreiding omdat ze relatief eenvoudig is gebleven, maar het spel toch een duidelijk ander doel heeft gekregen dan de originele Blackjack-versie. Tijdens het maken heb ik vooral meer inzicht gekregen in hoe de game-loop, globale variabelen, voorwaarden en functies samen de toestand van een game bijhouden.

## 29 Augustus 2026
Feedback van leerkracht ontvangen. 

vaste indices voor Goblin/Orc/Dragon, enemy_number → enemy_index, de drie defeated-booleans samengevoegd in één lijst, draw_enemy_status() met een loop, de herhaalde waarde 70 in draw_cards() in een variabele gezet, en de overbodige whitespace in het aangeduide if/elif-gedeelte weggehaald