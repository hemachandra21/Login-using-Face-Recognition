const canvas = document.getElementById('canvas1');
const c = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let mouse = {
    x:innerWidth/2,
    y:innerHeight/2
};

let particleArray;

let lastpoint = {
    x:0,
    y:0
};

let colors = [
    "#00FFF6",
    "#00E7FF",
    "#009EFF",
    "#0014FF"
];


window.addEventListener('mousemove', function(e)
{
    mouse.x = e.x;
    mouse.y = e.y;
    // init();
});

window.addEventListener('resize', function()
{
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    init();
});

window.addEventListener('mouseout', function()
{
    mouse.x = innerWidth/2,
    mouse.y = innerHeight/2
});

function init(){

    particleArray = [];

    for(var i=0; i<50; i++)
    {
        const r = GetRandomIntInRange(1,3);
        const color = 
        particleArray.push(new Particle(mouse.x, mouse.y, r, GetRandomColor()));
    }

}

function GetRandomColor()
{
    return colors[Math.floor(Math.random()*colors.length)];
}

function GetRandomIntInRange(min, max)
{
    return Math.random()*(max - min +1) + min;
}

function Particle(x, y, r, color)
{
    this.x = x;
    this.y = y;
    this.r = r;
    this.color = color;
    this.velocity = 0.03;
    this.radians = (Math.random()* Math.PI*2);
    this.distfromcenter = GetRandomIntInRange(50,150);
    lastpoint.x = this.x;
    lastpoint.y = this.y;
    this.lastmouse = {
        x:x,
        y:y
    };

    this.draw = function()
    {
        this.update();
        c.beginPath();
        c.strokeStyle = this.color;
        c.lineWidth = this.r;
        c.moveTo(lastpoint.x, lastpoint.y);
        c.lineTo(this.x, this.y);
        c.stroke();
        c.closePath();
        
    }
    this.update = function()
    {
        //creating drag effect
        this.lastmouse.x += (mouse.x - this.lastmouse.x)*0.05;
        this.lastmouse.y += (mouse.y - this.lastmouse.y)*0.05;

        //getting last position to draw line
        lastpoint.x = this.x;
        lastpoint.y = this.y;

        this.x = this.lastmouse.x + (Math.cos(this.radians)) * this.distfromcenter;
        this.y = this.lastmouse.y + (Math.sin(this.radians)) * this.distfromcenter;
        this.radians += this.velocity;
        // this.draw();
    }
}

init();
animate();

function animate()
{
    requestAnimationFrame(animate);
    // c.clearRect(0, 0, innerWidth, innerHeight);
    c.fillStyle = 'rgba( 0, 0, 0, 0.05)';
    c.fillRect( 0, 0, innerWidth, innerHeight);

    for(var i=0; i<particleArray.length; i++)
    {
        particleArray[i].draw();
    }

}
