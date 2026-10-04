(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  // Nav: solid on scroll + mobile menu
  const nav = $('#nav');
  const burger = $('.nav__burger');
  const onScroll = () => nav.classList.toggle('is-scrolled', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  $$('.nav__links a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('is-open');
    burger.setAttribute('aria-expanded', false);
    document.body.style.overflow = '';
  }));

  // Reveal on scroll, staggered per batch
  const io = new IntersectionObserver(entries => {
    entries.filter(e => e.isIntersecting).forEach((e, i) => {
      e.target.style.transitionDelay = `${Math.min(i * 80, 400)}ms`;
      e.target.classList.add('is-in');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -10% 0px' });
  $$('.reveal').forEach(el => io.observe(el));

  // Counters
  const fmt = n => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  const cio = new IntersectionObserver(entries => {
    entries.filter(e => e.isIntersecting).forEach(e => {
      const el = e.target, end = +el.dataset.count;
      cio.unobserve(el);
      if (reduce) { el.textContent = fmt(end); return; }
      const t0 = performance.now(), dur = 1800;
      const tick = t => {
        const p = Math.min((t - t0) / dur, 1);
        el.textContent = fmt(Math.round(end * (1 - Math.pow(1 - p, 4))));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }, { threshold: .6 });
  $$('[data-count]').forEach(el => cio.observe(el));

  // Parallax
  const para = $$('.parallax');
  if (!reduce && para.length) {
    let ticking = false;
    const update = () => {
      para.forEach(fig => {
        const r = fig.getBoundingClientRect();
        if (r.bottom < 0 || r.top > innerHeight) return;
        const offset = (r.top + r.height / 2 - innerHeight / 2) * +fig.dataset.speed;
        fig.querySelector('img').style.transform = `translate3d(0, ${offset - r.height * .07}px, 0)`;
      });
      ticking = false;
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  // Artist names: floating image preview that follows the cursor
  const preview = $('.name-preview');
  const pImg = preview && preview.querySelector('img');
  if (preview && matchMedia('(hover: hover)').matches) {
    let x = 0, y = 0, cx = 0, cy = 0, raf;
    const loop = () => {
      cx += (x - cx) * .15; cy += (y - cy) * .15;
      preview.style.left = cx + 'px'; preview.style.top = cy + 'px';
      raf = requestAnimationFrame(loop);
    };
    $$('.name').forEach(n => {
      n.addEventListener('mouseenter', e => {
        pImg.src = n.dataset.img;
        x = cx = e.clientX; y = cy = e.clientY;
        preview.classList.add('is-on');
        cancelAnimationFrame(raf); loop();
      });
      n.addEventListener('mousemove', e => { x = e.clientX; y = e.clientY; });
      n.addEventListener('mouseleave', () => { preview.classList.remove('is-on'); setTimeout(() => cancelAnimationFrame(raf), 400); });
    });
  }

  // Drag-to-scroll rail
  const rail = $('.rail');
  if (rail) {
    let down = false, startX = 0, startLeft = 0;
    rail.addEventListener('pointerdown', e => {
      if (e.pointerType !== 'mouse') return;
      down = true; startX = e.clientX; startLeft = rail.scrollLeft;
      rail.classList.add('is-drag');
    });
    addEventListener('pointermove', e => { if (down) rail.scrollLeft = startLeft - (e.clientX - startX); });
    addEventListener('pointerup', () => { down = false; rail.classList.remove('is-drag'); });
  }

  // Reel modal
  const reel = $('#reel');
  const reelVideo = reel.querySelector('video');
  $$('[data-open-reel]').forEach(b => b.addEventListener('click', () => {
    reel.showModal();
    reelVideo.play().catch(() => {});
  }));
  const closeReel = () => { reelVideo.pause(); reel.close(); };
  $('.reel__close').addEventListener('click', closeReel);
  reel.addEventListener('click', e => { if (e.target === reel) closeReel(); });
  reel.addEventListener('close', () => reelVideo.pause());

  // Contact form: validates and opens the user's mail client (static site, no backend)
  const form = $('#contact-form');
  const note = $('.form__note', form);
  form.addEventListener('submit', e => {
    e.preventDefault();
    const required = $$('[required]', form);
    let ok = true;
    required.forEach(i => {
      const bad = !i.value.trim() || (i.type === 'email' && !/^\S+@\S+\.\S+$/.test(i.value));
      i.classList.toggle('is-invalid', bad);
      if (bad) ok = false;
    });
    if (!ok) { note.textContent = 'Revisa nombre y email, por favor.'; return; }
    const d = Object.fromEntries(new FormData(form));
    const subject = `Solicitud de información · ${d.tipo} · ${d.nombre} ${d.apellido}`.trim();
    const body = [
      `Nombre: ${d.nombre} ${d.apellido}`,
      `Email: ${d.email}`,
      `Teléfono: ${d.telefono || '-'}`,
      `Tipo de evento: ${d.tipo}`,
      `Fecha aproximada: ${d.fecha || '-'}`,
      '',
      d.mensaje || ''
    ].join('\n');
    location.href = `mailto:info@back2backstage.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    note.textContent = 'Gracias. Abrimos tu correo con la solicitud lista para enviar.';
  });

  $('#year').textContent = new Date().getFullYear();
})();
