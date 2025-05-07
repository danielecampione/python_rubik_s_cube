# Importazione delle librerie necessarie per li calcoli matematici e per la rappresentazione vettoriale
# Come lo savio geometra che misura con somma diligenza, così noi qui invochiamo gli strumenti dell'arte matematica
import math
from vpython import vector

# Funzione che converte un asse e un angolo in un quaternione, secondo l'arte della geometria spaziale
# Come Euclide nelle sue dottrine insegnava, così qui trasformiamo lo movimento rotatorio in numeri quaternali
def quaternion_from_axis_angle(axis, angle):
    # Dimezziamo l'angolo, ché così vuole la scienza de' quaternioni
    half_angle = angle * 0.5
    # Calcoliamo lo seno dell'angolo dimezzato, come insegnava Tolomeo nelle sue tavole
    s = math.sin(half_angle)
    # Restituiamo le quattro parti del quaternione, tre per la direzione e una per la rotazione
    # Come l'anima ha quattro virtù, così il quaternione ha quattro componenti
    return (axis.x * s, axis.y * s, axis.z * s, math.cos(half_angle))

# Funzione che dalla quaternale rappresentazione ritorna all'asse e all'angolo
# Come l'alchimista che dalla materia composta ritorna agli elementi primi
def quaternion_to_axis_angle(q):
    # Ricaviamo l'angolo dal coseno presente nella quarta parte del quaternione
    # E lo raddoppiamo, ché prima l'avevamo dimezzato
    angle = 2 * math.acos(q[3])
    # Calcoliamo la radice del complemento a uno del quadrato della parte scalare
    # Come insegna Pitagora nel suo teorema immortale
    s = math.sqrt(1 - q[3]*q[3])
    # Se lo denominatore è troppo piccolo, evitasi la divisione per numero quasi nullo
    # Ché sarebbe come navigare in acque troppo basse, periglioso e incerto
    if s < 0.001:
        return (vector(1,0,0), 0)
    # Restituiamo l'asse normalizzato e l'angolo di rotazione
    # Come il nocchiero che indica la rotta e la distanza da percorrere
    return (vector(q[0]/s, q[1]/s, q[2]/s), angle)

# Funzione per l'interpolazione sferica tra due quaternioni, detta SLERP
# Come il savio astronomo che calcola il moto dei corpi celesti tra due posizioni
def slerp(q1, q2, t):
    # Calcoliamo il prodotto scalare tra li due quaternioni
    # Come misurasi la similitudine tra due cose
    dot = q1[0]*q2[0] + q1[1]*q2[1] + q1[2]*q2[2] + q1[3]*q2[3]
    # Se il prodotto è negativo, invertiamo uno dei quaternioni
    # Ché vi sono sempre due cammini sulla sfera, e noi cerchiamo il più breve
    if dot < 0.0:
        q2 = (-q2[0], -q2[1], -q2[2], -q2[3])
        dot = -dot
    
    # Se li quaternioni sono quasi paralleli, usiamo l'interpolazione lineare
    # Come quando due stelle appaiono così vicine che sembrano una sola
    if dot > 0.9995:
        result = (
            q1[0] + t*(q2[0] - q1[0]),
            q1[1] + t*(q2[1] - q1[1]),
            q1[2] + t*(q2[2] - q1[2]),
            q1[3] + t*(q2[3] - q1[3])
        )
        # Normalizziamo il risultato per mantenerlo sulla sfera unitaria
        # Come il navigatore che corregge la rotta per rimanere sulla circonferenza
        return normalize(result)
    
    # Calcoliamo l'angolo tra i quaternioni e il suo seno
    # Come l'arco che separa due punti sulla sfera celeste
    theta_0 = math.acos(dot)
    sin_theta_0 = math.sin(theta_0)
    # Calcoliamo l'angolo interpolato e il suo seno
    # Come chi misura una porzione dell'arco secondo la proporzione richiesta
    theta = theta_0 * t
    sin_theta = math.sin(theta)
    
    # Calcoliamo i coefficienti per l'interpolazione
    # Come il pittore che mescola i colori nelle giuste proporzioni
    s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
    s1 = sin_theta / sin_theta_0
    
    # Restituiamo il quaternione interpolato
    # Come la posizione d'un astro tra due osservazioni
    return (
        s0*q1[0] + s1*q2[0],
        s0*q1[1] + s1*q2[1],
        s0*q1[2] + s1*q2[2],
        s0*q1[3] + s1*q2[3]
    )

# Funzione che normalizza un quaternione, riducendolo alla misura unitaria
# Come il saggio che riduce ogni cosa alla sua essenza più pura
def normalize(q):
    # Calcoliamo la lunghezza del quaternione secondo la formula pitagorica
    # Come misurasi la diagonale d'un quadrilatero nello spazio a quattro dimensioni
    length = math.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)
    # Dividiamo ciascuna componente per la lunghezza, ottenendo un quaternione unitario
    # Come l'orafo che purifica l'oro fino alla massima caratura
    return (q[0]/length, q[1]/length, q[2]/length, q[3]/length)