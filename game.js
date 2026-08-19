const canvas = document.querySelector('#game');
const ctx = canvas.getContext('2d');
const healthEl = document.querySelector('#health');
const crumbsEl = document.querySelector('#crumbs');
const questEl = document.querySelector('#quest');
const restartBtn = document.querySelector('#restart');

const keys = new Set();
const gravity = 0.65;
const ground = 360;

const initialState = () => ({
  hero: { x: 46, y: 298, w: 34, h: 46, vx: 0, vy: 0, grounded: false, invulnerable: 0 },
  villain: { x: 622, y: 300, w: 46, h: 54, direction: -1 },
  burger: { x: 700, y: 283, w: 42, h: 42 },
  platforms: [
    { x: 0, y: ground, w: 768, h: 72 },
    { x: 132, y: 292, w: 118, h: 18 },
    { x: 312, y: 238, w: 132, h: 18 },
    { x: 512, y: 286, w: 96, h: 18 },
  ],
  crumbs: [
    { x: 166, y: 254, taken: false },
    { x: 354, y: 200, taken: false },
    { x: 420, y: 200, taken: false },
    { x: 548, y: 248, taken: false },
    { x: 650, y: 322, taken: false },
  ],
  health: 3,
  won: false,
  lost: false,
  messageTimer: 0,
});

let state = initialState();

function resetGame() {
  state = initialState();
  updateHud();
}

function updateHud() {
  healthEl.textContent = state.health;
  crumbsEl.textContent = state.crumbs.filter((crumb) => crumb.taken).length;
  if (state.won) questEl.textContent = 'Hambúrguer recuperado!';
  else if (state.lost) questEl.textContent = 'O lanche caiu nas trevas...';
  else if (state.crumbs.every((crumb) => crumb.taken)) questEl.textContent = 'Pegue o hambúrguer!';
  else questEl.textContent = 'Colete as migalhas';
}

function overlaps(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

function drawPixelRect(x, y, w, h, color, outline = '#1b1238') {
  ctx.fillStyle = outline;
  ctx.fillRect(x - 3, y - 3, w + 6, h + 6);
  ctx.fillStyle = color;
  ctx.fillRect(x, y, w, h);
}

function drawHero(hero) {
  drawPixelRect(hero.x + 6, hero.y + 8, 22, 22, '#f2b880');
  drawPixelRect(hero.x + 8, hero.y + 30, 18, 16, '#65d6ff');
  ctx.fillStyle = '#ffd166';
  ctx.fillRect(hero.x + 3, hero.y + 2, 28, 8);
  ctx.fillStyle = '#1b1238';
  ctx.fillRect(hero.x + 12, hero.y + 16, 4, 4);
  ctx.fillRect(hero.x + 22, hero.y + 16, 4, 4);
  ctx.fillStyle = '#e8e8f8';
  ctx.fillRect(hero.x + 29, hero.y + 18, 18, 5);
  ctx.fillRect(hero.x + 42, hero.y + 10, 5, 21);
}

function drawVillain(villain) {
  drawPixelRect(villain.x + 7, villain.y + 15, 32, 28, '#d62828');
  ctx.fillStyle = '#f2c078';
  ctx.fillRect(villain.x + 2, villain.y + 10, 42, 11);
  ctx.fillRect(villain.x + 2, villain.y + 38, 42, 11);
  ctx.fillStyle = '#1b1238';
  ctx.fillRect(villain.x + 14, villain.y + 23, 5, 5);
  ctx.fillRect(villain.x + 28, villain.y + 23, 5, 5);
  ctx.fillStyle = '#fff7d6';
  ctx.fillRect(villain.x + 16, villain.y + 34, 14, 4);
  ctx.fillStyle = '#65d6ff';
  ctx.fillRect(villain.x - 8, villain.y + 12, 8, 8);
  ctx.fillRect(villain.x + 46, villain.y + 12, 8, 8);
}

function drawBurger(burger) {
  ctx.fillStyle = '#f4a261';
  ctx.fillRect(burger.x, burger.y + 6, burger.w, 12);
  ctx.fillStyle = '#ffd166';
  ctx.fillRect(burger.x + 4, burger.y + 4, 5, 3);
  ctx.fillRect(burger.x + 20, burger.y + 3, 5, 3);
  ctx.fillStyle = '#5fbf5f';
  ctx.fillRect(burger.x + 1, burger.y + 19, burger.w - 2, 6);
  ctx.fillStyle = '#7b3f2a';
  ctx.fillRect(burger.x + 4, burger.y + 25, burger.w - 8, 10);
  ctx.fillStyle = '#f4a261';
  ctx.fillRect(burger.x + 2, burger.y + 35, burger.w - 4, 8);
}

function drawScene() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#79b8ff';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#ffffff55';
  for (let i = 0; i < 7; i += 1) ctx.fillRect(i * 128 + 16, 54 + (i % 2) * 28, 54, 10);

  state.platforms.forEach((platform) => {
    drawPixelRect(platform.x, platform.y, platform.w, platform.h, '#5b8c43', '#36592b');
    ctx.fillStyle = '#8a5a44';
    ctx.fillRect(platform.x, platform.y + 12, platform.w, platform.h - 12);
  });

  state.crumbs.forEach((crumb) => {
    if (crumb.taken) return;
    ctx.fillStyle = '#ffd166';
    ctx.fillRect(crumb.x, crumb.y, 14, 14);
    ctx.fillStyle = '#fff7d6';
    ctx.fillRect(crumb.x + 4, crumb.y + 3, 4, 4);
  });

  drawBurger(state.burger);
  drawVillain(state.villain);
  drawHero(state.hero);

  if (state.won || state.lost) {
    ctx.fillStyle = 'rgba(23, 19, 47, 0.78)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#ffd166';
    ctx.font = '32px Courier New';
    ctx.textAlign = 'center';
    ctx.fillText(state.won ? 'Vitória crocante!' : 'Derrota apimentada!', canvas.width / 2, 190);
    ctx.font = '18px Courier New';
    ctx.fillText('Clique em recomeçar para jogar novamente.', canvas.width / 2, 226);
    ctx.textAlign = 'left';
  }
}

function updateHero() {
  const hero = state.hero;
  const left = keys.has('ArrowLeft') || keys.has('a');
  const right = keys.has('ArrowRight') || keys.has('d');
  const jump = keys.has(' ') || keys.has('ArrowUp') || keys.has('w');

  hero.vx = left ? -4 : right ? 4 : 0;
  if (jump && hero.grounded) {
    hero.vy = -12;
    hero.grounded = false;
  }

  hero.x += hero.vx;
  hero.x = Math.max(0, Math.min(canvas.width - hero.w, hero.x));
  hero.vy += gravity;
  hero.y += hero.vy;
  hero.grounded = false;

  state.platforms.forEach((platform) => {
    const wasAbove = hero.y + hero.h - hero.vy <= platform.y;
    if (overlaps(hero, platform) && hero.vy >= 0 && wasAbove) {
      hero.y = platform.y - hero.h;
      hero.vy = 0;
      hero.grounded = true;
    }
  });

  if (hero.y > canvas.height) {
    state.health -= 1;
    hero.x = 46;
    hero.y = 298;
    hero.vy = 0;
  }

  if (hero.invulnerable > 0) hero.invulnerable -= 1;
}

function updateVillain() {
  const villain = state.villain;
  villain.x += villain.direction * 1.4;
  if (villain.x < 570 || villain.x > 665) villain.direction *= -1;
}

function updateCollectibles() {
  state.crumbs.forEach((crumb) => {
    if (!crumb.taken && overlaps(state.hero, { x: crumb.x, y: crumb.y, w: 14, h: 14 })) crumb.taken = true;
  });

  if (overlaps(state.hero, state.villain) && state.hero.invulnerable === 0 && !state.crumbs.every((crumb) => crumb.taken)) {
    state.health -= 1;
    state.hero.invulnerable = 80;
    state.hero.x = Math.max(8, state.hero.x - 70);
  }

  if (state.health <= 0) state.lost = true;
  if (state.crumbs.every((crumb) => crumb.taken) && overlaps(state.hero, state.burger)) state.won = true;
}

function loop() {
  if (!state.won && !state.lost) {
    updateHero();
    updateVillain();
    updateCollectibles();
    updateHud();
  }
  drawScene();
  requestAnimationFrame(loop);
}

window.addEventListener('keydown', (event) => {
  if (['ArrowLeft', 'ArrowRight', 'ArrowUp', ' ', 'a', 'd', 'w'].includes(event.key)) event.preventDefault();
  keys.add(event.key);
});

window.addEventListener('keyup', (event) => keys.delete(event.key));
restartBtn.addEventListener('click', resetGame);

updateHud();
loop();
