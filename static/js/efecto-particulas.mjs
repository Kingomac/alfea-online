import Particle from './particle.js'

/** @type { HTMLCanvasElement } */
const canvas = document.getElementById('efecto-particulas')
canvas.width = window.innerWidth
canvas.height = window.innerHeight


const ctx = canvas.getContext('2d')
let NUM_PARTICLES = 0
let particles = []
let particleInterval = undefined

window.addEventListener('DOMContentLoaded', () => {
    crearParticulas()
})

window.addEventListener('resize', () => {
    console.log('resize')
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    crearParticulas()
})

function crearParticulas() {
    clearInterval(particleInterval)
    NUM_PARTICLES = window.innerWidth * window.innerHeight / 10000
    particles = []
    particleInterval = undefined

    for (let i = 0; i < NUM_PARTICLES; i++) {
        particles.push(new Particle(
            Math.random() * canvas.width,
            Math.random() * canvas.height,
            Math.random() * 20 + 1
        ))
    }

    particleInterval = setInterval(() => {
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        for (const p of particles) {
            p.y += Math.random() * 0.27
            if (p.y > canvas.height + p.r) {
                p.y = -p.r
            }
            p.draw(ctx)
        }
    }, 1000 / 60);

}