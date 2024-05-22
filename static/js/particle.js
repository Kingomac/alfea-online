export default class Particle {
    constructor(x, y, r) {
        this.x = x
        this.y = y
        this.r = r
    }

    /**
     * 
     * @param {CanvasRenderingContext2D} ctx 
     */
    draw(ctx) {
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2)
        ctx.fillStyle = "rgba(212,46,93,0.5)"
        ctx.fill()
        ctx.closePath()
    }
}