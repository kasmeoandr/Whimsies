
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Nature's Ascent - Platformer Game</title>
    <style>
        * {
            box-sizing: border-box;
            touch-action: manipulation;
        }
        
        body {
            margin: 0;
            overflow: hidden;
            background-color: #87CEEB;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
            touch-action: none;
        }
        
        #game-container {
            position: relative;
            width: 800px;
            height: 600px;
            background: linear-gradient(to bottom, #87CEEB, #E0F7FA);
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            border-radius: 10px;
        }
        
        #player {
            position: absolute;
            width: 40px;
            height: 60px;
            background-color: #FF5722;
            border-radius: 5px;
            left: 100px;
            bottom: 200px;
            transition: transform 0.1s;
            z-index: 10;
        }
        
        .platform {
            position: absolute;
            height: 30px;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="30"><rect width="100" height="20" y="10" fill="%23795548"/><path d="M0,10 Q10,0 20,10 Q30,0 40,10 Q50,0 60,10 Q70,0 80,10 Q90,0 100,10" fill="%234CAF50" stroke="%23388E3C"/></svg>');
            background-repeat: repeat-x;
            background-size: 100px 30px;
        }
        
        .collectible {
            position: absolute;
            width: 20px;
            height: 20px;
            background-color: #FFD700;
            border-radius: 50%;
            animation: float 1s infinite alternate ease-in-out;
            box-shadow: 0 0 10px rgba(255,215,0,0.5);
        }
        
        .cloud {
            position: absolute;
            background-color: white;
            border-radius: 50px;
            opacity: 0.8;
        }
        
        #score-container {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-size: 24px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            z-index: 15;
        }
        
        #controls {
            position: absolute;
            bottom: 10px;
            width: 100%;
            text-align: center;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            background-color: rgba(0,0,0,0.3);
            padding: 5px 0;
        }
        
        @keyframes float {
            from { transform: translateY(0); }
            to { transform: translateY(-5px); }
        }
        
        #game-over {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.7);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 32px;
            display: none;
            z-index: 100;
        }
        
        button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 20px;
            cursor: pointer;
            border-radius: 5px;
            transition: background-color 0.3s;
            -webkit-tap-highlight-color: transparent;
        }
        
        button:hover {
            background-color: #3e8e41;
        }
        
        #player.face-right {
            transform: scaleX(1);
        }
        
        #player.face-left {
            transform: scaleX(-1);
        }
        
        #mobile-controls {
            position: absolute;
            bottom: 40px;
            width: 100%;
            display: none;
            justify-content: center;
            gap: 20px;
            z-index: 20;
        }
        
        .mobile-btn {
            width: 70px;
            height: 70px;
            background-color: rgba(255,255,255,0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            color: white;
            user-select: none;
            -webkit-user-select: none;
            -webkit-tap-highlight-color: transparent;
            touch-action: manipulation;
        }
        
        .mobile-btn:active {
            background-color: rgba(255,255,255,0.5);
        }
        
        #orientation-message {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.8);
            color: white;
            justify-content: center;
            align-items: center;
            text-align: center;
            font-size: 24px;
            z-index: 1000;
            padding: 20px;
        }
        
        /* Responsive game container */
        @media (max-width: 800px) {
            #game-container {
                width: 100vw;
                height: 100vh;
                border-radius: 0;
            }
            
            #mobile-controls {
                display: flex;
            }
            
            #controls {
                display: none;
            }
        }
        
        @media (max-height: 500px) and (orientation: landscape) {
            #mobile-controls {
                bottom: 10px;
            }
            
            .mobile-btn {
                width: 60px;
                height: 60px;
                font-size: 24px;
            }
        }
        
        @media (max-height: 400px) {
            #orientation-message {
                display: flex;
            }
            
            #game-container {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div id="orientation-message">
        <div>
            <p>Please rotate your device to portrait mode for the best gaming experience.</p>
            <button id="continue-anyway">Continue Anyway</button>
        </div>
    </div>

    <div id="game-container">
        <div id="player"></div>
        <div id="score-container">Score: <span id="score">0</span></div>
        <div id="controls">Use ← → to move and SPACEBAR to jump</div>
        <div id="mobile-controls">
            <div class="mobile-btn" id="left-btn">←</div>
            <div class="mobile-btn" id="jump-btn">↑</div>
            <div class="mobile-btn" id="right-btn">→</div>
        </div>
        <div id="game-over">
            <div>Game Over!</div>
            <div id="final-score">Score: 0</div>
            <button id="restart-button">Play Again</button>
        </div>
    </div>

    <script>
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
    </script>
