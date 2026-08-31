"""Canonical campaign-video metadata shared by métier pages and sitemaps."""
from __future__ import annotations

import json
from dataclasses import dataclass
from html import escape


BASE_URL = "https://diqto.fr"


@dataclass(frozen=True)
class CaptionCue:
    start: str
    end: str
    text: str


@dataclass(frozen=True)
class CampaignVideo:
    trade_id: str
    page_path: str
    heading: str
    description: str
    summary: str
    video_path: str
    poster_path: str
    captions_path: str
    sha256: str
    transcript: tuple[str, ...]
    cues: tuple[CaptionCue, ...]
    duration_seconds: int = 40
    width: int = 1080
    height: int = 1920
    upload_date: str = "2026-08-31T03:00:00+00:00"

    @property
    def page_url(self) -> str:
        return f"{BASE_URL}{self.page_path}"

    @property
    def video_url(self) -> str:
        return f"{BASE_URL}{self.video_path}"

    @property
    def poster_url(self) -> str:
        return f"{BASE_URL}{self.poster_path}"

    @property
    def transcript_text(self) -> str:
        return " ".join(self.transcript)


def cue(start: str, end: str, text: str) -> CaptionCue:
    return CaptionCue(start=start, end=end, text=text)


CAMPAIGN_VIDEOS = (
    CampaignVideo(
        trade_id="plombier",
        page_path="/plombier.html",
        heading="Du devis au paiement : le cas concret d'un plombier",
        description=(
            "Film Diqto de 40 secondes pour plombiers : dicter les travaux, "
            "préparer le devis, reprendre les changements et préparer la facture "
            "sans tout ressaisir."
        ),
        summary=(
            "Le chantier est encore frais. Le plombier dicte ce qui est prévu, "
            "relit le devis, indique les changements puis garde la décision sur "
            "la facture et le paiement."
        ),
        video_path="/assets/campaign/diqto-plombier-devis-paiement.mp4",
        poster_path="/assets/campaign/diqto-plombier-devis-paiement-poster.jpg",
        captions_path="/assets/campaign/diqto-plombier-devis-paiement-fr.vtt",
        sha256="56a881f132c1f014a8573245a0008b8d132b548779f9077aca35f8edf6c4e16b",
        transcript=(
            "Chaque métier a son langage. La même simplicité : vous parlez, Diqto prépare. Prenons l'exemple du plombier : il suit son intervention, du devis au paiement.",
            "Une intervention sur un chantier ne devrait pas être saisie trois fois. Avant le chantier, vous dictez les travaux prévus, le matériel et les quantités.",
            "Diqto prépare le devis. Vous relisez et vous l'envoyez. Le chantier terminé, vous indiquez seulement ce qui a changé.",
            "Diqto reprend le devis, prépare la facture et les données utiles à la facturation électronique. Après votre validation, votre client peut la régler par un lien sécurisé.",
            "Du devis au paiement, sans tout ressaisir. Diqto. Vous dictez. Diqto prépare.",
        ),
        cues=(
            cue("00:00:00.000", "00:00:01.640", "Chaque métier a son langage."),
            cue("00:00:02.000", "00:00:04.800", "La même simplicité : vous parlez, Diqto prépare."),
            cue("00:00:05.740", "00:00:09.840", "Prenons l'exemple du plombier : il suit son intervention, du devis au paiement."),
            cue("00:00:10.960", "00:00:14.260", "Une intervention sur un chantier ne devrait pas être saisie trois fois."),
            cue("00:00:14.520", "00:00:18.580", "Avant le chantier, vous dictez les travaux prévus, le matériel et les quantités."),
            cue("00:00:18.860", "00:00:21.920", "Diqto prépare le devis. Vous relisez et vous l'envoyez."),
            cue("00:00:22.160", "00:00:25.260", "Le chantier terminé, vous indiquez seulement ce qui a changé."),
            cue("00:00:25.420", "00:00:30.540", "Diqto reprend le devis, prépare la facture et les données utiles à la facturation électronique."),
            cue("00:00:30.680", "00:00:34.660", "Après votre validation, votre client peut la régler par un lien sécurisé."),
            cue("00:00:34.860", "00:00:39.620", "Du devis au paiement, sans tout ressaisir. Diqto. Vous dictez. Diqto prépare."),
        ),
    ),
    CampaignVideo(
        trade_id="electricien",
        page_path="/electricien.html",
        heading="Du diagnostic au paiement : le cas concret d'un électricien",
        description=(
            "Film Diqto de 40 secondes pour électriciens : dicter le diagnostic "
            "et les travaux, préparer le devis puis la facture sans tout ressaisir."
        ),
        summary=(
            "Après avoir localisé le défaut, l'électricien dicte les travaux, "
            "le matériel et les quantités. Diqto prépare, le professionnel relit "
            "et conserve la décision finale."
        ),
        video_path="/assets/campaign/diqto-electricien-diagnostic-paiement.mp4",
        poster_path="/assets/campaign/diqto-electricien-diagnostic-paiement-poster.jpg",
        captions_path="/assets/campaign/diqto-electricien-diagnostic-paiement-fr.vtt",
        sha256="117ebdaf79ab0c03b8dc2d5a5b136a309b5e0ab63634c8d31d7f33832c19e2aa",
        transcript=(
            "Chaque métier a son langage. La même simplicité : vous parlez, Diqto prépare. Prenons l'exemple de l'électricien : il suit son intervention, du diagnostic au paiement.",
            "Un diagnostic électrique ne devrait pas finir en notes à ressaisir. Après avoir localisé le défaut, vous dictez les travaux à prévoir, le matériel et les quantités.",
            "Diqto prépare le devis. Vous le relisez et vous l'envoyez. L'intervention terminée, vous indiquez seulement ce qui a changé.",
            "Diqto reprend le devis, prépare la facture et les données utiles à la facturation électronique. Après votre validation, votre client peut la régler par un lien sécurisé.",
            "Du diagnostic au paiement, sans tout ressaisir. Diqto. Vous dictez. Diqto prépare.",
        ),
        cues=(
            cue("00:00:00.000", "00:00:01.640", "Chaque métier a son langage."),
            cue("00:00:01.860", "00:00:04.600", "La même simplicité : vous parlez, Diqto prépare."),
            cue("00:00:04.780", "00:00:09.080", "Prenons l'exemple de l'électricien : il suit son intervention, du diagnostic au paiement."),
            cue("00:00:10.720", "00:00:14.220", "Un diagnostic électrique ne devrait pas finir en notes à ressaisir."),
            cue("00:00:14.420", "00:00:19.040", "Après avoir localisé le défaut, vous dictez les travaux à prévoir, le matériel et les quantités."),
            cue("00:00:19.300", "00:00:22.240", "Diqto prépare le devis. Vous le relisez et vous l'envoyez."),
            cue("00:00:22.580", "00:00:25.380", "L'intervention terminée, vous indiquez seulement ce qui a changé."),
            cue("00:00:25.380", "00:00:30.480", "Diqto reprend le devis, prépare la facture et les données utiles à la facturation électronique."),
            cue("00:00:30.640", "00:00:34.160", "Après votre validation, votre client peut la régler par un lien sécurisé."),
            cue("00:00:34.400", "00:00:39.160", "Du diagnostic au paiement, sans tout ressaisir. Diqto. Vous dictez. Diqto prépare."),
        ),
    ),
    CampaignVideo(
        trade_id="couvreur",
        page_path="/metiers/couvreur.html",
        heading="De l'inspection au paiement : le cas concret d'un couvreur",
        description=(
            "Film Diqto de 40 secondes pour couvreurs : dicter les travaux de "
            "toiture, préparer le devis puis la facture sans tout ressaisir."
        ),
        summary=(
            "Tuiles, faîtage, gouttières et quantités restent dans le même fil. "
            "Le couvreur indique ce qui a changé, puis relit avant toute facture "
            "ou demande de paiement."
        ),
        video_path="/assets/campaign/diqto-couvreur-inspection-paiement.mp4",
        poster_path="/assets/campaign/diqto-couvreur-inspection-paiement-poster.jpg",
        captions_path="/assets/campaign/diqto-couvreur-inspection-paiement-fr.vtt",
        sha256="cfa86319c041210e21f04170337b1d54f32bc309bd35dd140c2f822857caf0c5",
        transcript=(
            "Chaque métier a son langage. La même simplicité : vous parlez, Diqto prépare. Prenons l'exemple du couvreur : il suit son intervention, de l'inspection au paiement.",
            "Une inspection de toiture ne devrait pas finir en notes à ressaisir. Avant les travaux, vous dictez les tuiles à remplacer, le faîtage, les gouttières et les quantités.",
            "Diqto prépare le devis. Vous le relisez et vous l'envoyez. La toiture réparée, vous indiquez seulement ce qui a changé.",
            "Diqto reprend le devis, prépare la facture et les données utiles à la facturation électronique. Après votre validation, votre client peut la régler par un lien sécurisé.",
            "De l'inspection au paiement, sans tout ressaisir. Diqto. Vous dictez. Diqto prépare.",
        ),
        cues=(
            cue("00:00:00.000", "00:00:01.620", "Chaque métier a son langage."),
            cue("00:00:01.620", "00:00:04.840", "La même simplicité : vous parlez, Diqto prépare."),
            cue("00:00:04.840", "00:00:09.220", "Prenons l'exemple du couvreur : il suit son intervention, de l'inspection au paiement."),
            cue("00:00:10.520", "00:00:13.900", "Une inspection de toiture ne devrait pas finir en notes à ressaisir."),
            cue("00:00:13.900", "00:00:18.780", "Avant les travaux, vous dictez les tuiles à remplacer, le faîtage, les gouttières et les quantités."),
            cue("00:00:18.780", "00:00:21.940", "Diqto prépare le devis. Vous le relisez et vous l'envoyez."),
            cue("00:00:21.940", "00:00:25.100", "La toiture réparée, vous indiquez seulement ce qui a changé."),
            cue("00:00:25.100", "00:00:30.060", "Diqto reprend le devis, prépare la facture et les données utiles à la facturation électronique."),
            cue("00:00:30.060", "00:00:33.980", "Après votre validation, votre client peut la régler par un lien sécurisé."),
            cue("00:00:33.980", "00:00:39.300", "De l'inspection au paiement, sans tout ressaisir. Diqto. Vous dictez. Diqto prépare."),
        ),
    ),
    CampaignVideo(
        trade_id="macon",
        page_path="/metiers/macon.html",
        heading="Du devis au paiement : le cas concret d'un maçon",
        description=(
            "Film Diqto de 40 secondes pour maçons : dicter le chantier, ajuster "
            "le devis quand les travaux changent puis préparer la facture."
        ),
        summary=(
            "Le chantier peut évoluer. Le maçon signale l'écart avant de "
            "poursuivre, ajuste le devis puis garde la main sur la facture et "
            "le paiement."
        ),
        video_path="/assets/campaign/diqto-macon-devis-paiement.mp4",
        poster_path="/assets/campaign/diqto-macon-devis-paiement-poster.jpg",
        captions_path="/assets/campaign/diqto-macon-devis-paiement-fr.vtt",
        sha256="c524916bf97b2f1557bb24818c9713abc008210dd027931e1eedd2d3598f3ead",
        transcript=(
            "Chaque métier a son langage. La même simplicité : vous parlez, Diqto prépare. Prenons l'exemple du maçon : il suit son chantier, du devis au paiement.",
            "Un chantier de maçonnerie ne se déroule pas toujours comme prévu. Avant de commencer, vous dictez les travaux, les matériaux et les quantités.",
            "Diqto prépare le devis. Vous le relisez et vous l'envoyez. Si le chantier change, vous indiquez l'écart avant de poursuivre. Diqto vous aide à ajuster le devis.",
            "Les travaux terminés, Diqto prépare la facture et les données utiles à la facturation électronique. Après votre validation, votre client peut la régler par un lien sécurisé.",
            "Du devis au paiement, sans tout ressaisir. Diqto. Vous dictez. Diqto prépare.",
        ),
        cues=(
            cue("00:00:00.000", "00:00:01.580", "Chaque métier a son langage."),
            cue("00:00:01.940", "00:00:04.960", "La même simplicité : vous parlez, Diqto prépare."),
            cue("00:00:05.280", "00:00:08.980", "Prenons l'exemple du maçon : il suit son chantier, du devis au paiement."),
            cue("00:00:10.560", "00:00:13.500", "Un chantier de maçonnerie ne se déroule pas toujours comme prévu."),
            cue("00:00:13.760", "00:00:17.120", "Avant de commencer, vous dictez les travaux, les matériaux et les quantités."),
            cue("00:00:17.400", "00:00:20.220", "Diqto prépare le devis. Vous le relisez et vous l'envoyez."),
            cue("00:00:20.460", "00:00:25.600", "Si le chantier change, vous indiquez l'écart avant de poursuivre. Diqto vous aide à ajuster le devis."),
            cue("00:00:25.600", "00:00:30.700", "Les travaux terminés, Diqto prépare la facture et les données utiles à la facturation électronique."),
            cue("00:00:30.940", "00:00:34.480", "Après votre validation, votre client peut la régler par un lien sécurisé."),
            cue("00:00:34.720", "00:00:39.220", "Du devis au paiement, sans tout ressaisir. Diqto. Vous dictez. Diqto prépare."),
        ),
    ),
)


CAMPAIGN_VIDEO_BY_PAGE = {video.page_path: video for video in CAMPAIGN_VIDEOS}


def campaign_video_for_page(page_path: str) -> CampaignVideo | None:
    return CAMPAIGN_VIDEO_BY_PAGE.get(page_path)


def video_schema(video: CampaignVideo) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "@id": f"{video.page_url}#video",
        "name": video.heading,
        "description": video.description,
        "thumbnailUrl": [video.poster_url],
        "uploadDate": video.upload_date,
        "duration": f"PT{video.duration_seconds}S",
        "contentUrl": video.video_url,
        "url": video.page_url,
        "mainEntityOfPage": video.page_url,
        "inLanguage": "fr-FR",
        "isAccessibleForFree": True,
        "isFamilyFriendly": True,
        "transcript": video.transcript_text,
        "publisher": {
            "@type": "Organization",
            "name": "DIQTO",
            "url": f"{BASE_URL}/",
        },
    }


def render_video_head(video: CampaignVideo) -> str:
    schema = json.dumps(video_schema(video), ensure_ascii=False, indent=2)
    return f'''<meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1">
<meta property="og:video" content="{video.video_url}">
<meta property="og:video:type" content="video/mp4">
<meta property="og:video:width" content="{video.width}">
<meta property="og:video:height" content="{video.height}">
<script type="application/ld+json" data-schema="campaign-video">
{schema}
</script>'''


CAMPAIGN_VIDEO_CSS = '''
.campaign-video { max-width:800px; margin:0 auto 52px; padding:0 24px; }
.campaign-video-copy { max-width:680px; margin:0 auto 24px; text-align:center; }
.campaign-video-eyebrow { color:var(--primary); font-size:13px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }
.campaign-video h2 { margin:8px 0 12px; font-size:clamp(26px,4vw,38px); line-height:1.12; letter-spacing:-.03em; }
.campaign-video-copy p:last-child { color:var(--dim); }
.campaign-video-player { width:min(100%,360px); margin:0 auto; aspect-ratio:9/16; overflow:hidden; border:1px solid var(--border); border-radius:24px; background:#050806; box-shadow:0 24px 60px rgba(0,0,0,.35); }
.campaign-video-player video { width:100%; height:100%; display:block; object-fit:cover; }
.campaign-video-disclosure { margin:14px auto 0; max-width:600px; color:var(--dim); font-size:12px; text-align:center; }
.campaign-video-transcript { margin:18px auto 0; max-width:680px; border-top:1px solid var(--border); border-bottom:1px solid var(--border); padding:16px 0; }
.campaign-video-transcript summary { cursor:pointer; font-weight:700; }
.campaign-video-transcript p { color:var(--dim); margin-top:12px; }
'''


def render_video_section(video: CampaignVideo) -> str:
    paragraphs = "\n".join(
        f"    <p>{escape(paragraph)}</p>" for paragraph in video.transcript
    )
    return f'''<section class="campaign-video" data-campaign-video="{video.trade_id}" aria-labelledby="campaign-video-{video.trade_id}">
  <div class="campaign-video-copy">
    <p class="campaign-video-eyebrow">Cas concret en 40 secondes</p>
    <h2 id="campaign-video-{video.trade_id}">{escape(video.heading)}</h2>
    <p>{escape(video.summary)}</p>
  </div>
  <div class="campaign-video-player">
    <video controls preload="metadata" playsinline poster="{video.poster_path}" aria-label="{escape(video.heading, quote=True)}">
      <source src="{video.video_path}" type="video/mp4">
      <track kind="captions" src="{video.captions_path}" srclang="fr" label="Français" default>
      Votre navigateur ne permet pas de lire cette vidéo.
    </video>
  </div>
  <p class="campaign-video-disclosure">Film de démonstration avec situation fictive et écrans Diqto sur données de démonstration. Rien n'est envoyé sans validation.</p>
  <details class="campaign-video-transcript">
    <summary>Lire la transcription complète</summary>
{paragraphs}
  </details>
</section>'''


def render_vtt(video: CampaignVideo) -> str:
    entries = ["WEBVTT", ""]
    for index, item in enumerate(video.cues, start=1):
        entries.extend(
            [str(index), f"{item.start} --> {item.end}", item.text, ""]
        )
    return "\n".join(entries)
