const canvas = document.getElementById('canva_background');
const c = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var mouse = {
    x: innerWidth/2,
    y: innerHeight/2
};

let effectArray;

let lt = 0;
let t=0;
let fps = 15;
let nxtfrm = 1000/fps;


const fs = 25;
c.font = fs+'px Arial';



window.addEventListener('resize', function(e)
{
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    c.font = fs+'px Arial';
    init();
});

function init()
{
    effectArray = [];
    for(var i = 0; i < innerWidth/fs; i++)
    {
        if(i!=0)
            effectArray.push(new Effect(fs, effectArray[i-1].x + fs, 0));
        else
            effectArray.push(new Effect(fs, 0, 0))
    }
}


function Effect(fontsize, x, y)
{
    this.characters = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン    0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ♔♕♖♗♘♙CHESS♚♛♜♝♞♟☀☁❆WEATHER❅❄';
    this.x = x;
    this.y = y;
    this.fontsize = fontsize;

    this.text = '';

    this.draw = function()
    {
        this.text = this.characters[Math.floor(Math.random() * this.characters.length)];
        c.fillStyle = 'green';
        c.fillText(this.text, this.x, this.y);
        this.update();
    }
    this.update = function()
    {
        if(this.y >= innerHeight && Math.random()>0.98)
            this.y = 0;
        this.y +=this.fontsize;
    }

}


init();
animate(0);

function animate(ts)
{
    requestAnimationFrame(animate);
    
    const dt = ts - lt;
    lt = ts;
    if(t > nxtfrm)
    {
    c.fillStyle = 'rgba(0, 0, 0, 0.08)';
    c.fillRect(0, 0, innerWidth, innerHeight);

    for(var i = 0; i<effectArray.length; i++)
    {
        effectArray[i].draw();
    }
    t=0;
    }
    else{
        t+=dt;
    }
    // console.log(ts,lt);
    
}