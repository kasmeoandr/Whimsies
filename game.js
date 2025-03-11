// Game variables
const player = document.getElementById('player');
const gameContainer = document.getElementById('game-container');
const scoreElement = document.getElementById('score');
const gameOverScreen = document.getElementById('game-over');
const finalScoreElement = document.getElementById('final-score');
const restartButton = document.getElementById('restart-button');
const leftBtn = document.getElementById('left-btn');
const rightBtn = document.getElementById('right-btn');
const jumpBtn = document.getElementById('jump-btn');
const orientationMessage = document.getElementById('orientation-message');
const continueAnywayBtn = document.getElementById('continue-anyway');

let playerX = 100;
let playerY = 200;
let velocityX = 0;
let velocityY = 0;
let score = 0;
let platforms = [];
let collectibles = [];
let clouds = [];
let isJumping = false;
let gravity = 0.5;
let gameRunning = true;
let lastDirection = 'right';
let gameScale = 1;
let gameWidth = 800;
let gameHeight = 600;

// Key states
const keys = {
    left: false,
    right: false,
    up: false
};

// Continue anyway button
continueAnywayBtn.addEventListener('click', () => {
    orientationMessage.style.display = 'none';
    gameContainer.style.display = 'block';
});

// Event listeners for keyboard
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') keys.left = true;
    if (e.key === 'ArrowRight') keys.right = true;
    if (e.key === ' ' || e.key === 'ArrowUp') keys.up = true;
    
    // Prevent scrolling with space and arrow keys
    if(['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].indexOf(e.code) > -1) {
        e.preventDefault();
    }
});

document.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowLeft') keys.left = false;
    if (e.key === 'ArrowRight') keys.right = false;
    if (e.key === ' ' || e.key === 'ArrowUp') keys.up = false;
});

// Mobile controls - Touch Events
leftBtn.addEventListener('touchstart', (e) => {
    e.preventDefault();
    keys.left = true;
}, { passive: false });

leftBtn.addEventListener('touchend', (e) => {
    e.preventDefault();
    keys.left = false;
}, { passive: false });

rightBtn.addEventListener('touchstart', (e) => {
    e.preventDefault();
    keys.right = true;
}, { passive: false });

rightBtn.addEventListener('touchend', (e) => {
    e.preventDefault();
    keys.right = false;
}, { passive: false });

jumpBtn.addEventListener('touchstart', (e) => {
    e.preventDefault();
    keys.up = true;
}, { passive: false });

jumpBtn.addEventListener('touchend', (e) => {
    e.preventDefault();
    keys.up = false;
}, { passive: false });

// Mouse events for testing on desktop
leftBtn.addEventListener('mousedown', () => keys.left = true);
leftBtn.addEventListener('mouseup', () => keys.left = false);
leftBtn.addEventListener('mouseleave', () => keys.left = false);

rightBtn.addEventListener('mousedown', () => keys.right = true);
rightBtn.addEventListener('mouseup', () => keys.right = false);
rightBtn.addEventListener('mouseleave', () => keys.right = false);

jumpBtn.addEventListener('mousedown', () => keys.up = true);
jumpBtn.addEventListener('mouseup', () => keys.up = false);
jumpBtn.addEventListener('mouseleave', () => keys.up = false);

restartButton.addEventListener('click', () => {
    resetGame();
});

// Prevent default touchmove behavior to avoid scrolling
document.addEventListener('touchmove', (e) => {
    if (e.target.closest('#game-container')) {
        e.preventDefault();
    }
}, { passive: false });

// Initialize the game
function initGame() {
    resizeGame();
    createPlatforms();
    createCollectibles();
    createClouds();
    gameLoop();
}

// Resize game to fit screen
function resizeGame() {
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    
    // Set game container size based on window dimensions
    if (windowWidth <= 800 || windowHeight <= 600) {
        const scaleX = windowWidth / 800;
        const scaleY = windowHeight / 600;
        gameScale = Math.min(scaleX, scaleY);
        
        gameWidth = windowWidth;
        gameHeight = windowHeight;
        
        // Update game container size
        if (windowWidth <= 800) {
            gameContainer.style.width = windowWidth + 'px';
        }
        
        if (windowHeight <= 600) {
            gameContainer.style.height = windowHeight + 'px';
        }
    }
}

// Create initial platforms
function createPlatforms() {
    // Main ground
    createPlatform(0, 580, 800, 30);
    
    // Floating platforms
    createPlatform(100, 480, 200, 30);
    createPlatform(400, 480, 150, 30);
    createPlatform(650, 450, 120, 30);
    createPlatform(200, 380, 150, 30);
    createPlatform(450, 380, 180, 30);
    createPlatform(100, 280, 130, 30);
    createPlatform(350, 280, 120, 30);
    createPlatform(550, 280, 150, 30);
    createPlatform(250, 180, 300, 30);
    createPlatform(50, 150, 100, 30);
    createPlatform(650, 180, 120, 30);
}

// Create a platform
function createPlatform(x, y, width, height) {
    const platform = document.createElement('div');
    platform.className = 'platform';
    platform.style.width = width + 'px';
    platform.style.left = x + 'px';
    platform.style.top = y + 'px';
    
    gameContainer.appendChild(platform);
    platforms.push({
        element: platform,
        x: x,
        y: y,
        width: width,
        height: height
    });
}

// Create collectibles
function createCollectibles() {
    const positions = [
        {x: 150, y: 450},
        {x: 450, y: 450},
        {x: 700, y: 420},
        {x: 250, y: 350},
        {x: 500, y: 350},
        {x: 150, y: 250},
        {x: 400, y: 250},
        {x: 600, y: 250},
        {x: 300, y: 150},
        {x: 700, y: 150},
        {x: 100, y: 120}
    ];
    
    positions.forEach(pos => {
        const collectible = document.createElement('div');
        collectible.className = 'collectible';
        collectible.style.left = pos.x + 'px';
        collectible.style.top = pos.y + 'px';
        
        gameContainer.appendChild(collectible);
        collectibles.push({
            element: collectible,
            x: pos.x,
            y: pos.y,
            collected: false
        });
    });
}

// Create decorative clouds
function createClouds() {
    for (let i = 0; i < 5; i++) {
        const cloud = document.createElement('div');
        cloud.className = 'cloud';
        
        const width = 80 + Math.random() * 120;
        const height = width * 0.6;
        
        cloud.style.width = width + 'px';
        cloud.style.height = height + 'px';
        cloud.style.left = (Math.random() * 700) + 'px';
        cloud.style.top = (Math.random() * 200) + 'px';
        
        gameContainer.appendChild(cloud);
        clouds.push({
            element: cloud,
            x: parseFloat(cloud.style.left),
            speed: 0.2 + Math.random() * 0.3
        });
    }
}

// Check for platform collisions
function checkPlatformCollisions() {
    let onPlatform = false;
    
    platforms.forEach(platform => {
        // Check if player is above a platform and falling
        if (playerY + 60 >= platform.y && 
            playerY + 60 <= platform.y + 10 && 
            playerX + 40 >= platform.x && 
            playerX <= platform.x + platform.width &&
            velocityY >= 0) {
            
            playerY = platform.y - 60;
            velocityY = 0;
            isJumping = false;
            onPlatform = true;
        }
    });
    
    return onPlatform;
}

// Check for collectible collisions
function checkCollectibleCollisions() {
    collectibles.forEach(collectible => {
        if (!collectible.collected &&
            playerX < collectible.x + 20 &&
            playerX + 40 > collectible.x &&
            playerY < collectible.y + 20 &&
            playerY + 60 > collectible.y) {
            
            collectible.collected = true;
            collectible.element.style.display = 'none';
            score += 10;
            scoreElement.textContent = score;
            
            // Check if all collectibles are collected
            const allCollected = collectibles.every(c => c.collected);
            if (allCollected) {
                // Victory condition
                finalScoreElement.textContent = 'You won! Score: ' + score;
                gameOverScreen.style.display = 'flex';
                gameRunning = false;
            }
        }
    });
}

// Move clouds
function moveClouds() {
    clouds.forEach(cloud => {
        cloud.x -= cloud.speed;
        if (cloud.x < -parseFloat(cloud.element.style.width)) {
            cloud.x = gameWidth;
        }
        cloud.element.style.left = cloud.x + 'px';
    });
}

// Game over
function gameOver() {
    gameRunning = false;
    finalScoreElement.textContent = 'Score: ' + score;
    gameOverScreen.style.display = 'flex';
}

// Reset the game
function resetGame() {
    // Reset player position
    playerX = 100;
    playerY = 200;
    velocityX = 0;
    velocityY = 0;
    score = 0;
    scoreElement.textContent = score;
    
    // Reset collectibles
    collectibles.forEach(collectible => {
        collectible.collected = false;
        collectible.element.style.display = 'block';
    });
    
    // Hide game over screen
    gameOverScreen.style.display = 'none';
    gameRunning = true;
    
    // Resume game loop
    requestAnimationFrame(gameLoop);
}

// Update player direction for animation
function updatePlayerDirection() {
    if (velocityX > 0.5) {
        lastDirection = 'right';
        player.classList.remove('face-left');
        player.classList.add('face-right');
    } else if (velocityX < -0.5) {
        lastDirection = 'left';
        player.classList.remove('face-right');
        player.classList.add('face-left');
    }
}

// Main game loop
function gameLoop() {
    if (!gameRunning) return;
    
    // Handle keyboard input
    if (keys.left) velocityX = -5;
    else if (keys.right) velocityX = 5;
    else velocityX *= 0.8; // Friction
    
    // Jump if on platform
    if (keys.up && !isJumping) {
        velocityY = -12;
        isJumping = true;
    }
    
    // Apply gravity
    velocityY += gravity;
    
    // Update position
    playerX += velocityX;
    playerY += velocityY;
    
    // Update player direction (for animation)
    updatePlayerDirection();
    
    // Boundary checks based on game container size
    const rightBoundary = gameWidth - 40; // Player width is 40px
    if (playerX < 0) playerX = 0;
    if (playerX > rightBoundary) playerX = rightBoundary;
    
    // Check if player fell off
    if (playerY > gameHeight) {
        gameOver();
        return;
    }
    
    // Apply platform collisions
    const onPlatform = checkPlatformCollisions();
    
    // Check collectible collisions
    checkCollectibleCollisions();
    
    // Move clouds
    moveClouds();
    
    // Update player position
    player.style.left = playerX + 'px';
    player.style.bottom = (gameHeight - playerY - 60) + 'px';
    
    // Continue the game loop
    requestAnimationFrame(gameLoop);
}

// Handle orientation change
function handleOrientationChange() {
    if (window.innerHeight < 400) {
        orientationMessage.style.display = 'flex';
        gameContainer.style.display = 'none';
    } else {
        orientationMessage.style.display = 'none';
        gameContainer.style.display = 'block';
        resizeGame();
    }
}

// Event listener for orientation change and resize
window.addEventListener('resize', handleOrientationChange);
window.addEventListener('orientationchange', handleOrientationChange);

// Start the game
window.addEventListener('load', () => {
    handleOrientationChange();
    initGame();
});
