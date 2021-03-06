#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def testDelete():
    """Test if deletion from tables works"""
    deleteEverything()
    print "1. All matches, registrations, tournaments, and " \
        "players can be deleted."


def testCount():
    """Test if count returns numeric type 0 for empty tables"""
    deleteEverything()
    cM = countAllMatches()
    cR = countAllRegistrations()
    cT = countAllTournaments()
    cP = countAllPlayers()
    if cM == '0' or cR == '0' or cT == '0' or cP == '0':
        raise TypeError(
            "Counts should return numeric zero, not string '0'.")
    if cM != 0 or cR != 0 or cT != 0 or cP != 0:
        raise ValueError("After deleting, counts should return zero.")
    print "2. After deleting, all counts return zero."


def testCreatePlayer():
    """Test if player records can be created"""
    deleteEverything()
    createPlayerRecord("Chandra Nalaar")
    c = countAllPlayers()
    if c != 1:
        raise ValueError(
            "After creating one player record, count of players should be 1.")
    print "3. After creating one player record, count of players returns 1."


def testCreateTournament():
    """Test if tournaments can be created"""
    deleteEverything()
    createTournament("Fencing")
    c = countAllTournaments()
    if c != 1:
        raise ValueError(
            "After creating one tournament, count of tournaments should be 1.")
    print "4. After creating one tournament, count of tournaments returns 1."


def testRegister():
    """Test if players can be registered to different tournaments"""
    deleteEverything()
    createPlayerRecords(["Chandra Nalaar", "Ned Flanders"])
    createTournaments(["Fencing", "Ping Pong"])
    playerIDs = [int(row[0]) for row in getPlayerBios()]
    tIDs = [int(row[0]) for row in getTournamentInfo()]
    registerPlayer(playerIDs[0], tIDs[0])
    registerPlayer(playerIDs[1], tIDs[0])
    registerPlayer(playerIDs[0], tIDs[1])
    cTotal = countAllRegistrations()
    cFence = countRegistrations(tIDs[0])
    cPing = countRegistrations(tIDs[1])
    if cTotal != 3 or cFence != 2 or cPing != 1:
        raise ValueError(
            "Incorrect registrations after multiple players " \
            "register for multiple tournaments.")
    print "5. After multiple players register for multiple tournaments, " \
          "count of registrations is correct."


def testRegisterCountDeleteCount():
    """Test table counts after registration and then deletion"""
    deleteEverything()
    createPlayerRecords(["Markov Chaney", "Joe Malik",
                        "Mao Tsu-hsi", "Atlanta Hope"])
    createTournaments(["Fencing", "Ping Pong"])
    playerIDs = [int(row[0]) for row in getPlayerBios()]
    tIDs = [int(row[0]) for row in getTournamentInfo()]
    registerAll(playerIDs, tIDs)
    cPlayers = countAllPlayers()
    cRegistrations = countAllRegistrations()
    cFencing = countRegistrations(tIDs[0])
    cPing = countRegistrations(tIDs[1])
    cTourn = countAllTournaments()
    if (cPlayers != 4 or cRegistrations != 8 or 
        cFencing != 4 or cPing != 4 or cTourn != 2):
        raise ValueError(
            "After registering four players for two tournaments, " \
            "counts are wrong.")
    deleteEverything()
    cPlayers = countAllPlayers()
    cRegistrations = countAllRegistrations()
    cTourn = countAllTournaments()
    if cPlayers != 0 or cRegistrations != 0 or cTourn != 0:
        raise ValueError("After deleting, counts should return zero.")
    print "6. Players can be registered and deleted."


def testStandingsBeforeMatches():
    """Test whether standings show players with no matches"""
    deleteEverything()
    createPlayerRecords(["Melpomene Murray", "Randy Schwartz"])
    createTournaments(["Fencing", "Ping Pong"])
    playerIDs = [int(row[0]) for row in getPlayerBios()]
    tIDs = [int(row[0]) for row in getTournamentInfo()]
    registerAll(playerIDs, tIDs)
    standings = allStandings()
    if len(standings) < 4:
        raise ValueError("Players should appear in standings for a " \
                         "tournament even if they have not played any " \
                         "matches in that tournament.")
    elif len(standings) > 4:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 7:
        raise ValueError("Each standings row should have seven columns.")
    [(tourn1, id1, name1, wins1, matches1, stren1, points1),
     (tourn1, id2, name2, wins2, matches2, stren2, points2),
     (tourn2, id3, name3, wins3, matches3, stren3, points3),
     (tourn2, id3, name4, wins4, matches4, stren4, points4)] = standings
    if ( matches1 != 0 or matches2 != 0 or matches3 != 0 or matches4 != 0 or
         wins1 != 0 or wins2 != 0 or wins3 != 0 or wins4 != 0 or
         stren1 != 0 or stren2 != 0 or stren3 != 0 or stren4 != 0 or
         points1 != 0 or points2 != 0 or points3 != 0 or points4 != 0):
        raise ValueError(
            "Newly registered players should have no matches, " \
            "wins, strength of schedule, or points.")
    if tourn1 != tIDs[0] or tourn2 != tIDs[1]:
        raise ValueError("Standings do not list correct tournament.")
    if ( set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]) or 
         set([name3, name4]) != set(["Melpomene Murray", "Randy Schwartz"]) ):
        raise ValueError("Registered players' names should appear in " \
                         "standings even if they have no matches played.")
    print "7. Newly registered players appear in standings with no matches."


def testReportMatches():
    """Test if recording matches causes correct changes to standings."""
    deleteEverything()
    createPlayerRecords(["Bruno Walton", "Boots O'Neal",
                        "Cathy Burton", "Diane Grant"])
    createTournaments(["Fencing", "Ping Pong"])
    playerIDs = [int(row[0]) for row in getPlayerBios()]
    tIDs = [int(row[0]) for row in getTournamentInfo()]
    registerAll(playerIDs, tIDs)
    standingsOne = tournamentStandings(tIDs[0])
    standingsTwo = tournamentStandings(tIDs[1])
    [id1, id2, id3, id4] = [row[0] for row in standingsOne]
    [id5, id6, id7, id8] = [row[0] for row in standingsTwo]
    reportMatch(tIDs[0], id1, 3, id2, 2, False)
    reportMatch(tIDs[0], id3, 5, id4, 1, False)
    reportMatch(tIDs[1], id5, 2, id6, 1, False)
    reportMatch(tIDs[1], id7, 4, id8, 0, False)
    standings = allStandings()
    i = 0
    while i < 4:
        if standings[i][0] != tIDs[0]:
            raise ValueError("TournmentIDs is not correct in standings.")
        i+=1
    while i < 8:
        if standings[i][0] != tIDs[1]:
            raise ValueError("TournmentIDs is not correct in standings.")
        i+=1
    standingsOne = tournamentStandings(tIDs[0])
    standingsTwo = tournamentStandings(tIDs[1])
    for (i, n, w, m, s, p) in standingsOne:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each winner should have one win recorded.")
        if i in (id2, id4) and w != 0:
            raise ValueError("Each loser should have zero wins recorded.")
        if ( (i == id1 and p != 3) or
             (i == id2 and p != 2) or
             (i == id3 and p != 5) or
             (i == id4 and p != 1) ):
            raise ValueError("A player in the first tournament " \
                             "has the wrong number of total points.")
        if i in (id1, id3) and s != 0:
            raise ValueError("Winners' strength of schedule should be 0")
        if i in (id2, id4) and s != 1:
            raise ValueError("Losers' strength of schedule should be 1")   
    for (i, n, w, m, s, p) in standingsTwo:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id5, id7) and w != 1:
            raise ValueError("Each winner should have one win recorded.")
        if i in (id6, id8) and w != 0:
            raise ValueError("Each loser should have zero wins recorded.")
        if ( (i == id1 and p != 2) or
             (i == id2 and p != 1) or
             (i == id3 and p != 4) or
             (i == id4 and p != 0) ):
            raise ValueError("A player in the second tournament " \
                             "has the wrong number of total points.")
        if i in (id1, id3) and s != 0:
            raise ValueError("Winners' strength of schedule should be 0")
        if i in (id2, id4) and s != 1:
            raise ValueError("Losers' strength of schedule should be 1")   
    print "8. After a round of matches in two tournaments, " \
          "players standings are correct and count of matches is correct."


def testPairings():
    """Test if pairing algorithm works for multiple tournaments"""
    deleteEverything()
    createPlayerRecords(["Twilight Sparkle", "Fluttershy",
                         "Applejack", "Pinkie Pie"])
    createTournaments(["Fencing", "Ping Pong"])
    playerIDs = [int(row[0]) for row in getPlayerBios()]
    tIDs = [int(row[0]) for row in getTournamentInfo()]
    registerAll(playerIDs, tIDs)
    standingsOne = tournamentStandings(tIDs[0])
    standingsTwo = tournamentStandings(tIDs[1])
    [Rid1, Rid2, Rid3, Rid4] = [row[0] for row in standingsOne]
    [Rid5, Rid6, Rid7, Rid8] = [row[0] for row in standingsTwo]
    reportMatch(tIDs[0], Rid1, 2, Rid2, 0, False)
    reportMatch(tIDs[0], Rid3, 3, Rid4, 2, False)
    reportMatch(tIDs[1], Rid6, 1, Rid5, 0, False)
    reportMatch(tIDs[1], Rid8, 2, Rid7, 1, False)
    pairingsOne = swissPairings(tIDs[0])
    pairingsTwo = swissPairings(tIDs[1])
    if len(pairingsOne) != 2 or len(pairingsTwo) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(Pid1, Pname1, Pid2, Pname2), (Pid3, Pname3, Pid4, Pname4)] = pairingsOne
    [(Pid5, Pname5, Pid6, Pname6), (Pid7, Pname7, Pid8, Pname8)] = pairingsTwo
    correctPairsOne = set([frozenset([Rid1, Rid3]), frozenset([Rid2, Rid4])])
    actualPairsOne = set([frozenset([Pid1, Pid2]), frozenset([Pid3, Pid4])])
    correctPairsTwo = set([frozenset([Rid6, Rid8]), frozenset([Rid5, Rid7])])
    actualPairsTwo = set([frozenset([Pid5, Pid6]), frozenset([Pid7, Pid8])])
    if ( correctPairsOne != actualPairsOne or
         correctPairsTwo != actualPairsTwo ):
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "9. After one round in two tournaments, pairs are correct."

def testOddNumberPlayers():
    """Test if pairing algorithm handles multiple odd # player tournaments"""
    deleteEverything()
    createPlayerRecords(["Twilight Sparkle", "Fluttershy", "Applejack"])
    createTournaments(["Fencing", "Ping Pong"])
    playerIDs = [int(row[0]) for row in getPlayerBios()]
    tIDs = [int(row[0]) for row in getTournamentInfo()]
    registerAll(playerIDs, tIDs)
    pairingsOne = swissPairings(tIDs[0])
    pairingsTwo = swissPairings(tIDs[1])
    [(Pid1, Pid2), (Pid3, Pid4)] = [(row[0],row[2]) for row in pairingsOne]
    [(Pid5, Pid6), (Pid7, Pid8)] = [(row[0],row[2]) for row in pairingsTwo]
    if ( pairingsOne[0][2] != None or
         pairingsOne[0][1] != 'Twilight Sparkle' or
         pairingsTwo[0][2] != None or
         pairingsTwo[0][1] != 'Twilight Sparkle' ):
        raise ValueError(
            "The first registered player in a tournament should get a bye " \
            "in the first round if there is an odd number of players in " \
            "that tournament")
    print "10. With an odd number of players, the first registered player " \
          "in a tournament gets a bye in the first round."
    reportMatch(tIDs[0], Pid1, 0, Pid2, 0, False)
    reportMatch(tIDs[0], Pid3, 1, Pid4, 0, False)
    reportMatch(tIDs[1], Pid5, 0, Pid6, 0, False)
    reportMatch(tIDs[1], Pid7, 1, Pid8, 0, False)
    pairingsOne = swissPairings(tIDs[0])
    pairingsTwo = swissPairings(tIDs[1])
    [(Pid1, Pid2), (Pid3, Pid4)] = [(row[0],row[2]) for row in pairingsOne]
    [(Pid5, Pid6), (Pid7, Pid8)] = [(row[0],row[2]) for row in pairingsTwo]
    if ( pairingsOne[0][2] != None or
         pairingsOne[0][1] != 'Fluttershy' or
         pairingsTwo[0][2] != None or
         pairingsTwo[0][1] != 'Fluttershy' ):
        raise ValueError(
            "An incorrect player got a bye in the second round")
    print "11. The correct player got a bye in the second round " \
          "of each tournament."
    reportMatch(tIDs[0], Pid1, 0, Pid2, 0, False)
    reportMatch(tIDs[0], Pid3, 3, Pid4, 0, False)
    reportMatch(tIDs[1], Pid5, 0, Pid6, 0, False)
    reportMatch(tIDs[1], Pid7, 3, Pid8, 0, False)
    pairingsOne = swissPairings(tIDs[0])
    pairingsTwo = swissPairings(tIDs[1])
    [(Pid1, Pid2), (Pid3, Pid4)] = [(row[0],row[2]) for row in pairingsOne]
    [(Pid5, Pid6), (Pid7, Pid8)] = [(row[0],row[2]) for row in pairingsTwo]
    if ( pairingsOne[0][2] != None or
         pairingsOne[0][1] != 'Applejack' or
         pairingsTwo[0][2] != None or
         pairingsTwo[0][1] != 'Applejack' ):
        raise ValueError(
            "A player got more than one bye")
    print "12. No players got more than one bye in either tournament."


def testTies():
    """Test if pairings and standings for multiple tournies work with ties"""
    deleteEverything()
    createPlayerRecords(["Bruno Walton", "Boots O'Neal",
                         "Cathy Burton", "Diane Grant"])
    createTournaments(["Fencing", "Ping Pong"])
    playerIDs = [int(row[0]) for row in getPlayerBios()]
    tIDs = [int(row[0]) for row in getTournamentInfo()]
    registerAll(playerIDs, tIDs)
    standingsOne = tournamentStandings(tIDs[0])
    standingsTwo = tournamentStandings(tIDs[1])
    [id1, id2, id3, id4] = [row[0] for row in standingsOne]
    [id5, id6, id7, id8] = [row[0] for row in standingsTwo]
    reportMatch(tIDs[0], id1, 3, id2, 2, False)
    reportMatch(tIDs[0], id3, 4, id4, 4, True)
    reportMatch(tIDs[1], id5, 2, id6, 1, False)
    reportMatch(tIDs[1], id7, 3, id8, 3, True)
    standings = allStandings()
    for (t, i, n, w, m, s, p) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i == id1 and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        if i in (id2, id3, id4) and w != 0:
            raise ValueError("Players that did not win should have zero wins.")
        if ( (i == id1 and p != 3 and t != 1) or
             (i == id2 and p != 2 and t != 1) or
             (i == id3 and p != 4 and t != 1) or
             (i == id4 and p != 4 and t != 1) or
             (i == id5 and p != 2 and t != 2) or
             (i == id6 and p != 1 and t != 2) or
             (i == id7 and p != 3 and t != 2) or
             (i == id8 and p != 3 and t != 2) ):
            raise ValueError("A player has the wrong number of total points.")
        if i in (id1, id3, id4, id5, id7, id8) and s != 0:
            raise ValueError("Non-losers' strength of schedule should be 0")
        if i in (id2, id6) and s != 1:
            raise ValueError("Loser's strength of schedule should be 1")   
    print "13. After a round with ties in multiple tournaments, " \
          "all tournament standings are correct."


def testTieBreaks():
    """Test if tie breakers work properly"""
    deleteEverything()
    createPlayerRecords(["Twilight Sparkle", "Fluttershy",
                         "Applejack", "Thor"])
    createTournaments(["Fencing", "Ping Pong"])
    playerIDs = [int(row[0]) for row in getPlayerBios()]
    tIDs = [int(row[0]) for row in getTournamentInfo()]
    registerAll(playerIDs, tIDs)
    pairingsOne = swissPairings(tIDs[0])
    pairingsTwo = swissPairings(tIDs[1])
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairingsOne]
    [(id5, id6), (id7, id8)] = [(row[0],row[2]) for row in pairingsTwo]
    reportMatch(tIDs[0], id1, 4, id2, 2, False)
    reportMatch(tIDs[0], id3, 5, id4, 1, False)
    reportMatch(tIDs[1], id5, 5, id6, 3, False)
    reportMatch(tIDs[1], id7, 6, id8, 2, False)
    # After one round of tournament 1:
    # 1. Applejack  1 wins, 0 SOS,  5 pts, ID 3
    # 2. Twilight   1 wins, 0 SOS,  4 pts, ID 1
    # 3. Fluttershy 0 wins, 1 SOS,  2 pts, ID 2
    # 4. Thor       0 wins, 1 SOS,  1 pts, ID 4
    # After one round of tournament 2:
    # 1. Applejack  1 wins, 0 SOS,  6 pts, ID 7
    # 2. Twilight   1 wins, 0 SOS,  5 pts, ID 5
    # 3. Fluttershy 0 wins, 1 SOS,  3 pts, ID 6
    # 4. Thor       0 wins, 1 SOS,  2 pts, ID 8
    standings = allStandings()
    position = [row[2] for row in standings]
    if ( position[0] != 'Applejack' or
         position[1] != 'Twilight Sparkle' or
         position[2] != 'Fluttershy' or
         position[3] != 'Thor' or
         position[4] != 'Applejack' or
         position[5] != 'Twilight Sparkle' or
         position[6] != 'Fluttershy' or
         position[7] != 'Thor' ):
        raise ValueError("Points did not break tie correctly")
    pairingsOne = swissPairings(tIDs[0])
    pairingsTwo = swissPairings(tIDs[1])
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairingsOne]
    [(id5, id6), (id7, id8)] = [(row[0],row[2]) for row in pairingsTwo]
    reportMatch(tIDs[0], id1, 3, id2, 3, True)
    reportMatch(tIDs[0], id3, 2, id4, 1, False)
    reportMatch(tIDs[1], id5, 4, id6, 4, True)
    reportMatch(tIDs[1], id7, 3, id8, 2, False)
    # After two rounds of tournament 1:
    # 1. Twilight   1 wins,  2 SOS,  7 pts, ID 1
    # 2. Applejack  1 wins,  1 SOS,  8 pts, ID 3
    # 3. Fluttershy 1 wins,  1 SOS,  4 pts, ID 2
    # 4. Thor       0 wins,  2 SOS,  2 pts, ID 4
    # After two rounds of tournament 2:
    # 1. Twilight   1 wins,  2 SOS,  9 pts,  ID 5
    # 2. Applejack  1 wins,  1 SOS,  10 pts, ID 7
    # 3. Fluttershy 1 wins,  1 SOS,  6 pts,  ID 6
    # 4. Thor       0 wins,  2 SOS,  4 pts,  ID 8
    standings = allStandings()
    position = [row[2] for row in standings]
    if ( position[0] != 'Twilight Sparkle' or
         position[1] != 'Applejack' or
         position[2] != 'Fluttershy' or
         position[3] != 'Thor' or
         position[4] != 'Twilight Sparkle' or
         position[5] != 'Applejack' or
         position[6] != 'Fluttershy' or
         position[7] != 'Thor' ):
        raise ValueError("Strength of schedule did not break tie correctly")
    pairingsOne = swissPairings(tIDs[0])
    pairingsTwo = swissPairings(tIDs[1])
    [(id1, id2), (id3, id4)] = [(row[0],row[2]) for row in pairingsOne]
    [(id5, id6), (id7, id8)] = [(row[0],row[2]) for row in pairingsTwo]
    reportMatch(tIDs[0], id2, 7, id1, 0, False)
    reportMatch(tIDs[0], id4, 2, id3, 1, False)
    reportMatch(tIDs[1], id6, 8, id5, 1, False)
    reportMatch(tIDs[1], id8, 3, id7, 2, False)
    # After three rounds of tournament 1:
    # 1. Fluttershy 2 win,  3 SOS,  6 pts, ID 2
    # 2. Applejack  1 win,  4 SOS,  9 pts, ID 3
    # 3. Thor       1 win,  4 SOS,  9 pts, ID 4
    # 4. Twilight   1 win,  4 SOS,  7 pts, ID 1
    # After three rounds of tournament 2:
    # 1. Fluttershy 2 win,  3 SOS,  9 pts,  ID 6
    # 2. Applejack  1 win,  4 SOS,  12 pts, ID 7
    # 3. Thor       1 win,  4 SOS,  12 pts, ID 8
    # 4. Twilight   1 win,  4 SOS,  10 pts, ID 5
    standings = allStandings()
    position = [row[2] for row in standings]
    if ( position[0] != 'Fluttershy' or
         position[1] != 'Applejack' or
         position[2] != 'Thor' or
         position[3] != 'Twilight Sparkle' or
         position[4] != 'Fluttershy' or
         position[5] != 'Applejack' or
         position[6] != 'Thor' or
         position[7] != 'Twilight Sparkle' ):
        raise ValueError("PlayerID did not break tie correctly")
    print "14. After three rounds of multiple tournaments, including at " \
          "least one tie in each tournament and a three-way tie for second " \
          "place in each tournament, all tie-breakers work properly."


def deleteEverything():
    """Helper method for deleting all records from the database"""
    deleteAllMatches()
    deleteAllRegistrations()
    deleteAllTournaments()
    deleteAllPlayers()


if __name__ == '__main__':
    testDelete()
    testCount()
    testCreatePlayer()
    testCreateTournament()
    testRegister()
    testRegisterCountDeleteCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testOddNumberPlayers()
    testTies()
    testTieBreaks()
    print "Success!  All tests pass!"

