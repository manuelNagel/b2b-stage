(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  // Nav: solid on scroll + mobile menu
  const nav = $('#nav');
  const burger = $('.nav__burger');
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

  // Scroll progress bar + section index
  const bar = $('.progress span');
  const sideLinks = $$('.sidenav a');
  const count = $('.sidenav__count b');
  const sections = sideLinks.map(a => a.getAttribute('href') === '#top' ? $('.hero') : $(a.getAttribute('href')));
  const onScroll = () => {
    nav.classList.toggle('is-scrolled', scrollY > 40);
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = `scaleX(${max > 0 ? Math.min(scrollY / max, 1) : 0})`;
    let current = 0;
    sections.forEach((s, i) => { if (s && s.getBoundingClientRect().top <= innerHeight * .4) current = i; });
    sideLinks.forEach((a, i) => {
      a.classList.toggle('is-active', i === current);
      a.classList.toggle('is-past', i < current);
    });
    if (count) count.textContent = String(current + 1).padStart(2, '0');
  };
  let ticking = false;
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { onScroll(); ticking = false; }); } }, { passive: true });
  addEventListener('resize', onScroll);
  onScroll();

  // Reveal on scroll, staggered per batch
  const io = new IntersectionObserver(entries => {
    entries.filter(e => e.isIntersecting).forEach((e, i) => {
      e.target.style.transitionDelay = `${Math.min(i * 80, 400)}ms`;
      e.target.classList.add('is-in');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -10% 0px' });
  $$('.reveal').forEach(el => io.observe(el));

  // Parallax
  const para = $$('.parallax');
  if (!reduce && para.length) {
    let pTicking = false;
    const update = () => {
      para.forEach(fig => {
        const r = fig.getBoundingClientRect();
        if (r.bottom < 0 || r.top > innerHeight) return;
        const offset = (r.top + r.height / 2 - innerHeight / 2) * +fig.dataset.speed;
        fig.querySelector('img').style.transform = `translate3d(0, ${offset - r.height * .07}px, 0)`;
      });
      pTicking = false;
    };
    addEventListener('scroll', () => { if (!pTicking) { pTicking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  // Vertical clips: only play while visible
  const vio = new IntersectionObserver(entries => {
    entries.forEach(e => {
      const v = e.target;
      if (e.isIntersecting && !reduce) {
        if (v.preload === 'none') v.preload = 'auto';
        v.play().catch(() => {});
      } else {
        v.pause();
      }
    });
  }, { threshold: .4 });
  $$('[data-lazy-video]').forEach(v => vio.observe(v));

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

  // Contact form: validates and opens the user's mail client (static site, no backend)
  const en = document.documentElement.lang === 'en';
  const t = en
    ? { invalid: 'Please check your name, email and the privacy box.', sent: 'Thanks. Your email app is opening with the message ready to send.', subject: 'Website contact', name: 'Name', company: 'Company', role: 'Role' }
    : { invalid: 'Revisa nombre, email y la casilla de privacidad, por favor.', sent: 'Gracias. Abrimos tu correo con el mensaje listo para enviar.', subject: 'Contacto web', name: 'Nombre', company: 'Empresa', role: 'Rol' };
  const form = $('#contact-form');
  const note = $('.form__note', form);
  form.addEventListener('submit', e => {
    e.preventDefault();
    let ok = true;
    $$('[required]', form).forEach(i => {
      const bad = i.type === 'checkbox' ? !i.checked
        : !i.value.trim() || (i.type === 'email' && !/^\S+@\S+\.\S+$/.test(i.value));
      (i.type === 'checkbox' ? i.closest('label') : i).classList.toggle('is-invalid', bad);
      if (bad) ok = false;
    });
    if (!ok) { note.textContent = t.invalid; return; }
    const d = Object.fromEntries(new FormData(form));
    const subject = `${t.subject} · ${d.nombre}${d.empresa ? ' · ' + d.empresa : ''}`;
    const body = [
      `${t.name}: ${d.nombre}`,
      `Email: ${d.email}`,
      `${t.company}: ${d.empresa || '-'}`,
      `${t.role}: ${d.rol || '-'}`,
      '',
      d.mensaje || ''
    ].join('\n');
    location.href = `mailto:info@back2backstage.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    note.textContent = t.sent;
  });

  $('#year').textContent = new Date().getFullYear();
})();
