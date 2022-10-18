

class Team:
    def __init__(self,
                 name,
                 streak=1,
                 skill=1,
                 attack=1,
                 defense=1,
                 played=0,
                 wins=0,
                 draws=0,
                 losses=0,
                 scored=0,
                 conceeded=0,
                 points=0
                 ):

        self.name = name
        self.played = played
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.scored = scored
        self.conceeded = conceeded
        self.points = points
        self.skill = skill
        self.attack = attack
        self.defense = defense
        self.streak = streak

    def played_update(self):
        self.played = self.wins + self.draws + self.losses
        return self.played

    def won_update(self):
        self.wins += 1
        return self.wins

    def loss_update(self):
        self.losses += 1
        return self.losses

    def draw_update(self):
        self.draws += 1
        return self.draws

    def scored_update(self, goal_for):
        self.scored += goal_for
        return self.scored

    def conceeded_update(self, goal_against):
        self.conceeded += goal_against
        return self.conceeded

    def points_update(self):
        self.points = 3 * self.wins + self.draws
        return self.points

    def reset(self):
        self.__init__()


teams = []
# Number 0
teams.append(Team(
    name='Arsenal',
    skill=19.0,
    attack=17,
    defense=10
)
)
# Number 1
teams.append(Team(
    name='Aston Villa',
    skill=3,
    attack=9,
    defense=5
)
)
# Number 2
teams.append(Team(
    name='AFC Bournemouth',
    skill=4,
    attack=11,
    defense=8
)
)
# Number 3
teams.append(Team(
    name='Brentford',
    skill=17.2,
    attack=14,
    defense=10
)
)
# Number 4
teams.append(Team(
    name='Brighton and Hove',
    skill=11,
    attack=8,
    defense=8
)
)
# Number 5
teams.append(Team(
    name='Chelsea',
    skill=18.9,
    attack=18,
    defense=19
)
)
# Number 6
teams.append(Team(
    name='Crystal Palace',
    skill=9,
    attack=9,
    defense=11
)
)
# Number 7
teams.append(Team(
    name='Everton',
    skill=5,
    attack=9,
    defense=8
)
)
# Number 8
teams.append(Team(
    name='Fulham',
    skill=6,
    attack=9,
    defense=9
)
)
# Number 9
teams.append(Team(
    name='Leeds United',
    skill=10,
    attack=13,
    defense=7
)
)
# Number 10
teams.append(Team(
    name='Leicester City',
    skill=17.4,
    attack=12,
    defense=12
)
)
#Number 11
teams.append(Team(
    name='Liverpool',
    skill=19.2,
    attack=19,
    defense=19
)
)
# Number 12
teams.append(Team(
    name='Manchester City',
    skill=19.3,
    attack=21,
    defense=20,
)
)
# Number 13
teams.append(Team(
    name='Manchester United',
    skill=18.8,
    attack=14,
    defense=14
)
)
# Number 14
teams.append(Team(
    name='Newcastle United',
    skill=8,
    attack=12,
    defense=12
)
)
# Number 15
teams.append(Team(
    name='Nottingham Forest',
    skill=2,
    attack=8,
    defense=6
)
)
# Number 16
teams.append(Team(
    name='Southampton',
    skill=7,
    attack=8,
    defense=4
)
)
#Number 17
teams.append(Team(
    name='Tottenham Hotspurs',
    skill=18.95,
    attack=19,
    defense=17
)
)
# Number 18
teams.append(Team(
    name='West Ham United',
    skill=17.5,
    attack=12,
    defense=15
)
)
# Number 19
teams.append(Team(
    name='Wolverhampton Wanderers',
    skill=1,
    attack=4,
    defense=6
)
)


def match(team1, team2, score_tuple):
    if score_tuple[0] > score_tuple[1]:
        team1.won_update()
        team2.loss_update()
    elif score_tuple[0] < score_tuple[1]:
        team2.won_update()
        team1.loss_update()
    else:
        team2.draw_update()
        team1.draw_update()

    team1.played_update()
    team2.played_update()
    team1.scored_update(score_tuple[0])
    team2.scored_update(score_tuple[1])
    team2.conceeded_update(score_tuple[0])
    team1.conceeded_update(score_tuple[1])
    team1.points_update()
    team2.points_update()
