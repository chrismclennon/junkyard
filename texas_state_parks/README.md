# Texas State Parks Reservation Notifier

A super simple script that will check the Texas State Parks site every minute and send a text when a reservation is open.

Needs [PopcornNotify](https://popcornnotify.com/) for SMS.

Do a search on the [Texas State Parks](https://texasstateparks.reserveamerica.com/) site until you get the page showing the current two weeks of availability. Open Chrome Developer Console, in the Network tab, "Copy as cURL" the POST request to `deDetails.do` and paste it in the appropriate variable.

