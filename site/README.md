# Back2backstage · web

Sitio estático (HTML + CSS + JS, sin build). Todo el contenido real de la web actual se mantiene: textos, 3 servicios, cifras, carta de Alba García, email y teléfono.

## Ver en local

    python3 -m http.server 4321 --directory site

y abrir http://localhost:4321

## Estructura

- `index.html` — todas las secciones: portada con vídeo, nosotros + cifras, servicios, artistas (Rels B, Shakira), por qué elegirnos, método, fundadora, galería, contacto.
- `styles.css` — paleta de marca (azul #2219CC del logo + hueso #E3E2DE + negro), tipografías Big Shoulders Display / Instrument Serif / Inter Tight.
- `main.js` — animaciones de entrada, contadores, parallax, preview de artistas al pasar el ratón, galería arrastrable, modal del reel y formulario.
- `assets/img` — fotos optimizadas desde `content/` (máx. 2000 px).
- `assets/video/hero.mp4` (20 s, sin audio) y `reel-relsb.mp4` (reel completo 1080p) generados desde `RelsB.mov`.

## Pendiente antes de publicar

- El formulario abre el correo del usuario (mailto). Para recibir envíos directos, conectar Formspree, Netlify Forms o similar.
- Confirmar qué créditos de artistas y fotos se pueden publicar (derechos de imagen de los fotógrafos).
- Añadir redes sociales si las hay.
- Publicable tal cual en Netlify, Vercel o Cloudflare Pages arrastrando la carpeta `site/`.
