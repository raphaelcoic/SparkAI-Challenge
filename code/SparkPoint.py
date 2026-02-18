
class SparkPoint:
    """Represents a Spark Point."""
    def __init__(self, game_state, spark_point_id, position):
        self.game_state = game_state
        self.map = game_state.map
        self.units = game_state.units
        self.id = spark_point_id
        self.position = position
        self.value = 0


    @property
    def owner(self, value_required = 100):
        """Returns the player that owns this spark point."""

        return 'p1' if self.value == value_required else 'p2' if self.value == -value_required else None
        

    def is_occupied_by(self, player_id):
        """ Check if there is a unit controlled by a specific player at this spark point."""
        
        for unit in self.units:
            if unit.position == self.position and unit.player_id == player_id:
                return True
        return False


    @property
    def is_in_conflict(self):
        return self.is_occupied_by('p1') and self.is_occupied_by('p2')


    def update_value(self):
        for unit in self.units:
            if self.position == unit.position :
                if unit.player_id == 'p1':
                    self.value += unit.spark_speed * unit.get_multiplier('spark')
                else:
                    self.value -= unit.spark_speed * unit.get_multiplier('spark')


    def update_score(self, score = 1):
        self.update_value()
        if not self.is_in_conflict and self.is_occupied_by(self.owner):
            self.game_state.add_score(self.owner, score)


