
    // Create particle system

    function createParticles() {
        const container = document.querySelector('.circuit-container');
        const particleCount = 50;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            const size = Math.random() * 3 + 1;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            
            // Random position
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * 100 + 50;
            const x = Math.cos(angle) * distance + 150;
            const y = Math.sin(angle) * distance + 150;
            
            particle.style.left = x + 'px';
            particle.style.top = y + 'px';
            
            // Animation
            particle.style.animation = `
                rotate ${Math.random() * 10 + 10}s linear infinite,
                pulse ${Math.random() * 2 + 1}s ease-in-out infinite
            `;
            
            container.appendChild(particle);
        }
    }

    // Generate hexagon grid
    function generateHexGrid() {
        const svg = document.querySelector('.hex-grid');
        const size = 15;
        const width = 300;
        const height = 300;
        const rows = Math.ceil(height / (size * 1.5));
        const cols = Math.ceil(width / (size * Math.sqrt(3)));
        
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                const x = col * size * Math.sqrt(3);
                const y = row * size * 1.5;
                const points = hexagonPoints(x + (row % 2) * size * Math.sqrt(3) / 2, y, size);
                const hex = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
                hex.setAttribute("points", points);
                hex.setAttribute("fill", "none");
                hex.setAttribute("stroke", "#4a90e2");
                hex.setAttribute("stroke-width", "0.5");
                svg.appendChild(hex);
            }
        }
    }

    function hexagonPoints(x, y, size) {
        const points = [];
        for (let i = 0; i < 6; i++) {
            const angle = (Math.PI / 3) * i;
            points.push(`${x + size * Math.cos(angle)},${y + size * Math.sin(angle)}`);
        }
        return points.join(" ");
    }

    // Loading text animation
    function animateLoadingText() {
        const messages = [
            "AI",        
        ];
        let currentIndex = 0;
        const textElement = document.getElementById('loading-text');

        setInterval(() => {
            textElement.style.opacity = 0;
            setTimeout(() => {
                textElement.textContent = messages[currentIndex];
                textElement.style.opacity = 1;
                currentIndex = (currentIndex + 1) % messages.length;
            }, 10);
        }, 100);
    }


    window.addEventListener("load", function() {
        createParticles();
        generateHexGrid();
        
        animateLoadingText();
    
        const hder = document.querySelector('.navbar');
        // hder.style.display = 'none';
    
        
    });
    
    
    // // Initialize everything
    document.addEventListener('DOMContentLoaded', () => {
       // Hide loader after timeout
       setTimeout(() => {
        document.getElementById('loader-wrapper').classList.add('hidden');
        
    }, 800);
    });