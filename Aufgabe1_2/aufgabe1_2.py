import decimal
print('Uebungsblatt 1, Aufgabe 2')
budget = 1000000
cost = 50 + 50
ASICS = budget/cost
keypersecond = 5*10**8
print('Anzahl von Einheiten/ASICS: ' + str(ASICS))
print('(bei Budget in Höhe von 1 Mio. und 100 Euro an Kosten je ASIC)')
print('')
keylengths = [40, 56, 64, 88, 112, 128]
print('Dauer fuer Entschluesselungen fuer Schluessel:')
print('')
print('Minimal Schluessel-Suchzeit: erster Versuch erfolgreich:')
print('1 Sekunde geteilt durch 5 * 10^8')
print(1 / keypersecond, "oder: 0,0000000002 Sekunden");
print('')

for key in keylengths: #Alle Schluessellaengen werden durchlaufen
	print('Schluesselstarke ', key, 'Bit:');
	print('Durchschnittliche Schluesselsuchzeit:')
	print('Berechnung: (2^', key, '/5 * 10^8/10.000)/2')
	keylength = 2**key #schluessellaenge in Bit
	result = (keylength/keypersecond/ASICS)/2 #Ergebnis in sekunden
	print('Ergebnis: ', result, "Sekunden")
	if result > 3600: #if Abfrage fuer Stunden
		print('Das sind ', result/3600, 'Stunden.')
	print('')

	print('Maximale Schluesselsuchzeit:')
	print('Berechnung: 2^', key, '/5 * 10^8/10.000')
	resultmax = keylength/keypersecond/ASICS #Ergebnis von Maxschluesselsuchzeit
	print('Ergebnis: ', resultmax, "Sekunden")
	if resultmax > 3600:
		print('Das sind ', resultmax/3600, 'Stunden.')
	if resultmax > (3600*24*360) :
		print('Das sind ', resultmax/(3600*24*360), 'Jahre.')
	print('-------------------------------------------')
print('')
print('Bauen einer Suchmaschine mit Suchzeit von 24 Stunden:')
print('Moorsches Law: Verdoppelung von Transistoren auf gleicher Fläche alle 2 Jahre')
print('24 Stunden entsprechen', 24 * 3600, 'Sekunden')
print('1 Mrd. Euro entsprechen 10.000.000 ASICS')
print('Folgende Gleichung sollte somit gelöst werden:')
print('2^128 / (5 * 10^8 * 10.000.000 * 2^(x/2) * 2) = 864000, also:')
print('x = (log(2^128 / (5 * 10^15 * 86400 * 2))) * 2 / log(2)')
print('Dann sind x = 117 Jahre')

# 1 Mrd € und nur 24h Zeit. Wann ist das möglich?

# 24h entsprechen 86400s
# 1 Mrd € entsprechen 10.000.000 ASICs
# Moore's Law = Anzahl der Transistoren auf gleicher Fläche verdoppelt sich alle
# 2 Jahre

# 2^128 / (5 * 10^8 * 10.000.000 * 2^(x/2) * 2) = 864000
# verschl. startgeschw. einheiten x=jahre durchschnittliche zeit

# 2^128 / (5 * 10^15 * 2^(x/2) * 2) = 86400 | *2^(x/2); /86400
# 2^128 / (5 * 10^15 * 86400 * 2) = 2^(x/2) | log
# log(2^128 / (5 * 10^15 * 86400 * 2)) = x/2 * log(2) | /log(2); *2
# (log(2^128 / (5 * 10^15 * 86400 * 2))) * 2 / log(2) = x
# x = 116,9 y -> 117 y
