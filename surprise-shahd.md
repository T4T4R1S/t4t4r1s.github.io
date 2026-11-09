---
layout: null
title: For Shahd
permalink: /s-7k2x-shahd/
sitemap: false
robots: noindex
---

<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex,nofollow">
  <title>For Shahd</title>

  <!-- Google Fonts CDN -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lora:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">

  <style>
    /* --------------------------------------------------------------
       Respect reduced motion
       -------------------------------------------------------------- */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }

    /* ---------------------------------------------------------------
       Root variables / design palette
       --------------------------------------------------------------- */
    :root {
      --bg: #FAF6F1;
      --bg-dark: #2D1B20;
      --rose: #D8A7B1;
      --gold: #C9A66B;
      --plum: #4A2C3A;
      --plum-light: #6A3F4A;
      --text: #4A2C3A;
      --text-light: #6B5B6D;
      --border: #E0D5C8;
    }

    [data-theme="dark"] {
      --bg: #2D1B20;
      --bg-dark: #1A0D11;
      --rose: #C8788B;
      --gold: #B8936A;
      --plum: #E8D5D1;
      --text: #F5E8E0;
      --text-light: #A57D88;
      --border: #4A2C3A;
    }

    /* --------------------------------------------------------------
       Base resets
       -------------------------------------------------------------- */
    *,
    *::before,
    *::after {
      box-sizing: border-box;
    }

    html {
      font-size: 16px;
      scroll-behavior: smooth;
    }

    body {
      margin: 0;
      font-family: 'Cairo', system-ui, -apple-system, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      direction: rtl;
      line-height: 1.6;
      overflow-x: hidden;
    }

    html[dir="ltr"] body {
      direction: ltr;
      font-family: 'Lora', serif;
    }

    /* Language toggle */
    .lang-toggle {
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
      justify-content: center;
    }

    .lang-btn {
      background: transparent;
      border: 1px solid var(--gold);
      color: var(--gold);
      padding: 6px 12px;
      font-family: 'Cairo', system-ui, sans-serif;
      font-size: 0.85rem;
      border-radius: 4px;
      cursor: pointer;
      transition: background 0.2s, color 0.2s;
    }

    .lang-btn:hover,
    .lang-btn.active {
      background: var(--gold);
      color: var(--bg);
    }

    .lang-btn:focus {
      outline: 2px solid var(--plum);
      outline-offset: 2px;
    }

    /* --------------------------------------------------------------
       Gate screen
       -------------------------------------------------------------- */
    #gate {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, var(--bg) 0%, var(--rose) 100%);
      transition: opacity 0.6s ease;
    }

    #gate.revealed {
      opacity: 0;
      pointer-events: none;
    }

    .gate-content {
      text-align: center;
      max-width: 90%;
      padding: 2rem;
    }

    .gate-title {
      font-family: 'Playfair Display', serif;
      font-size: 2.5rem;
      color: var(--plum);
      margin-bottom: 0.5rem;
    }

    .gate-subtitle {
      font-family: 'Cairo', system-ui, sans-serif;
      font-size: 1.2rem;
      color: var(--text-light);
      margin-bottom: 2rem;
    }

    .gate-input-wrapper {
      position: relative;
      margin: 1.5rem auto;
    }

    .gate-input {
      width: 100%;
      max-width: 300px;
      padding: 12px 16px 12px 48px;
      font-family: 'Cairo', system-ui, sans-serif;
      font-size: 1rem;
      border: 2px solid var(--border);
      border-radius: 25px;
      background: var(--bg);
      color: var(--text);
      caret-color: var(--gold);
      transition: border-color 0.3s, box-shadow 0.3s;
    }

    .gate-input:focus {
      outline: none;
      border-color: var(--gold);
      box-shadow: 0 0 0 4px rgba(201, 166, 107, 0.15);
    }

    .gate-input::placeholder {
      color: var(--text-light);
    }

    .gate-input::-webkit-calendar-picker-indicator {
      display: none;
    }

    .gate-submit {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      background: transparent;
      border: none;
      color: var(--gold);
      font-family: 'Cairo', system-ui, sans-serif;
      font-size: 1.2rem;
      cursor: pointer;
    }

    .gate-submit:focus {
      outline: 2px solid var(--plum);
      outline-offset: 2px;
    }

    .gate-message {
      margin-top: 2rem;
      font-family: 'Cairo', system-ui, sans-serif;
      color: var(--rose);
      font-size: 0.95rem;
      min-height: 1.2rem;
    }

    /* Shake animation for wrong attempts */
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-8px); }
      40%, 80% { transform: translateX(8px); }
    }

    .shake {
      animation: shake 0.45s ease-in-out;
    }

    /* --------------------------------------------------------------
       Surprise container (initially hidden via <template>)
       -------------------------------------------------------------- */
    #surprise {
      display: none;
      min-height: 100vh;
      padding: 2rem 1rem;
    }

    #surprise.revealed {
      display: block;
      animation: fadeIn 0.8s ease forwards;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Typewriter effect */
    .typewriter {
      overflow: hidden;
      border-right: 2px solid var(--gold);
      white-space: nowrap;
      animation: typewriter 3s steps(40) forwards, blink-caret 0.7s step-end infinite;
    }

    @keyframes typewriter {
      from { width: 0; }
      to { width: 100%; }
    }

    @keyframes blink-caret {
      from, to { border-color: transparent; }
      50% { border-color: var(--gold); }
    }

    /* --------------------------------------------------------------
       Sections
       -------------------------------------------------------------- */
    .section {
      max-width: 800px;
      margin: 4rem auto;
      padding: 2rem;
      background: rgba(250, 246, 241, 0.5);
      border-radius: 12px;
      border: 1px solid var(--border);
      backdrop-filter: blur(10px);
    }

    .section[data-lang="ar"] {
      direction: rtl;
      text-align: right;
    }

    .section[data-lang="en"] {
      direction: ltr;
      text-align: left;
    }

    .section[data-lang="both"] {
      direction: rtl;
      text-align: right;
    }

    .section h2 {
      font-family: 'Amiri', serif;
      font-size: 1.8rem;
      color: var(--plum);
      margin-top: 0;
      margin-bottom: 1.5rem;
      padding-bottom: 0.8rem;
      border-bottom: 2px solid var(--gold);
    }

    .section h2.english {
      font-family: 'Playfair Display', serif;
      direction: ltr;
      unicode-bidi: bidi-override;
      direction: ltr;
    }

    .divider {
      width: 40px;
      height: 2px;
      background: var(--gold);
      margin: 1.5rem auto;
    }

    /* --------------------------------------------------------------
       Memories timeline
       -------------------------------------------------------------- */
    .timeline {
      position: relative;
      padding-left: 20px;
    }

    .timeline::before {
      content: '';
      position: absolute;
      left: 4px;
      top: 0;
      bottom: 0;
      width: 2px;
      background: var(--gold);
    }

    .timeline-item {
      margin-bottom: 2rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--border);
    }

    .timeline-item:last-child {
      border-bottom: none;
    }

    .timeline-date {
      font-family: 'Amiri', serif;
      font-size: 0.9rem;
      color: var(--gold);
      margin-bottom: 0.5rem;
    }

    .timeline-title {
      font-family: 'Playfair Display', serif;
      font-size: 1.1rem;
    }

    /* --------------------------------------------------------------
       Reasons cards (flip-in one by one)
       -------------------------------------------------------------- */
    .reasons-grid {
      display: grid;
      gap: 1rem;
    }

    .reason-card {
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.5rem;
      position: relative;
      overflow: hidden;
      transform: translateY(20px);
      opacity: 0;
      transition: transform 0.6s ease, opacity 0.6s ease;
    }

    .reason-card.visible {
      transform: translateY(0);
      opacity: 1;
    }

    .reason-card::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 0;
      height: 2px;
      background: var(--gold);
      transition: width 0.4s ease;
    }

    .reason-card.visible::after {
      width: 100%;
    }

    /* --------------------------------------------------------------
       Closing line
       -------------------------------------------------------------- */
    .closing {
      text-align: center;
      margin: 3rem 0;
    }

    .closing .heart {
      display: inline-block;
      margin-left: 4px;
      animation: pulse 1.5s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.2); }
    }

    /* --------------------------------------------------------------
       Confetti / petals button
       -------------------------------------------------------------- */
    .confetti-btn {
      display: inline-block;
      margin-top: 2rem;
      padding: 10px 20px;
      background: transparent;
      border: 2px solid var(--gold);
      color: var(--gold);
      font-family: 'Cairo', system-ui, sans-serif;
      font-size: 0.95rem;
      border-radius: 25px;
      cursor: pointer;
      transition: background 0.3s, color 0.3s;
    }

    .confetti-btn:hover {
      background: var(--gold);
      color: var(--bg);
    }

    .confetti-btn:focus {
      outline: 2px solid var(--plum);
      outline-offset: 2px;
    }

    /* --------------------------------------------------------------
       Reduced motion adjustments
       -------------------------------------------------------------- */
    @media (prefers-reduced-motion: reduce) {
      .typewriter { animation: none; }
      .reason-card { transition: none; transform: translateY(0); opacity: 1; }
      .confetti-btn { animation: none; }
      .heart { animation: none; }
      .timeline-item { animation: none; }
    }
  </style>
</head>
<body>

  <!-- ==================== GATE SCREEN ==================== -->
  <div id="gate">
    <div class="gate-content">
      <h1 class="gate-title">For Shahd</h1>
      <p class="gate-subtitle">اكتبي الكلمة السرية 🔑 / Enter our secret word</p>

      <div class="gate-input-wrapper">
        <input type="text" class="gate-input" id="passwordInput" placeholder="..." autocomplete="off">
        <button class="gate-submit" aria-label="Submit password" onclick="checkPassword()">✓</button>
      </div>

      <p class="gate-message" id="gateMessage"></p>
    </div>
  </div>

  <!-- ==================== SURPRISE CONTENT (in template) ==================== -->
  <template id="surpriseTemplate">
    <div id="surprise">
      <!-- Language toggle -->
      <div class="lang-toggle" id="langToggle">
        <button class="lang-btn active" data-lang="both" aria-label="Both languages">Both</button>
        <button class="lang-btn" data-lang="ar" aria-label="Arabic">AR</button>
        <button class="lang-btn" data-lang="en" aria-label="English">EN</button>
      </div>

      <!-- 1. Opening -->
      <section class="section" id="opening" data-lang="both">
        <h2 class="english">Happy [OCCASION], Shahd</h2>
        <div class="divider"></div>
        <p class="typewriter" id="typewriterText">كل سنة وانتي طيبة يا شهد 🤍</p>
      </section>

      <!-- 2. Heartfelt letter -->
      <section class="section" id="letter" data-lang="both">
        <h2>Letter from Mostafa</h2>
        <div class="divider"></div>

        <div id="letterAr" dir="rtl" lang="ar">
          <!-- CONFIG letterAr content -->
        </div>

        <div id="letterEn" dir="ltr" lang="en" style="display:none;">
          <!-- CONFIG letterEn content -->
        </div>
      </section>

      <!-- 3. Our moments timeline -->
      <section class="section" id="moments" data-lang="both">
        <h2>Our Moments</h2>
        <div class="divider"></div>
        <div class="timeline" id="timeline">
          <!-- CONFIG memories injected here -->
        </div>
      </section>

      <!-- 4. Reasons I love you -->
      <section class="section" id="reasons" data-lang="both">
        <h2>Reasons I Love You</h2>
        <div class="divider"></div>
        <div class="reasons-grid" id="reasonsGrid">
          <!-- CONFIG reasons injected here -->
        </div>
      </section>

      <!-- 5. Closing line -->
      <section class="section closing" id="closing">
        <p class="arabic" dir="rtl" lang="ar">حبيبك مصطفى / Yours, Mostafa</p>
        <span class="heart">❤️</span>
      </section>

      <!-- 6. Confetti button (optional) -->
      <button class="confetti-btn" id="confettiBtn" aria-label="Trigger confetti">
        اضغطي هنا 💌 / Tap here
      </button>
    </div>
  </template>

  <!-- Confetti canvas (hidden by default) -->
  <canvas id="confettiCanvas" style="position:fixed; top:0; left:0; pointer-events:none; width:100%; height:100%; z-index:100;"></canvas>

  <script>
    // ==============================================================
      // CONFIG – editable text in one place
      // ==============================================================
      const CONFIG = {
        // Occasion for the opening (e.g., "Anniversary", "Birthday", "Just because")
        occasion: "[OCCASION]",

        // Opening line (typewriter will show the Arabic; English is optional)
        openingAr: "كل سنة وانتي طيبة يا شهد 🤍",
        openingEn: "Happy [OCCASION], Shahd",

        // Letter from Mostafa (6-8 lines each language, separated by <br>)
        letterAr: "iestykiki ya shahd,\nanta nour el ein wafa el qolub,\nma malaket shi fi hayati illa entay,\nenta leya donya kbeera w nora,\nana bahebak toman w la kayfa,\nenta leya kol shay kbeer w khas\n kol sana wa anta Tayeba yastoreni el felfel 🤍",
        letterEn: "My dearest Shahd,\nYou are the light in my eyes and the warmth in all hearts,\nThere is nothing in my life but you,\nYou are a big world and a light to me,\nI love you so much and how,\nYou are everything big and special to me\nEvery day you make me shine 🤍",

        // Memories array for the timeline
        memories: [
          {
            date: "02.01.2024",
            titleAr: "أول لقاء",
            titleEn: "First Meeting",
            textAr: "تذكر أول مرة التقيت فيها عينك عيني، كان ذلكmoment سحري لن أنساه أبداً.",
            textEn: "Remember the first time I met your eyes — that moment was magical and I'll never forget it."
          },
          {
            date: "14.02.2024",
            titleAr: "عيد الحب الأول",
            titleEn: "First Valentine's Day",
            textAr: "كانت هذه أول Valentine's Day معنا، مليئة بالورود والهدايا الحلوة.",
            textEn: "This was our first Valentine's Day, filled with roses and sweet gifts."
          },
          {
            date: "15.06.2024",
            titleAr: "رحلة القاهرة",
            titleEn: "Cairo Trip",
            textAr: "رحلتنا إلى القاهرة وكانت أيام لا تنسى، أكلنا الكشري وضحكنا لحد النسيان.",
            textEn: "Our trip to Cairo was unforgettable days, we ate koshary and laughed till we forgot everything."
          },
          {
            date: "03.09.2024",
            titleAr: "ليلة السينما",
            titleEn: "Movie Night",
            textAr: "ليالي السينما معاً، حيث نتابع الأفلام ونشارك التعليقات المضحكة.",
            textEn: "Movie nights together, watching films and sharing funny comments."
          }
        ],

        // Reasons I love you (bilingual strings)
        reasons: [
          "أحبك لأنكِ النور في عيني ✨ / I love you because you are the light in my eyes",
          "أحبك لأن ابتسامتك تُضيء يومي ☀️ / I love you because your smile lights up my day",
          "أحبك لصبركِ ولطفكِ الشديدين 🤲 / I love you for your extreme patience and kindness",
          "أحبك لأنكِ تفهمينني من غير كلمات 🤝 / I love you because you understand me without words",
          "أحبك للحيوية والطاقة الإيجابية اللي فيكِ 🌺 / I love you for your vitality and positive energy",
          "أحبك لثقتكِ بنفسكِ وكبرياءكِ 👑 / I love you for your confidence and pride in yourself",
          "أحبك لكل صغيرة وكبيرة فيكي 🌹 / I love you for every small and big thing about you",
          "أحبك لأنكِ زوجتي وحبيبتي للأبد ❤️ / I love you because you are my wife and beloved forever"
        ]
      };

      // ==============================================================
      // Password handling – SHA-256 hash only, verification via crypto.subtle
      // ==============================================================
      const PLAIN_PASSWORD = '7ab!bk Mu$7af4'; // do NOT use this directly for comparison
      const PASSWORD_HASH = '64987531e7c8cabf8fee6215c21e589be0d3abf1979d4705a898e94775061256'; // SHA-256 of the password

      async function initPassword() {
        // Compute hash of the user's input and compare with stored hash
        const encoder = new TextEncoder();
        const data = encoder.encode(document.getElementById('passwordInput').value);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

        return hashHex === PASSWORD_HASH;
      }

      function checkPassword() {
        const input = document.getElementById('passwordInput').value.trim();
        if (input === '') {
          showMessage('يرجى Enter الكلمة / Please enter the word');
          return;
        }

        initPassword().then(isValid => {
          if (isValid) {
            // Fade out gate, reveal surprise
            document.getElementById('gate').classList.add('revealed');
            // Wait for fade out then show surprise
            setTimeout(() => {
              document.getElementById('gate').style.display = 'none';
              document.getElementById('surprise').classList.add('revealed');
              initSurprise();
            }, 600);
          } else {
            // Shake gate + message
            document.getElementById('gate').classList.add('shake');
            setTimeout(() => {
              document.getElementById('gate').classList.remove('shake');
            }, 450);
            showMessage('قريبة... جربي تاني 🤍 / So close... try again');
          }
        });
      }

      function showMessage(msg) {
        const el = document.getElementById('gateMessage');
        el.innerHTML = msg;
        el.style.opacity = '1';
        setTimeout(() => {
          el.style.opacity = '0';
        }, 3000);
      }

      // ==============================================================
      // Surprise initialization
      // ==============================================================
      function initSurprise() {
        // Typewriter effect
        const typewriter = document.getElementById('typewriterText');
        const openingAr = CONFIG.openingAr.replace('[OCCASION]', CONFIG.occasion);
        typewriter.textContent = openingAr;
        // Trigger typewriter animation
        typewriter.style.width = 'auto';
        // Wait for typewriter to finish then remove cursor simulation
        setTimeout(() => {
          typewriter.style.borderRight = 'none';
        }, 3200);

        // Language toggle
        initLanguageToggle();

        // Letter section
        initLetter();

        // Memories timeline
        initTimeline();

        // Reasons cards
        initReasons();

        // Confetti button
        initConfetti();
      }

      function initLanguageToggle() {
        const toggleBtns = document.querySelectorAll('.lang-btn');
        const sectionAr = document.getElementById('letterAr');
        const sectionEn = document.getElementById('letterEn');
        const openingAr = document.getElementById('typewriterText');

        function setLang(lang) {
          // Update toggle buttons
          toggleBtns.forEach(btn => btn.classList.remove('active'));
          const activeBtn = document.querySelector(`.lang-btn[data-lang="${lang}"]`);
          if (activeBtn) activeBtn.classList.add('active');

          // Update opening
          if (lang === 'ar') {
            openingAr.textContent = CONFIG.openingAr.replace('[OCCASION]', CONFIG.occasion);
            openingAr.style.display = 'block';
            sectionEn.style.display = 'none';
          } else if (lang === 'en') {
            openingAr.textContent = CONFIG.openingEn.replace('[OCCASION]', CONFIG.occasion);
            openingAr.style.display = 'block';
            sectionEn.style.display = 'block';
            // Simple English translation placeholder
            openingAr.innerHTML = CONFIG.openingEn.replace('[OCCASION]', CONFIG.occasion);
            sectionEn.style.display = 'block';
          } else { // both
            openingAr.textContent = CONFIG.openingAr.replace('[OCCASION]', CONFIG.occasion);
            openingAr.style.display = 'block';
            sectionEn.style.display = 'block';
          }
        }

        toggleBtns.forEach(btn => {
          btn.addEventListener('click', () => setLang(btn.dataset.lang));
        });

        // Default: Both
        setLang('both');
      }

      function initLetter() {
        const letterAr = document.getElementById('letterAr');
        const letterEn = document.getElementById('letterEn');

        letterAr.innerHTML = CONFIG.letterAr
          .split('\n')
          .map(line => `<p>${line}</p>`)
          .join('');

        // Initially show Arabic, hide English (toggle will switch)
        letterEn.innerHTML = CONFIG.letterEn
          .split('\n')
          .map(line => `<p>${line}</p>`)
          .join('');

        letterEn.style.display = 'none';
      }

      function initTimeline() {
        const timeline = document.getElementById('timeline');
        timeline.innerHTML = '';

        CONFIG.memories.forEach(mem => {
          const item = document.createElement('div');
          item.className = 'timeline-item';
          item.innerHTML = `
            <div class="timeline-date">${mem.date}</div>
            <div>
              <h3 class="timeline-title english">${mem.titleEn}</h3>
              <p dir="rtl" lang="ar">${mem.textAr}</p>
              <p dir="ltr" lang="en">${mem.textEn}</p>
            </div>
          `;
          timeline.appendChild(item);
        });

        // Fade-in on scroll for timeline items
        const observerOptions = {
          threshold: 0.1,
          rootMargin: '0px'
        };

        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.style.animation = 'fadeIn 0.6s ease forwards';
              observer.unobserve(entry.target);
            }
          });
        }, observerOptions);

        document.querySelectorAll('.timeline-item').forEach(item => {
          observer.observe(item);
        });
      }

      function initReasons() {
        const grid = document.getElementById('reasonsGrid');
        grid.innerHTML = '';

        CONFIG.reasons.forEach((reason, idx) => {
          const card = document.createElement('div');
          card.className = 'reason-card';
          card.style.transitionDelay = `${idx * 0.1}s`;
          card.innerHTML = `
            <p>${reason}</p>
          `;
          grid.appendChild(card);

          // Trigger visibility on scroll
          const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
              if (entry.isIntersecting) {
                card.classList.add('visible');
                observer.unobserve(card);
              }
            });
          }, {
            threshold: 0.2,
            rootMargin: '0px'
          });
          observer.observe(card);
        });
      }

      function initConfetti() {
        const canvas = document.getElementById('confettiCanvas');
        const ctx = canvas.getContext('2d');
        const particles = [];
        let animationId = null;

        function resizeCanvas() {
          canvas.width = window.innerWidth;
          canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        function createParticle() {
          const colors = ['#D8A7B1', '#C9A66B', '#4A2C3A', '#FAF6F1'];
          const color = colors[Math.floor(Math.random() * colors.length)];
          const size = Math.random() * 8 + 4;
          const x = Math.random() * canvas.width;
          const y = canvas.height + size;
          const fallingSpeed = Math.random() * 2 + 1;
          const rotation = Math.random() * 360;
          const spinSpeed = (Math.random() - 0.5) * 2;

          return {
            x,
            y,
            size,
            fallingSpeed,
            rotation,
            spinSpeed,
            color,
            opacity: 1
          };
        }

        function animateConfetti() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          particles.forEach((p, i) => {
            p.y -= p.fallingSpeed;
            p.rotation += p.spinSpeed;
            p.opacity -= 0.01;

            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rotation * Math.PI / 180);
            ctx.globalAlpha = Math.max(0, p.opacity);
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.size / 2, -p.size / 4, p.size, p.size / 2);
            ctx.restore();
          });

          // Remove finished particles
          particles.forEach((p, i) => {
            if (p.y < -10 || p.opacity <= 0) {
              particles.splice(i, 1);
            }
          });

          if (particles.length > 0) {
            animationId = requestAnimationFrame(animateConfetti);
          } else {
            cancelAnimationFrame(animationId);
          }
        }

        function triggerConfetti() {
          // Create a burst of particles
          const burstCount = 50;
          for (let i = 0; i < burstCount; i++) {
            particles.push(createParticle());
          }

          animateConfetti();
        }

        // Button click
        const confettiBtn = document.getElementById('confettiBtn');
        confettiBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          triggerConfetti();

          // Reset after animation
          setTimeout(() => {
            particles.length = 0;
            cancelAnimationFrame(animationId);
            ctx.clearRect(0, 0, canvas.width, canvas.height);
          }, 3000);
        });

        // Also trigger on page load for fun (but respect reduced motion)
        if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          setTimeout(() => {
            triggerConfetti();
          }, 3000);
        }
      }

      // ==============================================================
      // Initialization
      // ==============================================================
      document.getElementById('passwordInput').focus();

      // Respect prefers-reduced-motion for confetti
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        const style = document.createElement('style');
        style.textContent = '#confettiBtn { display: none; }';
        document.head.appendChild(style);
      }
  </script>
</body>
</html>