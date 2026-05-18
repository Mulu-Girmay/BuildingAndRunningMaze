self.east_wall[r1][c1] = 0  # Remove east wall of current
    
    def _choose_start_end(self):
        """Choose start and end positions (can be interior or edges)"""
        if self.config.start_end_type == 'edges':
            # Classic: Left edge to right edge
            self.start = (random.randint(0, self.rows - 1), 0)
            self.end = (random.randint(0, self.rows - 1), self.cols - 1)
            
            # Create openings on edges
            if self.start[0] > 0:
                self.north_wall[self.start[0]][0] = 0
            if self.end[0] < self.rows - 1:
                self.north_wall[self.end[0] + 1][self.end[1]] = 0
        
        elif self.config.start_end_type == 'interior':
            # Challenging: Both inside the maze
            self.start = (
                random.randint(1, self.rows - 2),
                random.randint(1, self.cols - 2)
            )
            self.end = (
                random.randint(1, self.rows - 2),
                random.randint(1, self.cols - 2)
            )
            
            # Ensure start != end
            while self.start == self.end:
                self.end = (
                    random.randint(1, self.rows - 2),
                    random.randint(1, self.cols - 2)
                )
            
            # Create openings for interior cells
            self._create_openings_at_start_end()
              def _create_openings_at_start_end(self):
        """Break walls to allow entry/exit from interior positions"""
        directions = ['north', 'south', 'east', 'west']
        
        # For start
        for direction in random.sample(directions, 1):
            self._break_wall_at(self.start[0], self.start[1], direction)
        
        # For end
        for direction in random.sample(directions, 1):
            self._break_wall_at(self.end[0], self.end[1], direction)

 def _break_wall_at(self, row, col, direction):
        """Break a specific wall at a cell"""
        if direction == 'north' and row > 0:
            self.north_wall[row][col] = 0
        elif direction == 'south' and row < self.rows - 1:
            self.north_wall[row + 1][col] = 0
        elif direction == 'west' and col > 0:
            self.east_wall[row][col - 1] = 0
        elif direction == 'east' and col < self.cols - 1:
            self.east_wall[row][col] = 0
      def _add_cycles(self, probability=0.05):
        """
        BONUS: Randomly eat extra walls to create cycles
        1 in 20 chance (5%) to create cycles that break the shoulder-to-wall rule
        """
        cycles_created = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                if random.random() < probability:
                    # Try to eat north wall
                    if row > 0 and self.north_wall[row][col] == 1:
                        self.north_wall[row][col] = 0
                        cycles_created += 1
                    # Try to eat east wall
                    elif col < self.cols - 1 and self.east_wall[row][col] == 1:
                        self.east_wall[row][col] = 0
                        cycles_created += 1
        
        print(f"[Generator] Created {cycles_created} cycles (extra walls eaten)")
