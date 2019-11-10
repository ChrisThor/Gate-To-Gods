import math


class Brezelheim:
    def __init__(self, level):
        self.brezelheimable = []
        self.reset_brezelheim(level)

    def check_distance(self, dy, dx, radius):
        if math.sqrt(dx * dx + dy * dy) <= radius:
            return True
        else:
            return False

    def brezelheim_x(self, level, error, dy, dx, y, start_y, target_y, start_x, x, radius):
        error -= dy
        if error < 0:
            if y < target_y:
                y += 1
            else:
                y -= 1
            error += dx

        if self.check_distance(y - start_y, x - start_x, radius):
            try:
                self.brezelheimable[y][x] = True
                if not level.is_visible(y, x):
                    return error, y, False
            except IndexError:
                return error, y, False
            return error, y, True
        else:
            return error, y, False

    def brezelheim_x_function(self, level, start_x, target_x, start_y, target_y, dx, dy, radius):
        error = dx / 2
        y = start_y
        if target_x >= start_x:
            for x in range(start_x + 1, target_x + 1):
                error, y, success = self.brezelheim_x(level, error, dy, dx, y, start_y, target_y, start_x, x, radius)
                if not success:
                    return False
        else:
            for x in range(start_x - 1, target_x - 1, -1):
                error, y, success = self.brezelheim_x(level, error, dy, dx, y, start_y, target_y, start_x, x, radius)
                if not success:
                    return False
        return True

    def brezelheim_y(self, level, error, dx, dy, x, start_x, target_x, start_y, y, radius):
        error -= dx
        if error < 0:
            if x < target_x:
                x += 1
            else:
                x -= 1
            error += dy

        if self.check_distance(y - start_y, x - start_x, radius):
            try:
                self.brezelheimable[y][x] = True
                if not level.is_visible(y, x):
                    return error, x, False
            except IndexError:
                return error, x, False
            return error, x, True
        else:
            return error, x, False

    def brezelheim_y_function(self, level, start_x, target_x, start_y, target_y, dx, dy, radius):
        error = dy / 2
        x = start_x
        if target_y >= start_y:
            for y in range(start_y + 1, target_y + 1):
                error, x, success = self.brezelheim_y(level, error, dx, dy, x, start_x, target_x, start_y, y, radius)
                if not success:
                    return False
        else:
            for y in range(start_y - 1, target_y - 1, -1):
                error, x, success = self.brezelheim_y(level, error, dx, dy, x, start_x, target_x, start_y, y, radius)
                if not success:
                    return False
        return True

    def draw_brezelheim(self, level, start_y, start_x, target_y, target_x, radius):
        dx = math.fabs(target_x - start_x)
        dy = math.fabs(target_y - start_y)

        try:
            self.brezelheimable[start_y][start_x] = True
        except IndexError:
            return False
        if target_x == start_x and target_y == start_y:
            return True

        if dx >= dy:
            return self.brezelheim_x_function(level, start_x, target_x, start_y, target_y, dx, dy, radius)
        else:
            return self.brezelheim_y_function(level, start_x, target_x, start_y, target_y, dx, dy, radius)

    def reset_brezelheim(self, level):
        self.brezelheimable = []
        for i in range(level.len_y):
            brezelheimable_x = []
            for j in range(level.len_x):
                brezelheimable_x.append(False)
            self.brezelheimable.append(brezelheimable_x)
