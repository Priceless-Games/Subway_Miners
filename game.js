let gameState = {
    position: 1,
    obstacles: [],
    score: 0,
    level: 1,
    powerUp: false,
    turnsLeftPowerUp: 0
};

function startGame() {
    gameState = {
        position: 1,
        obstacles: [],
        score: 0,
        level: 1,
        powerUp: false,
        turnsLeftPowerUp: 0
    };
    updateGame();
}

function move(direction) {
    if (direction === 'left' && gameState.position > 1) {
        gameState.position -= 1;
    } else if (direction === 'right' && gameState.position < 3) {
        gameState.position += 1;
    }
    updateGame();
}

function jump() {
    if (gameState.obstacles.length > 0) {
        gameState.obstacles.shift();
    }
    updateGame();
}

function updateGame() {
    // Add a new obstacle or power-up with some probability
    if (Math.random() < 0.3) {
        if (Math.random() < 0.1) {
            gameState.obstacles.push('P');
        } else {
            gameState.obstacles.push(Math.floor(Math.random() * 3) + 1);
        }
    }

    // Check for collision
    if (gameState.obstacles.length > 0 && gameState.obstacles[0] == gameState.position) {
        if (gameState.powerUp) {
            gameState.obstacles.shift();
            gameState.powerUp = false;
        } else {
            alert(`Game Over! Your score: ${gameState.score}`);
            startGame();
            return;
        }
    }

    // Check for power-up collection
    if (gameState.obstacles.length > 0 && gameState.obstacles[0] === 'P') {
        gameState.powerUp = true;
        gameState.turnsLeftPowerUp = 5;
        gameState.obstacles.shift();
    }

    // Update power-up state
    if (gameState.powerUp) {
        gameState.turnsLeftPowerUp -= 1;
        if (gameState.turnsLeftPowerUp === 0) {
            gameState.powerUp = false;
        }
    }

    // Update score and level
    gameState.score += 1;
    if (gameState.score % 10 === 0) {
        gameState.level += 1;
    }

    renderGame();
}

function renderGame() {
    // Clear the grid
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            document.getElementById(`cell-${i}-${j}`).innerHTML = '';
        }
    }

    // Render the player
    document.getElementById(`cell-2-${gameState.position - 1}`).innerHTML = '🚶';

    // Render the obstacles and power-ups
    gameState.obstacles.forEach((obstacle, index) => {
        if (obstacle === 'P') {
            document.getElementById(`cell-1-${index % 3}`).innerHTML = '⭐';
        } else {
            document.getElementById(`cell-1-${obstacle - 1}`).innerHTML = '🚧';
        }
    });

    // Update game info
    document.getElementById('game-info').innerHTML = `Score: ${gameState.score}  Level: ${gameState.level}  Power-Up: ${gameState.powerUp ? 'Active' : 'Inactive'}`;
}

// Initialize the game
startGame();
