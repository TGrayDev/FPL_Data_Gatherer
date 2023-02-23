SELECT player_first_name, player_second_name, minutes, cost, form
FROM players
--Added the minutes parameter to ignore outliers (E.G player with 1 goal in 5 minutes played from a substitution, their form would be abnormally high)
WHERE minutes > 200 AND form > 5
ORDER BY cost desc ;