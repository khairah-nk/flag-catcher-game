/**
 * Catch the Flag - Kids Educational Falling Game Engine
 * Features:
 * - Flags drop downwards from the top of the sky with gentle parachute swaying
 * - Real-time Web Speech Synthesis for country name pronunciation on touch/catch
 * - Web Audio API synthesizer for cheerful marimba, chime & pop sounds
 * - Points (+100 XP), Combos (x2, x3), Confetti explosions, and Level Progression
 * - Interactive Mascot with Catch Basket tracking touch/cursor
 */

class FlagGame {
  constructor() {
    this.countries = [];
    this.activeFlags = [];
    this.score = 0;
    this.combo = 0;
    this.streak = 64;
    this.lives = 3;
    this.maxLives = 3;
    this.soundEnabled = true;
    this.selectedContinent = 'All';
    this.targetCountry = null;
    this.levelProgress = 0;
    this.level = 1;
    this.mascotX = 400;

    // DOM References
    this.arena = document.getElementById('sky-arena');
    this.targetCountryLabel = document.getElementById('target-country-name');
    this.targetFlagThumb = document.getElementById('target-flag-thumb');
    this.scoreDisplay = document.getElementById('score-display');
    this.streakDisplay = document.getElementById('streak-display');
    this.heartsContainer = document.getElementById('hearts-container');
    this.progressBar = document.getElementById('level-progress');
    this.soundToggleBtn = document.getElementById('sound-toggle');
    this.modalBackdrop = document.getElementById('country-modal');
    this.modalFlagImg = document.getElementById('modal-flag-img');
    this.modalCountryName = document.getElementById('modal-country-name');
    this.modalCapital = document.getElementById('modal-capital');
    this.modalContinent = document.getElementById('modal-continent');
    this.modalFunFact = document.getElementById('modal-fun-fact');
    this.listenAgainBtn = document.getElementById('listen-again-btn');
    this.continueBtn = document.getElementById('continue-btn');
    this.mascot = document.getElementById('pilot-mascot');

    // Confetti Canvas
    this.initConfetti();

    // Web Audio Synthesizer
    this.initAudioContext();

    this.lastSpawnTime = 0;
    this.spawnInterval = 1800; // ms
    this.isRunning = true;

    this.init();
  }

  async init() {
    try {
      const res = await fetch('assets/data/countries.json');
      this.countries = await res.json();
    } catch (err) {
      console.error('Failed to load countries.json', err);
    }

    this.bindEvents();
    this.setNewTargetCountry();
    this.spawnClouds();
    this.updateHeartsUI();
    this.updateProgressUI();

    requestAnimationFrame(this.gameLoop.bind(this));
  }

  initConfetti() {
    this.canvas = document.createElement('canvas');
    this.canvas.id = 'game-confetti';
    this.canvas.style.position = 'absolute';
    this.canvas.style.inset = '0';
    this.canvas.style.pointerEvents = 'none';
    this.canvas.style.zIndex = '35';
    this.arena.appendChild(this.canvas);
    this.ctx = this.canvas.getContext('2d');
    this.particles = [];

    const resize = () => {
      this.canvas.width = this.arena.clientWidth || 800;
      this.canvas.height = this.arena.clientHeight || 480;
    };
    resize();
    window.addEventListener('resize', resize);
  }

  initAudioContext() {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioCtx();
    } catch (e) {}
  }

  playTone(frequency, type = 'sine', duration = 0.25, gainValue = 0.25) {
    if (!this.soundEnabled || !this.audioCtx) return;
    if (this.audioCtx.state === 'suspended') this.audioCtx.resume();
    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(frequency, this.audioCtx.currentTime);
    gain.gain.setValueAtTime(gainValue, this.audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, this.audioCtx.currentTime + duration);

    osc.connect(gain);
    gain.connect(this.audioCtx.destination);
    osc.start();
    osc.stop(this.audioCtx.currentTime + duration);
  }

  playCatchSuccess() {
    this.playTone(523.25, 'triangle', 0.15); // C5
    setTimeout(() => this.playTone(659.25, 'triangle', 0.15), 70); // E5
    setTimeout(() => this.playTone(783.99, 'triangle', 0.25), 140); // G5
    setTimeout(() => this.playTone(1046.5, 'sine', 0.35), 210); // C6
  }

  playMissSound() {
    this.playTone(330, 'sawtooth', 0.15);
    setTimeout(() => this.playTone(260, 'sawtooth', 0.25), 100);
  }

  speakCountry(phrase) {
    if (!this.soundEnabled) return;
    this.playTone(587.33, 'triangle', 0.12);

    if (this.activeAudio) {
      try { this.activeAudio.pause(); this.activeAudio.currentTime = 0; } catch(e) {}
    }

    let html5Played = false;
    try {
      const url = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=' + encodeURIComponent(phrase);
      this.activeAudio = new Audio(url);
      const p = this.activeAudio.play();
      if (p !== undefined) {
        p.then(() => { html5Played = true; }).catch(err => {
          this.fallbackSpeech(phrase);
        });
      }
    } catch(e) {
      this.fallbackSpeech(phrase);
    }

    setTimeout(() => {
      if (!html5Played) {
        this.fallbackSpeech(phrase);
      }
    }, 350);
  }

  fallbackSpeech(phrase) {
    if (!('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel();
      setTimeout(() => {
        window.speechSynthesis.resume();
        const ut = new SpeechSynthesisUtterance(phrase);
        ut.rate = 0.9;
        ut.pitch = 1.15;
        ut.lang = 'en-US';
        window.currentUtterance = ut;
        window.speechSynthesis.speak(ut);
      }, 60);
    } catch(e) {}
  }

  announceTarget() {
    if (!this.targetCountry) return;
    this.speakCountry(`Catch the flag of ${this.targetCountry.name}!`);
  }

  togglePause() {
    this.isPaused = !this.isPaused;
    const pauseModal = document.getElementById('pause-modal');
    const pauseText = document.getElementById('pause-text');
    if (this.isPaused) {
      if (pauseModal) pauseModal.classList.add('active');
      if (pauseText) pauseText.textContent = '▶️ Resume';
      this.playTone(350, 'sine', 0.15);
      this.speakCountry('Game paused');
    } else {
      if (pauseModal) pauseModal.classList.remove('active');
      if (pauseText) pauseText.textContent = '⏸️ Pause';
      this.playTone(550, 'sine', 0.15);
      this.announceTarget();
    }
  }

  bindEvents() {
    this.soundToggleBtn.addEventListener('click', () => {
      this.soundEnabled = !this.soundEnabled;
      this.soundToggleBtn.innerHTML = this.soundEnabled ? '🔊' : '🔇';
      if (!this.soundEnabled) window.speechSynthesis.cancel();
    });

    // Unlock speech on first interaction
    let hasInteracted = false;
    const unlockAudio = () => {
      if (hasInteracted) return;
      hasInteracted = true;
      if (this.audioCtx && this.audioCtx.state === 'suspended') this.audioCtx.resume();
      this.announceTarget();
    };
    this.arena.addEventListener('pointerdown', unlockAudio, { once: true });

    const promptAudioBtn = document.getElementById('prompt-speaker-btn');
    if (promptAudioBtn) {
      promptAudioBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        unlockAudio();
        this.announceTarget();
      });
    }

    const pauseBtn = document.getElementById('pause-game-btn');
    if (pauseBtn) {
      pauseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.togglePause();
      });
    }

    const resumeBtn = document.getElementById('resume-btn');
    if (resumeBtn) {
      resumeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.togglePause();
      });
    }

    const editionSelect = document.getElementById('edition-select');
    if (editionSelect) {
      editionSelect.addEventListener('change', async (e) => {
        const val = e.target.value;
        let dataFile = 'assets/data/countries.json';
        if (val === 'malaysia') dataFile = 'assets/data/malaysia_states.json';
        else if (val === 'usa') dataFile = 'assets/data/usa_states.json';

        try {
          const res = await fetch(dataFile);
          this.countries = await res.json();
          // Remove active falling flags
          this.activeFlags.forEach(f => f.el.remove());
          this.activeFlags = [];
          this.setNewTargetCountry();
        } catch(err) {
          console.error('Failed to switch edition', err);
        }
      });
    }

    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space') {
        e.preventDefault();
        this.togglePause();
      }
    });

    this.listenAgainBtn.addEventListener('click', () => {
      if (this.currentModalCountry) {
        this.speakCountry(this.currentModalCountry.name);
      }
    });

    this.continueBtn.addEventListener('click', () => {
      this.closeModal();
    });

    // Mascot tracking mouse / touch horizontally
    this.arena.addEventListener('pointermove', (e) => {
      const rect = this.arena.getBoundingClientRect();
      this.mascotX = Math.max(50, Math.min(rect.width - 50, e.clientX - rect.left));
      if (this.mascot) {
        this.mascot.style.transform = `translateX(${this.mascotX - 45}px)`;
      }
    });
  }

  getFilteredCountries() {
    if (!this.countries.length) return [];
    if (this.selectedContinent === 'All') return this.countries;
    return this.countries.filter(c => c.continent === this.selectedContinent);
  }

  setNewTargetCountry() {
    const list = this.getFilteredCountries();
    if (!list.length) return;
    this.targetCountry = list[Math.floor(Math.random() * list.length)];

    if (this.targetCountryLabel) {
      this.targetCountryLabel.textContent = this.targetCountry.name;
    }
    if (this.targetFlagThumb) {
      this.targetFlagThumb.src = this.targetCountry.flag;
      this.targetFlagThumb.alt = this.targetCountry.name;
    }

    setTimeout(() => {
      this.speakCountry(`Find ${this.targetCountry.name}!`);
    }, 300);
  }

  spawnClouds() {
    for (let i = 0; i < 4; i++) {
      const cloud = document.createElement('div');
      cloud.className = 'cloud';
      const width = 120 + Math.random() * 80;
      const height = 48 + Math.random() * 25;
      cloud.style.width = `${width}px`;
      cloud.style.height = `${height}px`;
      cloud.style.top = `${40 + Math.random() * 200}px`;
      cloud.style.left = `${Math.random() * 80}%`;
      cloud.style.opacity = (0.5 + Math.random() * 0.4).toFixed(2);
      this.arena.appendChild(cloud);
    }
  }

  explodeConfetti(x, y) {
    const colors = ['#FF7A00', '#2DA8FF', '#58CC02', '#FFB800', '#FF4757', '#8C52FF'];
    for (let i = 0; i < 35; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 3 + Math.random() * 6;
      this.particles.push({
        x: x,
        y: y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 2,
        color: colors[Math.floor(Math.random() * colors.length)],
        size: 5 + Math.random() * 6,
        life: 1.0,
        decay: 0.02 + Math.random() * 0.02
      });
    }
  }

  spawnFloatingText(text, x, y, color = '#FF7A00') {
    const el = document.createElement('div');
    el.textContent = text;
    el.style.position = 'absolute';
    el.style.left = `${x}px`;
    el.style.top = `${y}px`;
    el.style.fontWeight = '900';
    el.style.fontSize = '22px';
    el.style.color = color;
    el.style.textShadow = '0 2px 6px rgba(255,255,255,0.95)';
    el.style.pointerEvents = 'none';
    el.style.zIndex = '55';
    el.style.transition = 'transform 0.8s ease-out, opacity 0.8s ease-out';
    this.arena.appendChild(el);

    requestAnimationFrame(() => {
      el.style.transform = 'translateY(-50px) scale(1.15)';
      el.style.opacity = '0';
    });

    setTimeout(() => el.remove(), 800);
  }

  // SPAWN FALLING FLAG (Drops from top)
  spawnFlag() {
    const pool = this.getFilteredCountries();
    if (!pool.length) return;

    let country;
    if (this.targetCountry && Math.random() < 0.45) {
      country = this.targetCountry;
    } else {
      country = pool[Math.floor(Math.random() * pool.length)];
    }

    const arenaWidth = this.arena.clientWidth || 800;
    const startX = 30 + Math.random() * (arenaWidth - 170);
    const startY = -110;

    const flagEl = document.createElement('div');
    flagEl.className = 'falling-flag';
    flagEl.style.position = 'absolute';
    flagEl.style.left = '0';
    flagEl.style.top = '0';
    flagEl.style.cursor = 'pointer';
    flagEl.style.zIndex = '25';

    flagEl.innerHTML = `
      <div style="font-size: 24px; text-align: center; margin-bottom: -6px; pointer-events: none;">🎈</div>
      <div class="flag-box" style="width: 100px; height: 70px; border-radius: 16px; background: #FFF; padding: 4px; box-shadow: 0 10px 24px rgba(0,30,80,0.2); border: 3px solid #FFF; overflow: hidden; display: flex; align-items: center; justify-content: center;">
        <img class="flag-img" src="${country.flag}" alt="${country.name}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px; pointer-events: none;" />
      </div>
      <span class="flag-name-tag" style="background: #FFF; padding: 2px 10px; border-radius: 9999px; font-size: 12px; font-weight: 800; color: #1E293B; box-shadow: 0 3px 6px rgba(0,0,0,0.1); border: 1.5px solid #EFE7DA; margin-top: 3px; display: inline-block; white-space: nowrap; pointer-events: none;">${country.name}</span>
    `;

    const flagObj = {
      el: flagEl,
      country: country,
      x: startX,
      baseX: startX,
      y: startY,
      speed: 1.7 + Math.random() * 0.8,
      seed: Math.random() * 100,
      caught: false
    };

    const catchHandler = (e) => {
      e.stopPropagation();
      if (flagObj.caught) return;
      flagObj.caught = true;
      this.handleFlagCatch(flagObj);
    };

    flagEl.addEventListener('pointerdown', catchHandler);
    flagEl.addEventListener('click', catchHandler);

    this.arena.appendChild(flagEl);
    this.activeFlags.push(flagObj);
  }

  handleFlagCatch(flagObj) {
    const country = flagObj.country;

    // Speak country name immediately!
    this.speakCountry(country.name);

    flagObj.el.style.animation = 'catchBurst 0.35s forwards';
    setTimeout(() => {
      flagObj.el.remove();
      this.activeFlags = this.activeFlags.filter(f => f !== flagObj);
    }, 350);

    // Is it the target country?
    if (this.targetCountry && country.code === this.targetCountry.code) {
      this.combo++;
      const points = 100 + (this.combo > 1 ? (this.combo - 1) * 50 : 0);
      this.score += points;
      this.scoreDisplay.textContent = this.score;

      this.playCatchSuccess();
      this.explodeConfetti(flagObj.x + 50, flagObj.y + 40);

      const msg = this.combo > 1 ? `+${points} (x${this.combo} 🔥)` : `+${points} ⭐`;
      this.spawnFloatingText(msg, flagObj.x, flagObj.y, '#58CC02');

      this.levelProgress++;
      this.updateProgressUI();

      if (this.levelProgress >= 5) {
        this.levelProgress = 0;
        this.level++;
        this.openCountryModal(country, true);
      } else {
        setTimeout(() => this.setNewTargetCountry(), 600);
      }
    } else {
      this.combo = 0;
      this.lives = Math.max(0, this.lives - 1);
      this.updateHeartsUI();
      this.playMissSound();
      this.spawnFloatingText(`That's ${country.name}!`, flagObj.x, flagObj.y, '#FF4757');
      this.speak(`That's ${country.name}! Find ${this.targetCountry.name}!`);

      if (this.lives === 0) {
        setTimeout(() => {
          alert(`Game Over! Great effort! You scored ${this.score} points!`);
          this.lives = this.maxLives;
          this.score = 0;
          this.scoreDisplay.textContent = '0';
          this.updateHeartsUI();
          this.setNewTargetCountry();
        }, 500);
      }
    }
  }

  openCountryModal(country, isLevelWin = false) {
    this.currentModalCountry = country;
    this.modalFlagImg.src = country.flag;
    this.modalFlagImg.alt = country.name;
    this.modalCountryName.textContent = country.name;
    this.modalCapital.textContent = country.capital || 'Capital City';
    this.modalContinent.textContent = country.continent || 'World';
    this.modalFunFact.textContent = isLevelWin
      ? `🎉 Fantastic! You completed Level ${this.level - 1}! Next level starting!`
      : `Capital: ${country.capital || 'Capital City'}.`;
    this.modalBackdrop.classList.add('active');
  }

  closeModal() {
    this.modalBackdrop.classList.remove('active');
    this.updateProgressUI();
    this.setNewTargetCountry();
  }

  updateHeartsUI() {
    if (!this.heartsContainer) return;
    this.heartsContainer.innerHTML = '';
    for (let i = 0; i < this.maxLives; i++) {
      const span = document.createElement('span');
      span.className = `heart-icon ${i >= this.lives ? 'lost' : ''}`;
      span.textContent = '❤️';
      this.heartsContainer.appendChild(span);
    }
  }

  updateProgressUI() {
    if (!this.progressBar) return;
    const pct = (this.levelProgress / 5) * 100;
    this.progressBar.style.width = `${pct}%`;
  }

  gameLoop(timestamp) {
    if (!this.isRunning) return;
    if (this.isPaused) {
      requestAnimationFrame(this.gameLoop.bind(this));
      return;
    }

    const arenaWidth = this.arena.clientWidth || 800;
    const arenaHeight = this.arena.clientHeight || 480;

    // Spawn falling flag every 1.8s
    if (timestamp - this.lastSpawnTime > this.spawnInterval) {
      if (this.activeFlags.length < 5) {
        this.spawnFlag();
      }
      this.lastSpawnTime = timestamp;
    }

    // Move falling flags downwards
    for (let i = this.activeFlags.length - 1; i >= 0; i--) {
      const f = this.activeFlags[i];
      if (f.caught) continue;

      f.y += f.speed; // Fall down!
      const sway = Math.sin((timestamp / 450) + f.seed) * 16;
      const currentX = f.baseX + sway;

      f.x = currentX;
      f.el.style.transform = `translate3d(${currentX}px, ${f.y}px, 0)`;

      // Mascot catch detection at bottom
      if (f.y >= arenaHeight - 110 && f.y <= arenaHeight - 30) {
        if (Math.abs((currentX + 50) - this.mascotX) < 55) {
          f.caught = true;
          this.handleFlagCatch(f);
          continue;
        }
      }

      // Past bottom of sky
      if (f.y > arenaHeight + 30) {
        f.el.remove();
        this.activeFlags.splice(i, 1);
      }
    }

    // Render confetti particles
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.15;
      p.life -= p.decay;

      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      this.ctx.fill();

      if (p.life <= 0) {
        this.particles.splice(i, 1);
      }
    }

    requestAnimationFrame(this.gameLoop.bind(this));
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.game = new FlagGame();
});
