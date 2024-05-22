struct Point
{
	int x;
	int y;
};

vector<Point> snake = {
	Point{ WIDTH / 2 + 2, HEIGHT / 2 },
	Point{ WIDTH / 2 + 1, HEIGHT / 2 },
	Point{ WIDTH / 2, HEIGHT / 2 },
	Point{ WIDTH / 2 - 1, HEIGHT / 2 },
	Point{ WIDTH / 2 - 2, HEIGHT / 2 }
};
void drawSnakePart(Point p)
{
	gotoxy(p.x, p.y);
	cout << BODY;
}

void drawSnake()
{
for (size_t i = 0; i < snake.size(); i++)
		drawSnakePart(snake[i]);
}
enum class Direction
 {
	up,
	right,
	down,
	left
};

Direction direction = Direction::right;
void move()
{
	for (size_t i = snake.size() - 1; i > 0; i--)
		snake[i] = snake[i - 1];
	if (direction == Direction::up)
		snake[0].y -= 1;
	else if (direction == Direction::down)
		snake[0].y += 1;
	else if (direction == Direction::left)
		snake[0].x -= 1;
	else if (direction == Direction::right)
		snake[0].x += 1;
}

