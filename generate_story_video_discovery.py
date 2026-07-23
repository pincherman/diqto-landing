#!/usr/bin/env python3
"""Generate canonical watch pages and the video sitemap for Diqto stories."""
from __future__ import annotations

import argparse
import difflib
import json
from dataclasses import dataclass
from html import escape
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


ROOT = Path(__file__).resolve().parent
WATCH_DIR = ROOT / "histoires"
VIDEO_SITEMAP = ROOT / "video-sitemap.xml"
BASE_URL = "https://diqto.fr"
UPLOAD_DATE = "2026-07-17T12:55:17+00:00"


@dataclass(frozen=True)
class Story:
    slug: str
    title: str
    heading: str
    description: str
    eyebrow: str
    summary: str
    details: tuple[str, ...]
    transcript: tuple[str, ...]
    related_url: str
    related_label: str

    @property
    def watch_url(self) -> str:
        return f"{BASE_URL}/histoires/{self.slug}.html"

    @property
    def video_url(self) -> str:
        return f"{BASE_URL}/assets/stories/{self.slug}.mp4"

    @property
    def thumbnail_url(self) -> str:
        return f"{BASE_URL}/assets/stories/{self.slug}-poster.jpg"

    @property
    def captions_url(self) -> str:
        return f"/assets/stories/{self.slug}-fr.vtt"


STORIES = (
    Story(
        slug="marc-artisan",
        title="Créer un devis sur chantier avec la voix | Film Diqto",
        heading="Marc finit son devis avant de quitter le chantier.",
        description=(
            "Film Diqto de 30 secondes : un artisan dicte les travaux réalisés, "
            "relit son devis puis prépare la facture sans tout ressaisir."
        ),
        eyebrow="Artisan · chantier · devis vocal",
        summary=(
            "Les mesures, matériaux et détails sont encore frais. Marc les dicte "
            "avant de repartir, puis garde la main sur le devis et la facture."
        ),
        details=(
            "Dicter le travail réalisé pendant qu'il est encore en mémoire.",
            "Retrouver un devis préparé à relire plutôt qu'une page vide.",
            "Transformer le devis en facture sans ressaisir les mêmes informations.",
            "Valider chaque étape avant un partage ou une transmission.",
        ),
        transcript=(
            "Sur son chantier, Marc pense au travail bien fait et à la confiance de ses clients.",
            "En partant, il dicte à Diqto ce qu'il a réalisé. Le devis prend forme. Il relit et valide.",
            "Puis il le transforme en facture, sans ressaisie. Diqto prépare les informations utiles.",
            "Rien ne part sans son accord. Moins de paperasse. Plus de terrain.",
        ),
        related_url="/plombier.html",
        related_label="Voir le parcours artisan",
    ),
    Story(
        slug="claire-osteopathe",
        title="Compte rendu après une séance d'ostéopathie | Film Diqto",
        heading="Claire reste présente pour son patient, puis finit son administratif.",
        description=(
            "Film Diqto de 30 secondes : une ostéopathe dicte l'essentiel après "
            "la séance, relit son compte rendu et prépare sa note d'honoraires."
        ),
        eyebrow="Santé libérale · séance · honoraires",
        summary=(
            "Après la séance, Claire garde le fil clinique sans laisser "
            "l'administratif prendre la place de la relation avec le patient."
        ),
        details=(
            "Dicter l'essentiel juste après la séance.",
            "Relire et corriger le compte rendu avant de le conserver.",
            "Préparer les éléments de la note d'honoraires sans double saisie.",
            "Garder les informations sensibles et chaque partage sous contrôle.",
        ),
        transcript=(
            "Dans son cabinet, Claire a une priorité : prendre soin de son patient. Écouter. Observer. Rassurer.",
            "Après la séance, elle dicte l'essentiel à Diqto. Le compte rendu prend forme.",
            "Claire relit et valide. Diqto prépare la note d'honoraires et les pièces utiles.",
            "Rien ne part sans son accord. Moins d'administratif. Plus d'attention pour ses patients.",
        ),
        related_url="/osteopathe.html",
        related_label="Voir le parcours ostéopathe",
    ),
    Story(
        slug="sarah-avocate",
        title="Compte rendu, temps passé et honoraires d'avocat | Film Diqto",
        heading="Sarah garde son attention sur le dossier, pas sur la ressaisie.",
        description=(
            "Film Diqto de 30 secondes : une avocate reprend les faits, les "
            "diligences et le temps passé pour préparer son suivi et ses honoraires."
        ),
        eyebrow="Droit · rendez-vous · temps passé",
        summary=(
            "Sarah écoute son client pendant le rendez-vous. Ensuite, elle "
            "raconte les faits et la prochaine étape pendant que le contexte est frais."
        ),
        details=(
            "Reprendre les faits et diligences après le rendez-vous.",
            "Relier le temps passé au bon dossier.",
            "Préparer la note d'honoraires à partir du même fil de travail.",
            "Relire, corriger et décider avant toute action externe.",
        ),
        transcript=(
            "Face à son client, Sarah écoute, questionne et rassure. Toute son attention reste sur le dossier.",
            "Après le rendez-vous, elle raconte à Diqto les faits, les diligences et la prochaine étape.",
            "Son compte rendu prend forme. Le temps passé rejoint le dossier. Sa note d'honoraires se prépare.",
            "Sarah relit, corrige et valide. Rien ne part sans son accord.",
        ),
        related_url="/metiers/avocat.html",
        related_label="Voir le parcours avocate",
    ),
    Story(
        slug="jean-luc-karate",
        title="Gérer abonnements et cotisations d'un club de karaté | Film Diqto",
        heading="Jean-Luc suit les abonnements sans quitter le tatami des yeux.",
        description=(
            "Film Diqto de 30 secondes : un professeur de karaté organise ses "
            "formules, pratiquants, échéances et règlements tout en gardant la main."
        ),
        eyebrow="Enseignement · abonnements · cotisations",
        summary=(
            "Les enfants, adolescents et adultes n'ont pas les mêmes formules. "
            "Jean-Luc structure les règles puis suit les échéances sans tableur dispersé."
        ),
        details=(
            "Créer des formules adaptées aux groupes et niveaux.",
            "Affecter chaque pratiquant à la bonne formule.",
            "Suivre échéances, facturation et règlements pendant l'année.",
            "Traiter les exceptions manuellement quand la situation l'exige.",
        ),
        transcript=(
            "Au karaté, le geste juste demande toute l'attention de Jean-Luc.",
            "Mais enfants, adolescents et adultes n'ont ni les mêmes niveaux, ni les mêmes abonnements.",
            "Avec Diqto, il crée chaque formule, définit ses règles, puis l'affecte au pratiquant.",
            "Les échéances, la facturation et les règlements sont suivis. Jean-Luc garde la main sur les exceptions.",
        ),
        related_url="/metiers/prof_karate.html",
        related_label="Voir le parcours professeur de karaté",
    ),
)


def structured_data(story: Story) -> str:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "VideoObject",
                "name": story.heading,
                "description": story.description,
                "thumbnailUrl": [story.thumbnail_url],
                "uploadDate": UPLOAD_DATE,
                "duration": "PT30S",
                "contentUrl": story.video_url,
                "url": story.watch_url,
                "inLanguage": "fr-FR",
                "isFamilyFriendly": True,
                "transcript": " ".join(story.transcript),
                "publisher": {
                    "@type": "Organization",
                    "name": "DIQTO",
                    "url": f"{BASE_URL}/",
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Accueil",
                        "item": f"{BASE_URL}/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Histoires",
                        "item": f"{BASE_URL}/histoires.html",
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": story.heading,
                        "item": story.watch_url,
                    },
                ],
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def render_page(story: Story) -> str:
    detail_items = "\n".join(
        f"            <li>{escape(item)}</li>" for item in story.details
    )
    transcript = "\n".join(
        f"          <p>{escape(paragraph)}</p>" for paragraph in story.transcript
    )
    schema = structured_data(story)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#0c0c0c">
<title>{escape(story.title)}</title>
<meta name="description" content="{escape(story.description, quote=True)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1">
<link rel="canonical" href="{story.watch_url}">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/site-shell.css">
<link rel="stylesheet" href="/story-watch.css">
<script defer src="/site-shell.js"></script>
<meta property="og:type" content="video.other">
<meta property="og:url" content="{story.watch_url}">
<meta property="og:title" content="{escape(story.heading, quote=True)}">
<meta property="og:site_name" content="Diqto">
<meta property="og:description" content="{escape(story.description, quote=True)}">
<meta property="og:image" content="{story.thumbnail_url}">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="720">
<meta property="og:video" content="{story.video_url}">
<meta property="og:video:type" content="video/mp4">
<meta property="og:video:width" content="1280">
<meta property="og:video:height" content="720">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="player">
<meta name="twitter:title" content="{escape(story.heading, quote=True)}">
<meta name="twitter:description" content="{escape(story.description, quote=True)}">
<meta name="twitter:image" content="{story.thumbnail_url}">
<script type="application/ld+json">
{schema}
</script>
</head>
<body>
<a class="global-skip-link" href="#contenu">Aller au contenu</a>
<header class="global-header" data-menu-open="false">
  <div class="global-nav">
    <a class="global-brand" href="/" aria-label="Diqto, accueil">
      <span class="global-brand-mark" aria-hidden="true">
        <i></i><i></i><i></i><i></i><i></i>
      </span>
      <span class="global-brand-name">diq<em>to</em></span>
    </a>
    <button class="global-menu-toggle" type="button" aria-expanded="false" aria-controls="navigation-principale">Menu</button>
    <nav class="global-menu" id="navigation-principale" aria-label="Navigation principale">
      <a href="/">Accueil</a>
      <a href="/fonctionnalites.html">Fonctionnalités</a>
      <a href="/histoires.html" aria-current="page">Histoires</a>
      <a href="/metiers.html">Métiers</a>
      <a href="/guides.html">Guides</a>
      <a href="/#tarifs">Tarifs</a>
      <a class="global-cta" href="/?source=seo_video_{story.slug}#beta">Commencer gratuit</a>
    </nav>
  </div>
</header>
<main id="contenu">
  <div class="watch-container">
    <nav class="watch-breadcrumbs" aria-label="Fil d'Ariane">
      <a href="/">Accueil</a><span>›</span>
      <a href="/histoires.html">Histoires</a><span>›</span>Film
    </nav>
  </div>
  <header class="watch-hero">
    <div class="watch-container">
      <p class="watch-eyebrow">{escape(story.eyebrow)}</p>
      <h1>{escape(story.heading)}</h1>
      <p class="watch-lead">{escape(story.summary)}</p>
      <p class="watch-disclosure">Film de 30 secondes · Personnage et situation fictifs · Écrans Diqto sur données de démonstration.</p>
    </div>
  </header>
  <div class="watch-container">
    <div class="watch-player">
      <video controls preload="metadata" playsinline poster="/assets/stories/{story.slug}-poster.jpg" aria-label="{escape(story.heading, quote=True)}">
        <source src="/assets/stories/{story.slug}.mp4" type="video/mp4">
        <track kind="captions" src="{story.captions_url}" srclang="fr" label="Français" default>
        Votre navigateur ne permet pas de lire cette vidéo.
      </video>
    </div>
  </div>
  <div class="watch-container watch-main">
    <div class="watch-grid">
      <div>
        <section class="watch-section">
          <h2>Ce que montre ce film</h2>
          <ul>
{detail_items}
          </ul>
        </section>
        <section class="watch-section">
          <h2>Le principe Diqto</h2>
          <p>La voix ou le texte sert à préparer un brouillon utile. Le professionnel relit, corrige et décide. Aucun document, paiement ou message ne part simplement parce que Diqto a préparé une base.</p>
        </section>
        <section class="watch-section">
          <h2>Transcription de la vidéo</h2>
          <details class="watch-transcript">
            <summary>Lire la transcription complète</summary>
{transcript}
          </details>
        </section>
      </div>
      <aside class="watch-aside">
        <h2>Voir le parcours complet</h2>
        <p>Retrouvez les documents, les contrôles et les limites présentés pour ce métier.</p>
        <div class="watch-actions">
          <a class="watch-button" href="{story.related_url}">{escape(story.related_label)}</a>
          <a class="watch-button secondary" href="/?source=seo_video_{story.slug}#beta">Créer un brouillon gratuit</a>
          <a class="watch-button secondary" href="/histoires.html">Voir les quatre films</a>
        </div>
      </aside>
    </div>
  </div>
</main>
<footer class="watch-footer">
  <div class="watch-container">
    <nav aria-label="Navigation de pied de page">
      <span>© 2026 Diqto</span>
      <a href="/">Accueil</a>
      <a href="/histoires.html">Histoires</a>
      <a href="/facturation-electronique.html">Facturation électronique</a>
      <a href="/guides.html">Guides</a>
      <a href="/confidentialite.html">Confidentialité</a>
    </nav>
  </div>
</footer>
</body>
</html>
"""


def render_video_sitemap() -> str:
    entries = []
    for story in STORIES:
        entries.append(
            "  <url>\n"
            f"    <loc>{xml_escape(story.watch_url)}</loc>\n"
            "    <video:video>\n"
            f"      <video:thumbnail_loc>{xml_escape(story.thumbnail_url)}</video:thumbnail_loc>\n"
            f"      <video:title>{xml_escape(story.heading)}</video:title>\n"
            f"      <video:description>{xml_escape(story.description)}</video:description>\n"
            f"      <video:content_loc>{xml_escape(story.video_url)}</video:content_loc>\n"
            "      <video:duration>30</video:duration>\n"
            "      <video:family_friendly>yes</video:family_friendly>\n"
            "      <video:live>no</video:live>\n"
            "    </video:video>\n"
            "  </url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


def write_or_check(path: Path, content: str, check: bool) -> bool:
    if check:
        actual = path.read_text(encoding="utf-8") if path.exists() else ""
        if actual == content:
            return True
        diff = difflib.unified_diff(
            actual.splitlines(),
            content.splitlines(),
            fromfile=str(path),
            tofile=f"generated:{path.name}",
            lineterm="",
        )
        print("\n".join(diff))
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    results = [
        write_or_check(WATCH_DIR / f"{story.slug}.html", render_page(story), args.check)
        for story in STORIES
    ]
    results.append(write_or_check(VIDEO_SITEMAP, render_video_sitemap(), args.check))
    if not all(results):
        return 1
    action = "check" if args.check else "generate"
    print(f"story_video_discovery_{action}: OK pages={len(STORIES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
