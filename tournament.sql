-- The database schema for a Swiss-style tournament.

-- to reset the database during testing
DROP DATABASE IF EXISTS tournament
-- create and connect to the database using psql command line commands
CREATE DATABASE tournament;
\c tournament;

-- create the tables necessary to support a Swiss-style tournament

-- table holds player info
CREATE TABLE Player (
	PlayerID serial PRIMARY KEY,
	PlayerName vachar(50) NOT NULL,
	PlayerDOB date NOT NULL,
	PlayerEmail varchar(30)
);

-- table holds match info
CREATE TABLE Matches (
	MatchID serial PRIMARY KEY,
	Winner integer NOT NULL REFERENCES Player (PlayerID),
	WinnerPoints integer NOT NULL CHECK (WinnerPoints >= 0),
	Loser integer NOT NULL REFERENCES Player (PlayerID),
	LoserPoints integer NOT NULL CHECK (LoserPoints >= 0),
	MatchNotes text
);

-- view to calculate how many points each player scored
CREATE OR REPLACE VIEW PlayerPoints as
	SELECT Player.PlayerID, Matches.WinnerPoints as PointsScored, Matches.LoserID as Opponent 
	FROM Player LEFT JOIN Matches ON Player.PlayerID = Matches.Winner
	GROUP BY PlayerID
	UNION
	SELECT Player.PlayerID, Matches.LoserPoints as PointsScored, Matches.WinnerID as Opponent
	FROM Player LEFT JOIN Matches ON Player.PlayerID = Matches.Loser
	GROUP BY PlayerID
;

-- view to get players paired with opponents and the opponent's total wins (no duplicates)
CREATE OR REPLACE VIEW PlayerOpponents as
	SELECT Player.PlayerID,
		PlayerPoints.Opponent,
		(SELECT count(*) FROM Matches WHERE Winner in PlayerPoints.Opponent) as OpponentWins
	FROM Player LEFT JOIN PlayerPoints on Player.PlayerID = PlayerPoints.PlayerID
;

-- view to calculate tournament standings
-- the player in the top row is the leader, the player in the bottom row is in last place
-- ties in total wins are broken by strength of schedule first and total points scored second
CREATE OR REPLACE VIEW Standings as 
	SELECT Player.PlayerName,
		(SELECT count(*) FROM Matches WHERE (Winner = Player.PlayerID) OR (Loser = Player.PlayerID)) as MatchesPlayed,
		(SELECT count(*) FROM Matches WHERE Winner = Player.PlayerID) as Wins,
		(SELECT count(*) FROM Matches WHERE Loser = Player.PlayerID) as Loses,
		PlayerOpponents.OpponentWins,
		(SELECT sum(points) FROM
			(SELECT PlayerWinPoints.WinnerPoints, PlayerLossPoints.LoserPoints
				FROM 
				WHERE (Winner = Player.PlayerID) OR (Loser = Player.PlayerID)) as TotalPoints
	FROM Player
		LEFT JOIN Matches on Player.PlayerID = Matches.
		LEFT JOIN PlayerOpponentWins on Player.PlayerID = PlayerOpponents.PlayerID
		LEFT JOIN PlayerWinPoints
		LEFT JOIN PlayerLossPoints
;