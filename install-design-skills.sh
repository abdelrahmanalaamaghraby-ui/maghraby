#!/usr/bin/env bash
# Installs the reviewed design skills for Claude Code.
# Every third-party skill is pinned to the exact commit that was reviewed
# (see github-design-skills-review.md), so later changes upstream are not pulled in.
#
# Usage:
#   bash install-design-skills.sh                 # install to ~/.claude/skills (all projects)
#   bash install-design-skills.sh --project       # install to ./.claude/skills (this project only)
#   bash install-design-skills.sh --zip           # also build ZIPs for upload to claude.ai
#   bash install-design-skills.sh --with-carousel # + arabic-brand-carousel (renders HTML/PNG, not Canva)
#   bash install-design-skills.sh --with-folio    # + folio (print design as HTML/PDF, runs scripts; not Canva)
set -euo pipefail

THIS_REPO="https://github.com/abdelrahmanalaamaghraby-ui/maghraby.git"
THIS_REF="claude/serene-cerf-oq5gfq"

DEST="$HOME/.claude/skills"
MAKE_ZIP=0
WITH_CAROUSEL=0
WITH_FOLIO=0
for arg in "$@"; do
  case "$arg" in
    --project) DEST="$(pwd)/.claude/skills" ;;
    --zip) MAKE_ZIP=1 ;;
    --with-carousel) WITH_CAROUSEL=1 ;;
    --with-folio) WITH_FOLIO=1 ;;
    -h|--help) sed -n 2,13p "$0"; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 1 ;;
  esac
done

command -v git >/dev/null || { echo "git is required" >&2; exit 1; }
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$DEST"

# fetch <name> <repo-url> <ref-or-sha>
fetch() {
  local dir="$WORK/$1"
  git init -q "$dir"
  git -C "$dir" remote add origin "$2"
  git -C "$dir" fetch -q --depth 1 origin "$3"
  git -C "$dir" checkout -q FETCH_HEAD
}

# install <src-dir> <skill-name>
install_skill() {
  local src="$1" name="$2"
  [ -f "$src/SKILL.md" ] || { echo "  ✗ $name: SKILL.md not found in $src" >&2; return 1; }
  if [ -e "$DEST/$name" ]; then
    mv "$DEST/$name" "$DEST/$name.bak-$(date +%Y%m%d%H%M%S)"
    echo "  (backed up existing $name)"
  fi
  cp -R "$src" "$DEST/$name"
  echo "  ✓ $name"
}

echo "Installing skills into: $DEST"

echo "• This repo (canva-design-system)"
fetch maghraby "$THIS_REPO" "$THIS_REF"
install_skill "$WORK/maghraby/skills/canva-design-system" canva-design-system

echo "• anthropics/skills @ ca45fc4 (theme-factory)"
fetch anthropics https://github.com/anthropics/skills.git ca45fc496a3436251f191354091d557da31c15b5
install_skill "$WORK/anthropics/skills/theme-factory" theme-factory

echo "• Paramchoudhary/ResumeSkills @ 74ae19e (3 CV skills)"
fetch resume https://github.com/Paramchoudhary/ResumeSkills.git 74ae19e7c62b0516d1c298328e5544976c12da5d
for s in resume-formatter resume-ats-optimizer resume-bullet-writer; do
  install_skill "$WORK/resume/skills/$s" "$s"
done

if [ "$WITH_CAROUSEL" = 1 ]; then
  echo "• saoudphotos/arabic-brand-carousel @ 1592a37"
  fetch carousel https://github.com/saoudphotos/arabic-brand-carousel.git 1592a370471790ca3e22df4204b29c72adcfcf3a
  install_skill "$WORK/carousel/arabic-brand-carousel" arabic-brand-carousel
fi

if [ "$WITH_FOLIO" = 1 ]; then
  echo "• Folio @ 6dd90e0 (read skills/folio/scripts before first use)"
  fetch folio https://github.com/stanesjenson11-lgtm/Folio---Claude-Design-Skill-For-Poster-Brochure-Magazine.git 6dd90e0019a39539d6ac6543e53c8437a3a8e13f
  install_skill "$WORK/folio/skills/folio" folio
fi

if [ "$MAKE_ZIP" = 1 ]; then
  command -v zip >/dev/null || { echo "zip is required for --zip" >&2; exit 1; }
  ZIPDIR="$(pwd)/skill-zips"
  mkdir -p "$ZIPDIR"
  for d in "$DEST"/*/; do
    n="$(basename "$d")"
    case "$n" in *.bak-*) continue ;; esac
    (cd "$DEST" && zip -qr "$ZIPDIR/$n.zip" "$n")
  done
  echo "ZIPs for claude.ai (Settings → Capabilities → Skills → Upload): $ZIPDIR"
fi

echo
echo "Done. Installed skills:"
ls -1 "$DEST" | grep -v '\.bak-' | sed 's/^/  - /'
echo "Restart Claude Code (or start a new session) so it picks up the skills."
