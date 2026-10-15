"""Generate site/en/index.html from site/index.html.

The Spanish page is the source of truth. Each pair below swaps one Spanish
string for its English version; the script stops if a string is missing,
so edits to the Spanish copy surface here instead of silently leaving
Spanish text on the English page.

Run from the repo root:  python3 tools/build_en.py
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

PAIRS = [
    ('<html lang="es">', '<html lang="en">'),
    ('<title>B2B Stage · Hospitality, logística y producción para artistas</title>',
     '<title>B2B Stage · Artist hospitality, logistics &amp; production in Spain</title>'),
    ('content="B2B Stage: hospitality, logística y producción del lado del artista para conciertos, giras, festivales y espacios de marca. Desde Mallorca, en toda España."',
     'content="B2B Stage: artist-side hospitality, logistics and production for concerts, tours, festivals and brand spaces. Based in Mallorca, working across Spain."'),
    ('content="B2B Stage · Todo lo que el público no ve, hecho impecable"',
     'content="B2B Stage · Everything the audience never sees, done flawlessly"'),
    ('content="Hospitality, logística y producción del lado del artista. Desde Mallorca, en toda España."',
     'content="Artist-side hospitality, logistics and production. Based in Mallorca, working across Spain."'),
    ('<!-- Preview en GitHub Pages: quitar noindex al publicar en el dominio real -->',
     '<!-- GitHub Pages preview: remove noindex when publishing on the real domain -->'),
    ('<link rel="alternate" hreflang="es" href="./">\n  <link rel="alternate" hreflang="en" href="en/">',
     '<link rel="alternate" hreflang="es" href="../">\n  <link rel="alternate" hreflang="en" href="./">'),
    ('"description": "Hospitality, logística y producción del lado del artista para conciertos, giras, festivales y espacios de marca."',
     '"description": "Artist-side hospitality, logistics and production for concerts, tours, festivals and brand spaces."'),

    # Navigation
    ('aria-label="B2B Stage, inicio"', 'aria-label="B2B Stage, home"'),
    ('aria-label="Principal"', 'aria-label="Main"'),
    ('<a href="#quienes">Quiénes somos</a>\n      <a href="#servicios">Servicios</a>\n      <a href="#trayectoria">Trayectoria</a>\n      <a href="#metodo">Método</a>\n      <a href="#contacto" class="btn btn--small">Contacto</a>',
     '<a href="#quienes">About</a>\n      <a href="#servicios">Services</a>\n      <a href="#trayectoria">Track record</a>\n      <a href="#metodo">Method</a>\n      <a href="#contacto" class="btn btn--small">Contact</a>'),
    ('<div class="lang" aria-label="Idioma"><a href="./" aria-current="true" lang="es">ES</a><a href="en/" lang="en" hreflang="en">EN</a></div>',
     '<div class="lang" aria-label="Language"><a href="../" lang="es" hreflang="es">ES</a><a href="./" aria-current="true" lang="en">EN</a></div>'),
    ('aria-label="Abrir menú"', 'aria-label="Open menu"'),
    ('aria-label="Secciones"', 'aria-label="Sections"'),
    ('<li><a href="#top"><span>Inicio</span></a></li>', '<li><a href="#top"><span>Home</span></a></li>'),
    ('<li><a href="#quienes"><span>Quiénes somos</span></a></li>', '<li><a href="#quienes"><span>About</span></a></li>'),
    ('<li><a href="#servicios"><span>Servicios</span></a></li>', '<li><a href="#servicios"><span>Services</span></a></li>'),
    ('<li><a href="#trayectoria"><span>Trayectoria</span></a></li>', '<li><a href="#trayectoria"><span>Track record</span></a></li>'),
    ('<li><a href="#metodo"><span>Método</span></a></li>', '<li><a href="#metodo"><span>Method</span></a></li>'),
    ('<li><a href="#equipo"><span>Equipo y valores</span></a></li>', '<li><a href="#equipo"><span>Team &amp; values</span></a></li>'),
    ('<li><a href="#contacto"><span>Contacto</span></a></li>', '<li><a href="#contacto"><span>Contact</span></a></li>'),

    # Hero
    ('<p class="eyebrow intro">Hospitality · Logística · Producción</p>',
     '<p class="eyebrow intro">Hospitality · Logistics · Production</p>'),
    ('<span class="line"><span>Todo lo que</span></span>\n          <span class="line"><span>el público no ve,</span></span>\n          <span class="line"><span><em>hecho impecable.</em></span></span>',
     '<span class="line"><span>Everything the</span></span>\n          <span class="line"><span>audience never sees,</span></span>\n          <span class="line"><span><em>done flawlessly.</em></span></span>'),
    ('<p>Hospitality, logística y producción del lado del artista para conciertos, giras, festivales y espacios de marca. Desde Mallorca, en toda España.</p>',
     '<p>Artist-side hospitality, logistics and production for concerts, tours, festivals and brand spaces. Based in Mallorca, working across Spain.</p>'),
    ('Conócenos <span', 'About us <span'),
    ('>Ver trayectoria</a>', '>See our work</a>'),
    ('<div class="hero__caption">Palma, noche de concierto</div>', '<div class="hero__caption">Palma, concert night</div>'),

    # Credentials
    ('aria-label="Artistas y venues"', 'aria-label="Artists and venues"'),
    ('<p class="creds__venues container">En <b>', '<p class="creds__venues container">At <b>'),

    # About
    ('alt="Estadio con el escenario montado y sillas en el césped, horas antes del concierto"',
     'alt="Stadium with the stage built and chairs on the pitch, hours before the concert"'),
    ('<figcaption>Estadio, horas antes de abrir puertas</figcaption>', '<figcaption>Stadium, hours before doors open</figcaption>'),
    ('01 — Quiénes somos', '01 — About us'),
    ('Nadie aplaude un transfer puntual. <em>Por eso existimos.</em>',
     'Nobody applauds an on-time transfer. <em>That’s why we exist.</em>'),
    ('Somos el equipo que trabaja donde no llegan los focos: del primer rider al último cierre de puertas.',
     'We’re the team working where the spotlight doesn’t reach: from the first rider to the last door closing.'),
    ('<dt>Artistas atendidos</dt>', '<dt>Artists looked after</dt>'),
    ('<dt>Ciudades de gira</dt>', '<dt>Tour cities</dt>'),
    ('<dt>Continentes</dt>', '<dt>Continents</dt>'),
    ('alt="Camerino preparado con sofás, catering y burro de vestuario"',
     'alt="Dressing room set up with sofas, catering and a wardrobe rail"'),
    ('<figcaption>Camerino, antes de la llegada</figcaption>', '<figcaption>Dressing room, before arrival</figcaption>'),
    ('alt="Dos miembros del equipo con walkie en un espacio de marca"',
     'alt="Two crew members with walkie-talkies in a brand space"'),
    ('<figcaption>Equipo en operación</figcaption>', '<figcaption>Crew at work</figcaption>'),
    ('alt="Miembro del equipo con acreditación junto a la valla del público"',
     'alt="Crew member with a pass by the crowd barrier"'),

    # Services
    ('02 — Servicios', '02 — Services'),
    ('Un solo pase. <br><em>Todas las puertas.</em>', 'One pass. <br><em>Every door.</em>'),
    ('Tu equipo produce el show; nosotros, todo lo que rodea al artista. Un interlocutor, tres áreas.',
     'Your team produces the show; we handle everything around the artist. One contact, three areas.'),
    ('“Que el artista se sienta en casa.”', '“Make the artist feel at home.”'),
    ('<li>Camerinos según rider</li>', '<li>Dressing rooms to rider</li>'),
    ('<li>Catering de artista y equipo</li>', '<li>Artist and crew catering</li>'),
    ('<li>Backstage bar y zonas VIP</li>', '<li>Backstage bar and VIP areas</li>'),
    ('<li>Guest lists y acreditaciones</li>', '<li>Guest lists and accreditation</li>'),
    ('<li>Meet &amp; greet y sponsors</li>', '<li>Meet &amp; greets and sponsors</li>'),
    ('<h3>Logística</h3>', '<h3>Logistics</h3>'),
    ('“Cada trayecto, en nuestras manos.”', '“Every journey, in our hands.”'),
    ('<li>Vuelos nacionales e internacionales</li>', '<li>Domestic and international flights</li>'),
    ('<li>Hoteles según rider</li>', '<li>Hotels to rider</li>'),
    ('<li>Transfers con flota de alta gama</li>', '<li>Transfers with a premium fleet</li>'),
    ('<li>Advancing con el tour manager</li>', '<li>Advancing with the tour manager</li>'),
    ('<li>Tour support y disponibilidad 24 h</li>', '<li>Tour support, available 24/7</li>'),
    ('<h3>Producción</h3>', '<h3>Production</h3>'),
    ('“Del plano al último cierre de puertas.”', '“From the floor plan to the last door closing.”'),
    ('<li>Planificación y hojas de ruta</li>', '<li>Planning and day sheets</li>'),
    ('<li>Montaje, pruebas, show y desmontaje</li>', '<li>Load-in, soundcheck, show and load-out</li>'),
    ('<li>Equipos y proveedores</li>', '<li>Crews and suppliers</li>'),
    ('<li>Gran formato en estadio</li>', '<li>Large-scale stadium shows</li>'),
    ('<li>Espacios de marca</li>', '<li>Brand spaces</li>'),

    # Track record
    ('03 — Trayectoria', '03 — Track record'),
    ('Hecho, <em>no prometido.</em>', 'Done, <em>not promised.</em>'),
    ('Una selección de proyectos recientes, con lo que hicimos en cada uno.',
     'A selection of recent projects, and what we did on each.'),
    ('<h3>Temporada de estadio</h3><p>Producción de gran formato en el Estadi Mallorca Son Moix.</p>',
     '<h3>Stadium season</h3><p>Large-scale production at Estadi Mallorca Son Moix.</p>'),
    ('<span class="case-row__tag">Producción</span>', '<span class="case-row__tag">Production</span>'),
    ('<h3>Kakkmaddafakka · Gira española</h3><p>Tour support en 9 ciudades.</p>',
     '<h3>Kakkmaddafakka · Spanish tour</h3><p>Tour support across 9 cities.</p>'),
    ('<span class="case-row__tag">Logística</span>', '<span class="case-row__tag">Logistics</span>'),
    ('<p>Tour support internacional.</p>', '<p>International tour support.</p>'),
    ('<p>Festival con Rudimental y John Newman.</p>', '<p>Festival with Rudimental and John Newman.</p>'),
    ('<p>Personal por zonas, mobiliario, proveedores, control de flujos e instalación Wolf Head.</p>',
     '<p>Zoned staffing, furniture, suppliers, crowd-flow control and the Wolf Head installation.</p>'),
    ('<p>Ciclo de conciertos en Palma.</p>', '<p>Concert series in Palma.</p>'),
    ('<span class="case-row__tag">Conciertos</span>', '<span class="case-row__tag">Concerts</span>'),

    # Behind the scenes rail
    ('Desde <em>dentro</em>', 'From <em>the inside</em>'),
    ('Arrastra o desliza <span', 'Drag or swipe <span'),
    ('aria-label="Galería desde dentro, desliza horizontalmente"', 'aria-label="Behind-the-scenes gallery, scroll horizontally"'),
    ('aria-label="Vídeo de un estadio lleno durante un concierto"', 'aria-label="Video of a full stadium during a concert"'),
    ('<figcaption>Estadio lleno</figcaption>', '<figcaption>Sold-out stadium</figcaption>'),
    ('aria-label="Vídeo de un DJ en cabina entre humo"', 'aria-label="Video of a DJ in the booth through smoke"'),
    ('<figcaption>Desde la cabina</figcaption>', '<figcaption>From the booth</figcaption>'),
    ('alt="Equipo dentro de un espacio de marca de colores"', 'alt="Crew inside a colourful brand space"'),
    ('<figcaption>Espacio de marca</figcaption>', '<figcaption>Brand space</figcaption>'),
    ('alt="Escenario iluminado en azul frente al público"', 'alt="Stage lit in blue in front of the crowd"'),
    ('aria-label="Vídeo de un recinto de festival al atardecer"', 'aria-label="Video of a festival site at sunset"'),
    ('<figcaption>Atardecer en recinto</figcaption>', '<figcaption>Sunset on site</figcaption>'),
    ('alt="Rels B en el escenario entre llamaradas"', 'alt="Rels B on stage between flames"'),
    ('aria-label="Vídeo del público frente al escenario"', 'aria-label="Video of the crowd in front of the stage"'),
    ('<figcaption>Público</figcaption>', '<figcaption>Crowd</figcaption>'),
    ('alt="Vista aérea de un recinto con estructuras de colores y público"', 'alt="Aerial view of a site with colourful structures and crowd"'),
    ('alt="Estadio vacío visto desde un palco con el escenario montado al fondo"', 'alt="Empty stadium seen from a box, with the stage built at the far end"'),
    ('<figcaption>Montaje, visto desde el palco</figcaption>', '<figcaption>Build day, from the box</figcaption>'),
    ('aria-label="Vídeo de fuegos artificiales sobre el recinto"', 'aria-label="Video of fireworks over the site"'),
    ('<figcaption>Final de fiesta</figcaption>', '<figcaption>Grand finale</figcaption>'),
    ('alt="Estadi Mallorca Son Moix lleno de noche durante un concierto"', 'alt="Estadi Mallorca Son Moix full at night during a concert"'),
    ('alt="Arcos de colores con las letras de LATINA al anochecer"', 'alt="Colourful arches spelling LATINA at dusk"'),
    ('alt="Concierto junto a la catedral de Palma de noche"', 'alt="Concert by Palma cathedral at night"'),
    ('<figcaption>Recinto desde arriba</figcaption>', '<figcaption>Site from above</figcaption>'),
    ('alt="Equipo celebrando en el backstage"', 'alt="Crew celebrating backstage"'),
    ('<figcaption>Al cerrar puertas</figcaption>', '<figcaption>After doors close</figcaption>'),
    ('alt="Tipi iluminado en rojo de noche en un recinto"', 'alt="Tipi lit in red at night on site"'),
    ('<figcaption>Recinto, de noche</figcaption>', '<figcaption>Site at night</figcaption>'),
    ('alt="Público emocionado durante un concierto"', 'alt="Emotional crowd during a concert"'),
    ('<figcaption>Por esto lo hacemos</figcaption>', '<figcaption>Why we do it</figcaption>'),

    # Method
    ('04 — Método', '04 — Method'),
    ('Del rider <em>al aplauso.</em>', 'From rider <em>to applause.</em>'),
    ('Un solo equipo acompaña al artista desde el primer email hasta que se apagan las luces.',
     'One team stays with the artist from the first email until the lights go down.'),
    ('<h3>Briefing</h3><p>Rider y necesidades de artista, promotor y sponsors.</p>',
     '<h3>Briefing</h3><p>Rider and needs of artist, promoter and sponsors.</p>'),
    ('<h3>Propuesta</h3><p>Alcance, equipo y presupuesto, por escrito.</p>',
     '<h3>Proposal</h3><p>Scope, team and budget, in writing.</p>'),
    ('<h3>Preproducción</h3><p>Camerinos, viajes, proveedores y listas con horarios cerrados.</p>',
     '<h3>Pre-production</h3><p>Dressing rooms, travel, suppliers and lists, with fixed times.</p>'),
    ('<h3>Show day</h3><p>Coordinación en recinto y con el tour manager, 24 h.</p>',
     '<h3>Show day</h3><p>On-site coordination with the tour manager, 24/7.</p>'),
    ('<h3>Cierre</h3><p>Informe de accesos, incidencias y aprendizajes.</p>',
     '<h3>Wrap-up</h3><p>Report on access, incidents and lessons learned.</p>'),
    ('</svg>Disponibilidad 24 h</li>', '</svg>Available 24/7</li>'),
    ('</svg>Plan B antes que el problema</li>', '</svg>Plan B before the problem</li>'),
    ('</svg>NDA estándar y total confidencialidad</li>', '</svg>Standard NDA and full confidentiality</li>'),

    # Team
    ('05 — Equipo', '05 — Team'),
    ('“La música no llegó a mi vida, <em>yo llegué a la suya.</em>”',
     '“Music didn’t come into my life, <em>I came into its.</em>”'),
    ('Crecí entre escenarios y camerinos, en una familia donde el arte era el día a día. Desde pequeña entendí que la magia no solo ocurre en el escenario, sino también detrás de él.',
     'I grew up between stages and dressing rooms, in a family where art was everyday life. From a young age I understood that the magic doesn’t only happen on stage, but behind it too.'),
    ('Hoy, en B2B Stage, transformamos esa herencia en una forma de trabajar: cuidar cada detalle para que los artistas se sientan comprendidos y en casa, allí donde el show empieza.',
     'Today, at B2B Stage, we’ve turned that heritage into a way of working: caring for every detail so artists feel understood and at home, right where the show begins.'),
    ('<span>Responsable de B2B Stage</span>', '<span>Head of B2B Stage</span>'),

    # Values
    ('reveal">Valores</p>', 'reveal">Values</p>'),
    ('Cuando el artista está bien, <em>el show es mejor.</em>', 'When the artist is well, <em>the show is better.</em>'),
    ('<h3>Cuidado</h3><p>El rider se cumple, entero.</p>', '<h3>Care</h3><p>The rider gets met, all of it.</p>'),
    ('<h3>Discreción</h3><p>Lo que pasa en el camerino se queda en el camerino.</p>',
     '<h3>Discretion</h3><p>What happens in the dressing room stays in the dressing room.</p>'),
    ('<h3>Anticipación</h3><p>El plan B existe antes que el problema.</p>',
     '<h3>Foresight</h3><p>Plan B exists before the problem does.</p>'),
    ('<h3>Oficio</h3><p>Venimos de la industria y hablamos su idioma.</p>',
     '<h3>Craft</h3><p>We come from the industry and speak its language.</p>'),
    ('<h3>Respeto</h3><p>Por artistas, equipos y proveedores.</p>', '<h3>Respect</h3><p>For artists, crews and suppliers.</p>'),

    # Contact
    ('06 — Contacto', '06 — Contact'),
    ('Hablemos de lo <em>que hay detrás.</em>', 'Let’s talk about <em>what’s behind it.</em>'),
    ('<p class="reveal">Respondemos en menos de 24 horas.</p>', '<p class="reveal">We reply within 24 hours.</p>'),
    ('<li><span>Teléfono</span>', '<li><span>Phone</span>'),
    ('<label><span>Nombre</span>', '<label><span>Name</span>'),
    ('<label><span>Empresa</span>', '<label><span>Company</span>'),
    ('<label><span>Rol</span><input name="rol" placeholder="Promotor, tour manager, venue…"',
     '<label><span>Role</span><input name="rol" placeholder="Promoter, tour manager, venue…"'),
    ('<label><span>Mensaje</span>', '<label><span>Message</span>'),
    ('Acepto que B2B Stage use estos datos solo para responder a mi mensaje.',
     'I agree that B2B Stage may use this data only to reply to my message.'),
    ('Enviar <span aria-hidden="true">→</span></button>', 'Send <span aria-hidden="true">→</span></button>'),

    # Footer
    ('<div><span>Contacto</span>', '<div><span>Contact</span>'),
    ('<div><span>Servicios</span><a href="#servicios">Hospitality</a><a href="#servicios">Logística</a><a href="#servicios">Producción</a></div>',
     '<div><span>Services</span><a href="#servicios">Hospitality</a><a href="#servicios">Logistics</a><a href="#servicios">Production</a></div>'),
    ('<div><span>Compañía</span><a href="#quienes">Quiénes somos</a><a href="#trayectoria">Trayectoria</a><a href="#metodo">Método</a></div>',
     '<div><span>Company</span><a href="#quienes">About</a><a href="#trayectoria">Track record</a><a href="#metodo">Method</a></div>'),
    ('<span>Todo lo que el público no ve.</span>', '<span>Everything the audience never sees.</span>'),
]


def main():
    html = (SITE / "index.html").read_text()
    missing = [es for es, _ in PAIRS if es not in html]
    if missing:
        raise SystemExit("Spanish strings not found (update PAIRS):\n- " + "\n- ".join(m[:80] for m in missing))
    for es, en in PAIRS:
        html = html.replace(es, en)
    # The English page lives one folder down
    html = re.sub(r'(src|href|poster|content)="(assets/|styles\.css|main\.js)', r'\1="../\2', html)
    out = SITE / "en" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html)
    print(f"Wrote {out.relative_to(SITE.parent)}")


if __name__ == "__main__":
    main()
