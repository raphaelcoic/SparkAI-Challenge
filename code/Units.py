from __future__ import annotations
import code.GameState as GameState


class Unit:
    """Abstract class for a unit."""

    def __init__(self, game_state : GameState, player_id: str, unit_id : str):
        self.game_state = game_state
        self.map = game_state.map
        self.player_id = player_id
        self.my_units = game_state.units[player_id]
        self.id = unit_id
        self.type = None
        self.position = self.map.base1 if player_id == 'p1' else self.map.base2
        self.speed = None
        self.max_health = None
        self.health = None
        self.spark_speed = 0
        self.cost = 0
        self.wait = 0
        self.active_effects = {}      #{effect_name: (effect_value, duration)}

        
    @property
    def is_alive(self):
        return self.health > 0


    @property
    def damage_receiver(self):
        return self.active_effects['protector'][0] if self.has_effect('protector') else self

    def get_multiplier(self, attribute : str):
        effect_name = f'{attribute}_boost'
        return self.active_effects[effect_name][0] if self.has_effect(effect_name) else 1


    def apply_boost(self, attribute : str, value : float, duration : int):
        self.active_effects[f'{attribute}_boost'] = (value, duration)


    def apply_effect(self, effect_name : str, value, duration : int = 1):
        self.active_effects[effect_name] = (value, duration)

    def has_effect(self, effect_name : str):
        if effect_name not in self.active_effects:
            return False
        value, dur = self.active_effects[effect_name]
        if dur <= 0:
            del self.active_effects[effect_name]
            return False
        return True


    def end_turn(self):
        for effect_name in list(self.active_effects):
            value, dur = self.active_effects[effect_name]
            self.active_effects[effect_name] = (value, dur - 1)
            self.has_effect(effect_name)


    def take_damage(self, amount):
        """Decreases the unit's health by amount."""
        self.damage_receiver.health -= amount


    def move(self, v):
        """Moves the unit to v if it is adjacent to it."""

        assert self.map.distance(self.position, v) <= self.speed * self.get_multiplier('speed'), "Impossible move"
        self.position = v


class Worker(Unit):
    """Class for a worker unit."""

    def __init__(self, game_state : GameState, player_id : str, unit_id : str):
        super().__init__(game_state, player_id, unit_id)
        self.max_health = 5
        self.health = self.max_health
        self.speed = 1
        self.extraction_speed = 1
        self.load = 0
        self.capacity = 3
        self.type = "worker"
        self.cost = 10


    @property
    def available_space(self):
        """Returns the number of resources available to extract."""

        return self.capacity - self.load


    def extract(self):
        """Extracts resources from the map."""

        assert self.load < self.capacity and self.map.resources(self.position) != 0, "Impossible extraction"
        available_resources = self.map.resources(self.position)
        extracted_resources = min(available_resources, self.available_space, self.extraction_speed)

        self.load += extracted_resources
        self.map.resources[self.position] -= extracted_resources


    def drop(self):
        """Drops resources on the base."""

        assert (self.position == self.map.base1 and self.player_id == 'p1') or (
                    self.position == self.map.base2 and self.player_id == 'p2'), "Drop location not allowed"
        self.map.resources[self.position] += self.load
        self.load = 0


    def give_to(self, target: Worker):
        """Gives resources to another worker."""

        assert target.type == "worker", "Target not a worker"
        assert target.position == self.position, "Target out of range"
        assert self.load > 0, "No resources to give"
        assert target.available_space > 0, "Target full"

        transferred_resources = min(self.load, target.available_space)
        self.load -= transferred_resources
        target.load += transferred_resources
        
class Minor(Worker):
    """Class for an extractor unit."""
    def __init__(self, game_state : GameState, player_id : str, unit_id : str):
        super().__init__(game_state, player_id, unit_id)
        self.subtype = "minor"
        self.speed = 1
        self.extraction_speed = 2
        self.capacity = 10
        self.cost = 10
        
        
class Transporter(Worker):
    """Class for an extractor unit."""
    def __init__(self, game_state : GameState, player_id : str, unit_id : str):
        super().__init__(game_state, player_id, unit_id)
        self.subtype = "transporter"
        self.speed = 2
        self.extraction_speed = 1
        self.capacity = 3
        self.cost = 10
    

class Army(Unit):
    """Class for an army unit."""
    def __init__(self, game_state, player_id, unit_id):
        super().__init__(game_state, player_id, unit_id)
        self.type = "army"
        self.damage = 1
        self.range = 1
        self.spark_speed = 1

    def attack(self, target: Unit):
        """Attacks the target unit."""
        
        assert self.wait == 0, "Unit is waiting"
        assert self.map.distance(self.position, target.position) <= self.range, "Target out of range"
        target.take_damage(self.damage * self.get_multiplier('damage'))
        self.wait = 1


class Corebot(Army):
    """Class for a basic fighter unit."""

    def __init__(self, game_state, player_id, unit_id):
        super().__init__(game_state, player_id, unit_id)
        self.subtype = "corebot"
        self.max_health = 5
        self.health = self.max_health
        self.speed = 1
        self.damage = 2
        self.range = 1
        self.spark_speed = 1
        self.cost = 20


class Phasor(Army):
    """Class for a longdistance unit."""

    def __init__(self, game_state, player_id, unit_id):
        super().__init__(game_state, player_id, unit_id)
        self.subtype = "phasor"
        self.max_health = 3
        self.health = self.max_health
        self.speed = 1
        self.damage = 2
        self.range = 3
        self.spark_speed = 1
        self.cost = 30
        
    def longshot(self, target: Unit):
        """Attacks the target unit with a longshot."""
        
        assert self.wait == 0, "Unit is waiting"
        assert self.map.distance(self.position, target.position) <= self.range * 2, "Target out of range"
        target.health -= self.damage * 2
        self.wait = 2
        
        
class Megacore(Army):
    """Class for a highlevel health unit."""
    
    def __init__(self, game_state, player_id, unit_id):
        super().__init__(game_state, player_id, unit_id)
        self.subtype = "megacore"
        self.max_health = 10
        self.health = self.max_health
        self.speed = 1
        self.damage = 1
        self.range = 0
        self.spark_speed = 1
        self.cost = 40

    def protect(self, target: Unit):
        """Protects the target unit from damage."""
        
        assert self.wait == 0, "Unit is waiting"
        target.apply_effect("protection", 2)
        self.wait = 3
        

class Sparker(Army):
    """Class for a spark unit."""

    def __init__(self, game_state, player_id, unit_id):
        super().__init__(game_state, player_id, unit_id)
        self.subtype = "sparker"
        self.max_health = 5
        self.health = self.max_health
        self.speed = 2
        self.damage = 1
        self.range = 1
        self.spark_speed = 2
        self.cost = 30

    def spark_burst(self):
        """Increase spark_speed of every unit around."""

        assert self.wait == 0, "Unit is waiting"
        for unit in self.game_state.units():
            if (unit.player_id == self.player_id
                    and unit.type == "army"
                    and unit.position == self.position):
                unit.apply_boost("spark", 2, 1)
        self.wait = 3
        
class Healer(Army):
    """Class for a healer unit."""
    
    def __init__(self, game_state, player_id, unit_id):
        super().__init__(game_state, player_id, unit_id)
        self.subtype = "sparker"
        self.max_health = 5
        self.health = self.max_health
        self.speed = 1
        self.damage = 1
        self.range = 1
        self.healing_range = 1
        self.healing_amount = 1
        self.spark_speed = 2
        self.cost = 100
        
    def heal(self, target: Unit):

        """Heals the target unit."""
        assert self.wait == 0, "Unit is waiting"
        assert self.map.distance(self.position, target.position) <= self.healing_range, "Target out of range"
        assert target.health < target.max_health, "Target already full life"
        target.health = min(target.health + self.healing_amount, target.max_health)
        self.wait = 1

    def heal_burst(self):
        """Heals every unit in the healing range."""

        assert self.wait == 0, "Unit is waiting"
        for unit in self.my_units:
            if (self.map.distance(self.position, unit.position) <= self.healing_range
                    and unit.health < unit.max_health):
                unit.health = min(unit.health + self.healing_amount, unit.max_health)
        self.wait = 4


class Commandant(Army):
    def __init__(self, game_state, player_id, unit_id):
        super().__init__(game_state, player_id, unit_id)
        self.subtype = "commandant"
        self.max_health = 7
        self.health = self.max_health
        self.speed = 1
        self.damage = 2
        self.range = 2
        self.spark_speed = 1
        self.cost = 100

    def boost(self, target: Army):
        """Boosts the target unit's attributes."""

        assert self.wait == 0, "Unit is waiting"
        target.apply_boost("speed", 1.5, 2)
        target.apply_boost("damage", 1.5, 2)
        self.wait = 2


    def boost_burst(self):
        """Boosts every unit around."""

        assert self.wait == 0, "Unit is waiting"
        for unit in self.my_units:
            if unit.type == "army" and unit.position == self.position:
                unit.apply_boost("speed", 1.5, 2)
                unit.apply_boost("damage", 1.5, 2)
        self.wait = 4

