# B2B Stage · web

Sitio estático (HTML + CSS + JS, sin build). Se publica en GitHub Pages con cada push a `main`.

## Ver en local

    python3 -m http.server 4321 --directory site

y abrir http://localhost:4321

## Estructura

- `index.html`: portada con vídeo, credenciales, quiénes somos y cifras, servicios (hospitality, logística y producción), trayectoria, galería "Desde dentro", método, equipo, valores y contacto.
- `styles.css`: paleta de marca (azul #2219CC del logo, hueso #E3E2DE y negro), con tipografías Big Shoulders Display, Instrument Serif e Inter Tight.
- `main.js`: barra de progreso e índice de secciones, animaciones de entrada, parallax, vídeos verticales que solo se reproducen al verse, galería arrastrable y formulario.
- `assets/`: fotos y vídeos sacados de `content/b2b-approved-content` y optimizados.

## Pendiente antes de publicar en el dominio real

- Confirmar el rol exacto en cada proyecto de Trayectoria (La Patrona, Palma Concert Series, Grup Trui) y los años que faltan.
- Confirmar las cifras (20+ artistas, 6 venues, 9 ciudades, 2 continentes).
- Legales: aviso legal, privacidad y cookies, con la sociedad que presta el servicio. Nombre del holding para "Una compañía de […]".
- Unificar el email (info@ en la web, alba@ en el dossier).
- Versión en inglés.
- Testimonios reales de tour managers y promotores.
- Conectar el formulario a un servicio (Formspree, etc.); ahora abre el correo del visitante.
- Dominio propio: quitar `noindex`, añadir canonical y sitemap.
